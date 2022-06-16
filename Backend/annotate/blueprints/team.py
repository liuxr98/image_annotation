from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError
from annotate.models import db, User, Team, TeamMember
from sqlalchemy import func
from flask_restful import Api, Resource
import pymysql

team_bp = Blueprint('team', __name__)
api = Api(team_bp)


class TeamList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        teams = User.query.get(user_id).teams
        teams_arr = []
        for team in teams:
            teams_arr.append(team.toDict())
        return jsonify(teams_arr)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        request_data = request.get_json()
        added_team = Team(
            name=request_data.get('name'),
            user_id=user_id
        )
        db.session.add(added_team)
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


class TeamItem(Resource):
    @jwt_required()
    def get(self, team_id):
        user_id = get_jwt_identity()
        team = Team.query.get(team_id)
        if team:
            if team.user_id != user_id:  # team owner is not the same as the user of token
                return 'NotAllowed', 403
            res = team.toDict()
            members_arr = []
            for member in team.members:
                members_arr.append(member.toDict())
            res['members'] = members_arr
            return jsonify(res)
        return {}

    @jwt_required()
    def delete(self, team_id):
        user_id = get_jwt_identity()
        team = Team.query.get(team_id)
        if team:
            if team.user_id != user_id:  # team owner is not the same as the user of token
                return 'NotAllowed', 403
            db.session.delete(team)
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
        return "deleted team doesn't exist"


class TeamMemberList(Resource):
    @jwt_required()
    def post(self, team_id):
        request_data = request.get_json()
        user = User.query.filter_by(username=func.binary(request_data.get('name'))).first()
        added_member = TeamMember(
            member_id=user.id,
            role=request_data.get('role'),
            team_id=team_id
        )
        db.session.add(added_member)
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


class TeamMemberItem(Resource):
    @jwt_required()
    def delete(self, member_id):
        member = TeamMember.query.get(member_id)
        if member:
            db.session.delete(member)
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
        return "deleted member doesn't exist"


api.add_resource(TeamList, '/')
api.add_resource(TeamItem, '/<int:team_id>')
api.add_resource(TeamMemberList, '/<int:team_id>/members')
api.add_resource(TeamMemberItem, '/members/<int:member_id>')
