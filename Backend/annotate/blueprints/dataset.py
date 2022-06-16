import os.path

import pymysql
import json
import zipfile
import imghdr

from annotate.utils.custom_coco import CustomCocoAnnotation, CustomCoco
from sahi.utils.coco import Coco, CocoCategory, CocoImage, CocoAnnotation
from sahi.utils.file import save_json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request, current_app
from PIL import Image as PILImage
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from annotate.models import User, Dataset, DatasetLabel, LabelGroup, Image, AnnotationBbox, db
from annotate.utils.utils import make_unique
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import event

dataset_bp = Blueprint('dataset', __name__)
api = Api(dataset_bp)
allowed_content_type = ["image/jpeg", "image/png", "image/bmp"]


@event.listens_for(Image, 'before_delete')
def cascade_delete_image(mapper, connection, target):
    os.remove(os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], target.img_src))


@dataset_bp.route('/info/<int:dataset_id>', methods=['GET'])
@jwt_required()
def getDatasetInfo(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    dataset_dict = dataset.toDict()
    return jsonify(dataset_dict)


@dataset_bp.route('/auto/<int:dataset_id>', methods=['PUT'])
@jwt_required()
def preAutoAnnotate(dataset_id):
    dataset = Dataset.query.get(dataset_id)
    user_id = get_jwt_identity()
    if dataset is None:
        return 'operated dataset not exist', 404
    if dataset.user_id != user_id:  # dataset owner is not the same as the user of token
        return 'NotAllowed', 403
    if dataset:
        dataset.status = 'InAutoAnnotation'
        db.session.commit()
        from acelery.tasks import auto_annotate
        auto_annotate.delay(dataset_id)
    return 'success'


class DatasetList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        datasets = User.query.get(user_id).datasets
        datasets_arr = []
        for dataset in datasets:
            datasets_arr.append(dataset.toDict())
        return jsonify(datasets_arr)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        request_data = request.get_json()
        added_dataset = Dataset(
            name=request_data.get('name'),
            description=request_data.get('description'),
            user_id=user_id
        )
        db.session.add(added_dataset)
        failed = False
        err_reason = ''
        try:
            db.session.commit()
        except pymysql.Error as err:
            failed = True
            err_reason = str(err)
        except SQLAlchemyError as err:
            failed = True
            err_reason = str(err)
        if failed:
            return err_reason, 409
        return 'success'


#  '/<int:dataset_id>'
class DatasetItem(Resource):
    @jwt_required()
    def delete(self, dataset_id):
        user_id = get_jwt_identity()
        dataset = Dataset.query.get(dataset_id)
        if dataset.user_id != user_id:  # dataset owner is not the same as the user of token
            return 'NotAllowed', 403
        if dataset:
            db.session.delete(dataset)
            failed = False
            err_reason = ''
            try:
                db.session.commit()
            except pymysql.Error as err:
                failed = True
                err_reason = str(err)
            except SQLAlchemyError as err:
                failed = True
                err_reason = str(err)
            if failed:
                return err_reason, 409
            return 'success'
        return "deleted dataset doesn't exist"

    @jwt_required()
    def put(self, dataset_id):
        file = request.files.get('file')
        try:
            content = json.loads(file.read())
        except json.decoder.JSONDecodeError as err:
            return 'Json format error', 400
        dataset = Dataset.query.get(dataset_id)
        dataset.custom_label_format = content
        db.session.commit()
        return 'success'

    @jwt_required()
    def get(self, dataset_id):
        """
           获取 COCO format 数据集
        """
        coco = CustomCoco()
        dataset = Dataset.query.get(dataset_id)
        category_id_map = {}
        for idx, label in enumerate(dataset.labels):
            coco.add_category(CocoCategory(id=idx, name=label.name))
            category_id_map[label.id] = idx
        for image in dataset.images:
            _, file_name = os.path.split(image.img_src)
            coco_image = CocoImage(file_name=file_name, height=image.height, width=image.width)
            for bbox in image.annotation_bboxes:
                coco_image.add_annotation(
                    CustomCocoAnnotation(
                        bbox=[bbox.factorX * image.width,
                              bbox.factorY * image.height,
                              bbox.factorWidth * image.width,
                              bbox.factorHeight * image.height],
                        category_id=category_id_map[bbox.dataset_label_id],
                        attributes=bbox.additionalInfo
                    )
                )
            coco.add_image(coco_image)

        try:
            tmp_json_path = os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], make_unique('labels.json'))
            save_json(data=coco.json, save_path=tmp_json_path)
            zip_name = "%s.zip" % dataset.name
            tmp_zip_path = os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], make_unique(zip_name))
            try:
                zf = zipfile.ZipFile(tmp_zip_path, 'w')
                for image in dataset.images:
                    zf.write(os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], image.img_src)
                             , arcname=os.path.join('images', image.img_src))
                zf.write(tmp_json_path, 'labels.json')
            finally:
                zf.close()
        finally:
            file_size = os.path.getsize(tmp_zip_path)

            def generate_and_remove_file():
                with open(tmp_zip_path, 'rb') as f:
                    for line in f:
                        yield line
                os.remove(tmp_zip_path)
                os.remove(tmp_json_path)
        return current_app.response_class(generate_and_remove_file(), headers={
            'content-type': 'application/zip',
            'content-disposition': 'attachment; filename=%s;' % zip_name.encode("utf-8").decode("latin1"),
            'content-length': file_size
        })


# '/<int:dataset_id>/images'
class DatasetImageList(Resource):
    @jwt_required()
    def get(self, dataset_id):
        user_id = get_jwt_identity()
        dataset = Dataset.query.get(dataset_id)
        if dataset.user_id != user_id:  # dataset owner is not the same as the user of token
            return 'NotAllowed', 403
        images_arr = []
        for image in dataset.images:
            images_arr.append(image.toDict())
        return jsonify(images_arr)

    @jwt_required()
    def delete(self, dataset_id):
        request_data = request.get_json()
        deleted_arr = request_data.get('deletedIndexArray')
        for image_id in deleted_arr:
            image = Image.query.get(image_id)
            if image:
                db.session.delete(image)
        db.session.commit()
        return 'Success'

    @jwt_required()
    def post(self, dataset_id):
        """
           @desc 上传导入图片
        """
        upload_format = request.args.get('format')
        is_zip = upload_format == 'zip'
        user_id = get_jwt_identity()
        dataset = Dataset.query.get(dataset_id)
        if dataset.user_id != user_id:  # dataset owner is not the same as the user of token
            return 'NotAllowed', 403
        if is_zip:
            file = request.files.get('file')
            file_like_object = file.stream._file
            zipfile_ob = zipfile.ZipFile(file_like_object)
            file_names = zipfile_ob.namelist()
            for file_name in file_names:
                # check
                with zipfile_ob.open(file_name) as fp:
                    try:
                        # maybe throw error because invalid image
                        PILImage.open(fp)
                    except IOError:
                        continue
                with zipfile_ob.open(file_name) as fp:
                    f = FileStorage(fp)
                    original_filename = secure_filename(f.filename)
                    unique_filename = make_unique(original_filename)
                    f.save(os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], unique_filename))
                    width, height = PILImage.open(f).size
                    dataset.images.append(Image(
                        width=width,
                        height=height,
                        img_src=unique_filename
                    ))
                    db.session.commit()
        else:
            file_list = request.files.getlist('file')
            if file_list:
                for file in file_list:
                    original_filename = secure_filename(file.filename)
                    unique_filename = make_unique(original_filename)
                    file.save(os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], unique_filename))
                    img = PILImage.open(file)
                    width, height = img.size
                    dataset.images.append(Image(
                        width=width,
                        height=height,
                        img_src=unique_filename
                    ))
                db.session.commit()
        return 'success'


# '/<int:dataset_id>/labels'
class DatasetLabelList(Resource):
    @jwt_required()
    def get(self, dataset_id):
        labels = Dataset.query.get(dataset_id).labels
        labels_arr = []
        for label in labels:
            labels_arr.append(label.toDict())
        return jsonify(labels_arr)

    @jwt_required()
    def post(self, dataset_id):
        request_data = request.get_json()
        if request_data.get('labelGroupImportFlag'):
            # 当前数据集
            current_dataset = Dataset.query.get(dataset_id)
            # 当前已有的数据集的 label names
            origin_labels = map(lambda x: x.name, current_dataset.labels)
            # 即将导入的标签集已有的labels
            imported_labels = LabelGroup.query.get(request_data.get('labelGroupID')).labels
            # 冲突的label
            conflicted_labels = []
            for label in imported_labels:
                if label.name in origin_labels:
                    conflicted_labels.append(label.name)
                else:
                    current_dataset.labels.append(DatasetLabel(
                        name=label.name,
                        color=label.color
                    ))
            db.session.commit()
            return jsonify(conflicted_labels)
        else:
            added_label = DatasetLabel(
                **request_data.get('label'),
                dataset_id=dataset_id
            )
            db.session.add(added_label)
            failed = False
            try:
                db.session.commit()
            except pymysql.Error as err:
                failed = True
                err_reason = str(err)
            except SQLAlchemyError as err:
                failed = True
                err_reason = str(err)
            if failed:
                return err_reason, 409
            return 'success'


# '/labels/<int:label_id>'
class DatasetLabelItem(Resource):
    @jwt_required()
    def delete(self, label_id):
        deleted_label = DatasetLabel.query.get(label_id)
        if deleted_label:
            db.session.delete(deleted_label)
            failed = False
            err_reason = ''
            try:
                db.session.commit()
            except pymysql.Error as err:
                failed = True
                err_reason = str(err)
            except SQLAlchemyError as err:
                failed = True
                err_reason = str(err)
            if failed:
                return err_reason, 409
            return 'success'
        return "deleted label doesn't exist"

    @jwt_required()
    def put(self, label_id):
        updated_label = DatasetLabel.query.get(label_id)
        request_data = request.get_json()
        updated_label.name = request_data.get('name')
        updated_label.color = request_data.get('color')
        failed = False
        err_reason = ''
        try:
            db.session.commit()
        except pymysql.Error as err:
            failed = True
            err_reason = str(err)
        except SQLAlchemyError as err:
            failed = True
            err_reason = str(err)
        if failed:
            return err_reason, 409
        return 'success'


# '/images/<int:image_id>/bboxes'
class DatasetImageAnnotationBoxList(Resource):
    @jwt_required()
    def post(self, image_id):
        AnnotationBbox.query.filter_by(image_id=image_id).delete()
        bboxes = request.get_json()
        for bbox in bboxes:
            db.session.add(AnnotationBbox(
                **bbox,
                image_id=image_id
            ))
        annotated_image = Image.query.get(image_id)
        if len(bboxes) == 0:
            annotated_image.labeled = False
        else:
            annotated_image.labeled = True
        db.session.commit()

    @jwt_required()
    def get(self, image_id):
        bboxes = Image.query.get(image_id).annotation_bboxes
        bboxes_arr = []
        for bbox in bboxes:
            bboxes_arr.append(bbox.toDict())
        return jsonify(bboxes_arr)


api.add_resource(DatasetImageAnnotationBoxList, '/images/<int:image_id>/bboxes')
api.add_resource(DatasetLabelItem, '/labels/<int:label_id>')
api.add_resource(DatasetLabelList, '/<int:dataset_id>/labels')
api.add_resource(DatasetImageList, '/<int:dataset_id>/images')
api.add_resource(DatasetItem, '/<int:dataset_id>')
api.add_resource(DatasetList, '/')
