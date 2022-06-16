"""
    构造虚拟数据用于测试
"""
import os

from PIL import Image as PILImage
from faker import Faker
from annotate.models import *
from werkzeug.security import generate_password_hash
from annotate.utils.utils import make_unique

Faker.seed(0)
fake = Faker()


def fake_user(count=5):
    for i in range(count):
        user = User(username=fake.user_name(), password_hash=generate_password_hash('123456'))
        db.session.add(user)
    db.session.commit()


def fake_dataset(app, count=5):
    users = User.query.all()
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    for user in users:
        for i in range(count):
            dataset = Dataset(
                name=fake.bothify(text='dataset-????####'),
                description=fake.sentence(),
                user_id=user.id
            )
            # fake label in dataset
            for j in range(3):
                label = DatasetLabel(
                    name=fake.word(),
                    color=fake.color()
                )
                dataset.labels.append(label)

            # fake image in dataset
            for root, dirs, files in os.walk(os.path.join(basedir, 'mock-images')):
                for file_name in files:
                    img = PILImage.open(os.path.join(root, file_name))
                    unique_filename = make_unique(file_name)
                    img.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], unique_filename))
                    width, height = img.size
                    dataset.images.append(Image(
                        img_src=unique_filename,
                        width=width,
                        height=height,
                    ))
            db.session.add(dataset)
    db.session.commit()


def fake_label_group(count=3):
    users = User.query.all()
    for user in users:
        for i in range(count):
            label_group = LabelGroup(
                name=fake.bothify(text='label-group-????####'),
                user_id=user.id
            )
            for j in range(5):
                label = LabelGroupLabel(
                    name=fake.word(),
                    color=fake.color()
                )
                label_group.labels.append(label)
            db.session.add(label_group)
    db.session.commit()


def fake_team(count=3):
    users = User.query.all()
    for user in users:
        for i in range(count):
            team = Team(
                name=fake.bothify(text='team-????####'),
                user_id=user.id,
            )
            # 默认情况下队伍成员只有队伍创建者本人
            team.members.append(TeamMember(
                member_id=user.id
            ))
            db.session.add(team)
    db.session.commit()
