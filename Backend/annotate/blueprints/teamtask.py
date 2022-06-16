from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from annotate.models import db, TeamTask, User, Team, SubTeamTask, Dataset, Image, TeamMember
from flask_restful import Api, Resource
import pymysql

teamtask_bp = Blueprint('teamtask', __name__)
api = Api(teamtask_bp)


# '/'
class TeamTaskList(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        request_data = request.get_json()
        team_id = request_data.get('teamID')
        dataset_id = request_data.get('datasetID')
        task_name = request_data.get('name')

        added_teamtask = TeamTask(
            name=task_name,
            dataset_id=dataset_id,
            team_id=team_id,
            status="InProgress",
            assigner_id=user_id,
        )
        dataset = Dataset.query.get(dataset_id)
        dataset.status = 'InTeamTask'  # 处于团队标注的任务集将被锁定

        unlabeled_images = Image.query.filter_by(dataset_id=dataset_id).filter_by(labeled=False).all()
        unlabeled_images_cnt = len(unlabeled_images)

        labeler_members = TeamMember.query.filter_by(team_id=team_id).filter_by(role='labeler').all()
        labeler_members_cnt = len(labeler_members)

        allocate_num, remain = unlabeled_images_cnt // labeler_members_cnt, unlabeled_images_cnt % labeler_members_cnt
        added_teamtask.subtask_num = labeler_members_cnt  # 发布的子任务数量等于团队标注员人数（暂时不考虑审核任务）
        image_index = 0

        for member in labeler_members:
            subtask = SubTeamTask(
                assignee_id=member.member_id,
                assigner_username=current_user.username,
                type='label',
                status='InProgress',
                team_task_name=task_name,
                dataset_id=dataset_id
            )
            actual_allocate = allocate_num
            if remain > 0:
                remain -= 1
                actual_allocate += 1
            for i in range(actual_allocate):
                added_teamtask.images.append(unlabeled_images[image_index])
                subtask.images.append(unlabeled_images[image_index])
                image_index += 1
            added_teamtask.subtasks.append(subtask)

        db.session.add(added_teamtask)
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
    def get(self):
        user_id = get_jwt_identity()
        team_tasks = User.query.get(user_id).team_tasks
        team_tasks_arr = []
        for team_task in team_tasks:
            team_tasks_arr.append(team_task.toDict())
        return jsonify(team_tasks_arr)


# '/subs'
class SubTeamTaskList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        subtasks = User.query.get(user_id).subtasks
        subtasks_arr = []
        for subtask in subtasks:
            subtasks_arr.append(subtask.toDict())

        return jsonify(subtasks_arr)


# '/subs/<int:subtask_id>'
class SubTeamTaskItem(Resource):
    """
        @desc 提交子任务
    """
    @jwt_required()
    def put(self, subtask_id):
        user_id = get_jwt_identity()
        subtask = SubTeamTask.query.get(subtask_id)
        if subtask:
            if subtask.assignee_id != user_id:  # 被分配任务者与token表示的用户ID不一致，不允许操作
                return 'NotAllowed', 403
            if subtask.status == 'InProgress':
                team_task = subtask.team_task
                team_task.subtask_submitted_num += 1
                if team_task.subtask_submitted_num == team_task.subtask_num:
                    team_task.status = 'Finished'
            subtask.status = 'Submitted'
            db.session.commit()
            return 'Success'
        return "Submitted Task doesn't exist!"


# '/subs/<int:subtask_id>/images'
class SubtaskImageList(Resource):
    @jwt_required()
    def get(self, subtask_id):
        images = SubTeamTask.query.get(subtask_id).images
        images_arr = []
        for image in images:
            images_arr.append(image.toDict())
        return jsonify(images_arr)


# '/<int:teamtask_id>'
class TeamTaskItem(Resource):
    @jwt_required()
    def delete(self, teamtask_id):
        user_id = get_jwt_identity()
        team_task = TeamTask.query.get(teamtask_id)
        if team_task:
            if team_task.assinger_id != user_id:
                return 'NotAllowed', 403
            if team_task.status != 'Reviewed':  # 任务尚未验收通过，则删除已有标注框
                for image in team_task.images:
                    for annotation_box in image.annotation_bboxes:
                        db.session.delete(annotation_box)

            for subtask in team_task.subtasks:
                subtask.status = 'Deleted'
            team_task.dataset.status = 'None'  # 清除数据集的团队任务状态
            db.session.delete(team_task)
            db.session.commit()
            return 'success'
        return "deleted teamtask doesn't exist"

    """
        @desc 改变任务状态: 终止任务或验收任务
    """
    @jwt_required()
    def put(self, teamtask_id):
        request_data = request.get_json()
        team_task = TeamTask.query.get(teamtask_id)
        action_type = request_data.get('actionType')
        if action_type == 'Terminate':
            for subtask in team_task.subtasks:
                subtask.status = 'Terminated'

            reserved = request_data.get('reserved')
            if reserved:
                team_task.status = 'TerminatedReserved'
                for subtask in team_task.subtasks:
                    if subtask.status == 'InProgress':  # 尚未提交的任务的标注框不保存
                        for image in subtask.images:
                            for annotation_box in image.annotation_bboxes:
                                db.session.delete(annotation_box)
            else:
                team_task.status = 'TerminatedUnreserved'
                team_task.dataset.status = 'None'
                for image in team_task.images:
                    for annotation_box in image.annotation_bboxes:
                        db.session.delete(annotation_box)
            db.session.commit()
        elif action_type == 'Review':
            team_task.status = 'Reviewed'
            team_task.dataset.status = 'None'
            db.session.commit()


# '/<int:teamtask_id/images>'
class TeamTaskImageList(Resource):
    @jwt_required()
    def get(self, teamtask_id):
        images = TeamTask.query.get(teamtask_id).images
        images_arr = []
        for image in images:
            images_arr.append(image.toDict())
        return jsonify(images_arr)


api.add_resource(SubtaskImageList, '/subs/<int:subtask_id>/images')
api.add_resource(SubTeamTaskItem, '/subs/<int:subtask_id>')
api.add_resource(SubTeamTaskList, '/subs')
api.add_resource(TeamTaskItem, '/<int:teamtask_id>')
api.add_resource(TeamTaskImageList, '/<int:teamtask_id>/images')
api.add_resource(TeamTaskList, '/')
