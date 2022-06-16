from annotate.extensions import db
from werkzeug.security import check_password_hash
from sqlalchemy import inspect
from sqlalchemy.orm import object_session
from datetime import datetime


class AuditMixin:
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class ToDictMixin:
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class User(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(256))
    datasets = db.relationship('Dataset', cascade='all')
    team_tasks = db.relationship('TeamTask', cascade='all')
    subtasks = db.relationship('SubTeamTask', cascade='all')
    label_groups = db.relationship('LabelGroup', cascade='all')
    teams = db.relationship('Team', cascade='all')
    models = db.relationship('AIModel', cascade='all')

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


class Dataset(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # is_in_team_task = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('None', 'InTeamTask', 'InAutoAnnotation'), default='None')
    labels = db.relationship('DatasetLabel', cascade='all')
    images = db.relationship('Image', cascade='all')
    custom_label_format = db.Column(db.JSON)

    @property
    def labeled_images_cnt(self):
        return object_session(self).query(Image).\
                with_parent(self).\
                filter(Image.dataset_id == self.id,
                       Image.labeled == True).count()
        # return len(self.images)

    @property
    def images_cnt(self):
        return object_session(self).\
                query(Image).\
                with_parent(self).\
                filter(Image.dataset_id == self.id).count()

    def toDict(self):
        res = super().toDict()
        res['images_cnt'] = self.images_cnt
        res['labeled_images_cnt'] = self.labeled_images_cnt
        return res


class DatasetLabel(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    color = db.Column(db.String(20))
    annotation_bboxes = db.relationship('AnnotationBbox', backref='label', cascade='all')
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))


class LabelGroup(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    labels = db.relationship('LabelGroupLabel', cascade='all')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class LabelGroupLabel(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    color = db.Column(db.String(20))
    label_group_id = db.Column(db.Integer, db.ForeignKey('label_group.id'))


class Image(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    img_src = db.Column(db.String(256))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    subtask_id = db.Column(db.Integer, db.ForeignKey('sub_team_task.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('team_task.id'))
    labeled = db.Column(db.Boolean, default=False)
    annotation_bboxes = db.relationship('AnnotationBbox', backref='image', cascade='all')


class AnnotationBbox(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    factorX = db.Column(db.Float)
    factorY = db.Column(db.Float)
    factorWidth = db.Column(db.Float)
    factorHeight = db.Column(db.Float)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    dataset_label_id = db.Column(db.Integer, db.ForeignKey('dataset_label.id'))
    # type = db.Column(db.Integer, default=0)  # 标识当前标注框是否为团队任务标注狂
    additionalInfo = db.Column(db.JSON)

    def toDict(self):
        dict_res = super().toDict()
        label_info = getattr(self, 'label')
        if label_info is None:
            return dict_res
        dict_res['label_info'] = label_info.toDict()
        return dict_res


class TeamTask(db.Model, AuditMixin, ToDictMixin):  # 团队任务
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    status = db.Column(
        db.Enum("InProgress", "Finished", "TerminatedReserved", "TerminatedUnreserved", "Reviewed"),
        default="InProgress"
    )
    assigner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    subtask_num = db.Column(db.Integer)
    subtask_submitted_num = db.Column(db.Integer, default=0)
    subtasks = db.relationship('SubTeamTask', backref='team_task')
    dataset = db.relationship('Dataset')
    images = db.relationship('Image')

    def toDict(self):
        dict_res = super().toDict()
        dataset_info = getattr(self, 'dataset')
        dict_res['dataset_name'] = dataset_info.name
        return dict_res


class SubTeamTask(db.Model, AuditMixin, ToDictMixin):  # 团队任务的子任务
    id = db.Column(db.Integer, primary_key=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigner_username = db.Column(db.String(30))
    type = db.Column(db.Enum('label', 'review'), default='label')  # 描述子任务是审核任务还是标注任务，目前仅支持标注任务
    status = db.Column(db.Enum('InProgress', 'Submitted', 'Terminated', 'Deleted'), default='InProgress')  # 描述子任务状态
    team_task_id = db.Column(db.Integer, db.ForeignKey('team_task.id'))
    team_task_name = db.Column(db.String(30))
    dataset_id = db.Column(db.Integer)
    images = db.relationship('Image')


class Team(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    members = db.relationship('TeamMember', cascade='all')

    def toDict(self):
        dict_res = super().toDict()
        dict_res['memberCnt'] = len(getattr(self, 'members'))
        return dict_res


class TeamMember(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    role = db.Column(db.Enum('labeler', 'reviewer'), default='labeler')
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    member = db.relationship('User')

    def toDict(self):
        dict_res = super().toDict()
        dict_res['member_name'] = getattr(self, 'member').username
        return dict_res


class AIModel(db.Model, ToDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(30))
    url = db.Column(db.String(256))
    proj_url = db.Column(db.String(256))
    status = db.Column(db.Enum('NotTrained', 'InProgress', 'Error', 'Finished'), default='NotTrained')
