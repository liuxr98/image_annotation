import json
import pathlib
import shutil
import zipfile
import os

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api, Resource

import annotate.settings
from annotate.models import db, User, AIModel
from annotate.utils.utils import make_unique
from werkzeug.utils import secure_filename
from sqlalchemy import event

model_bp = Blueprint('model', __name__)
api = Api(model_bp)


@event.listens_for(AIModel, 'before_delete')
def cascade_delete_model(mapper, connect, target):
    shutil.rmtree(os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], target.url))


class ModelList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        models = User.query.get(user_id).models
        models_arr = []
        for model in models:
            models_arr.append(model.toDict())
        return jsonify(models_arr)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        name = request.form['name']
        projName = request.form['projName']

        file = request.files.get('file')
        zipfile_name = os.path.splitext(file.filename)[0]

        # projName 为空
        if not projName:
            # 默认使用 zip 文件名
            projName = zipfile_name
        file_like_object = file.stream._file
        zipfile_ob = zipfile.ZipFile(file_like_object)

        original_filename = secure_filename(name)
        unique_filename = make_unique(original_filename)

        extract_path = os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], unique_filename)

        zipfile_ob.extractall(path=extract_path)
        user.models.append(AIModel(
            name=name,
            url=unique_filename,
            proj_url=os.path.join(unique_filename, projName)
        ))
        db.session.commit()
        return 'Success'


class ModelItem(Resource):
    @jwt_required()
    def delete(self, model_id):
        ai_model = AIModel.query.get(model_id)
        if ai_model:
            db.session.delete(ai_model)
            db.session.commit()
            return 'Success'
        return 'Deleted Model Not Exist'

    @jwt_required()
    def put(self, model_id):
        file = request.files.get('file')
        ai_model = AIModel.query.get(model_id)
        if ai_model:
            save_path = os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], ai_model.proj_url, file.filename)
            file.save(save_path)
            return 'Success'
        return 'Operated Model Not Exist'

    @jwt_required()
    def get(self, model_id):
        """
            @desc: 获取模型的 train.log, evaluate.log 内容
        """
        ai_model = AIModel.query.get(model_id)
        if ai_model:
            try:
                with open(os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], ai_model.proj_url, 'train.log'), 'r') as f:
                    train_content = f.read()
            except IOError:
                train_content = ''
            try:
                with open(os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], ai_model.proj_url, 'evaluate.log'), 'r') as f:
                    evaluate_content = f.read()
            except IOError:
                evaluate_content = ''
            return jsonify(
                {
                    'name': ai_model.name,
                    'train_log': train_content,
                    'evaluate_log': evaluate_content
                }
            )
        return 'Operated Model Not Exist'


@model_bp.route('/<int:model_id>/train', methods=['POST'])
@jwt_required()
def train_model(model_id):
    model = AIModel.query.get(model_id)
    model.status = 'InProgress'
    from acelery.tasks import train_model
    train_model.delay(model_id)
    return 'Success'


@model_bp.route('/<int:model_id>/evaluate', methods=['POST'])
@jwt_required()
def evaluate_model(model_id):
    from acelery.tasks import evaluate_model
    evaluate_model.delay(model_id)
    return 'Success'


@model_bp.route('/<int:model_id>/export', methods=['GET'])
@jwt_required()
def export_model(model_id):
    """
        导出模型，默认导出路径为模型文件夹下的 /weights
    """
    model = AIModel.query.get(model_id)
    zip_name = "%s.zip" % model.name
    tmp_zip_path = os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], make_unique(zip_name))

    def zip_dir(path, zip_handle: zipfile.ZipFile):
        """
            @desc 压缩指定文件夹
            :param path: the path of zipped folder
            :param zip_handle: zipfile handle
            :return: none
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_handle.write(os.path.join(root, file),
                                 os.path.relpath(os.path.join(root, file),
                                                 os.path.join(path, '..')))

    try:
        zf = zipfile.ZipFile(tmp_zip_path, 'w')
        zipped_folder_path = os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], model.proj_url, 'weights')
        zip_dir(zipped_folder_path, zf)
    finally:
        zf.close()
    file_size = os.path.getsize(tmp_zip_path)

    def generate_and_remove_file():
        with open(tmp_zip_path, 'rb') as f:
            for line in f:
                yield line
        os.remove(tmp_zip_path)

    return current_app.response_class(generate_and_remove_file(), headers={
        'content-type': 'application/zip',
        'content-disposition': 'attachment; filename=%s;' % zip_name.encode("utf-8").decode("latin1"),
        'content-length': file_size
    })


api.add_resource(ModelList, '/')
api.add_resource(ModelItem, '/<int:model_id>')
