from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from annotate.models import User, LabelGroup, LabelGroupLabel, db
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
import pymysql

label_group_bp = Blueprint('labelgroup', __name__)
api = Api(label_group_bp)


class LabelGroupList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        labelgroups = User.query.get(user_id).label_groups
        labelgroups_arr = []
        for labelgroup in labelgroups:
            labelgroups_arr.append(labelgroup.toDict())
        return jsonify(labelgroups_arr)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        request_data = request.get_json()
        added_labelgroup = LabelGroup(
            name=request_data.get('name'),
            user_id=user_id  # current user
        )
        for label in request_data.get('labels'):
            added_labelgroup.labels.append(LabelGroupLabel(
                name=label['name'],
                color=label['color'],
            ))
        db.session.add(added_labelgroup)
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


class LabelGroupItem(Resource):
    @jwt_required()
    def delete(self, label_group_id):
        labelgroup = LabelGroup.query.get(label_group_id)
        if labelgroup:
            db.session.delete(labelgroup)
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
        return "deleted labelgroup doesn't exist"


class LabelList(Resource):
    @jwt_required()
    def get(self, label_group_id):
        labelgroup = LabelGroup.query.get(label_group_id)
        labels = labelgroup.labels
        labels_arr = []
        for label in labels:
            labels_arr.append(label.toDict())
        return jsonify(labels_arr)

    @jwt_required()
    def post(self, label_group_id):
        request_data = request.get_json()
        added_label = LabelGroupLabel(
            name=request_data.get('name'),
            color=request_data.get('color'),
            label_group_id=label_group_id
        )
        db.session.add(added_label)
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


class LabelItem(Resource):
    @jwt_required()
    def put(self, label_id):
        updated_label = LabelGroupLabel.query.get(label_id)
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

    @jwt_required()
    def delete(self, label_id):
        label = LabelGroupLabel.query.get(label_id)
        if label:
            db.session.delete(label)
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


api.add_resource(LabelItem, '/labels/<int:label_id>')
api.add_resource(LabelList, '/<int:label_group_id>/labels')
api.add_resource(LabelGroupItem, '/<int:label_group_id>')
api.add_resource(LabelGroupList, '/')
