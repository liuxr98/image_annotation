import os

import click
from flask import Flask, send_from_directory
from flask.json import JSONEncoder
from datetime import date

from annotate.settings import config
from annotate.blueprints.dataset import dataset_bp
from annotate.blueprints.labelgroup import label_group_bp
from annotate.blueprints.team import team_bp
from annotate.blueprints.user import user_bp
from annotate.blueprints.teamtask import teamtask_bp
from annotate.blueprints.aimodel import model_bp
from annotate.blueprints.detection import detection_bp
from annotate.extensions import db, cors, jwt


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)


def create_app(config_name=None, platform=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask('annotate')
    app.config.from_object(config[config_name])
    if config_name == 'development':
        if platform is not None and platform == 'wsl':
            app.config.update(
                SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:PASSWORD@ZYC-Y9000P.local:3306/annotate',
            )
    app.json_encoder = MyJSONEncoder

    @app.route('/data/<string:image_name>')
    def get_image(image_name):
        return send_from_directory(app.config['IMAGE_UPLOAD_FOLDER'], image_name)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_blueprints(app):
    app.register_blueprint(dataset_bp, url_prefix='/datasets')
    app.register_blueprint(label_group_bp, url_prefix='/labelgroups')
    app.register_blueprint(team_bp, url_prefix='/teams')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(teamtask_bp, url_prefix='/teamtasks')
    app.register_blueprint(model_bp, url_prefix='/models')
    app.register_blueprint(detection_bp, url_prefix='/detection')


def register_extensions(app):
    db.init_app(app)
    cors.init_app(app, expose_headers=["Content-Disposition", "Content-Type"], supports_credentials=True, origins=["http://127.0.0.1:8080", "http://101.34.255.125:8080"])
    jwt.init_app(app)


def register_commands(app):
    def clear_dir(folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database"""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo("Initialized database.")

    @app.cli.command()
    def forge():
        """Generate fake data"""
        db.drop_all()
        db.create_all()
        clear_dir(app.config['IMAGE_UPLOAD_FOLDER'])
        clear_dir(app.config['MODEL_UPLOAD_FOLDER'])

        from annotate.fakes import fake_user, fake_dataset, fake_label_group, fake_team
        fake_user()
        fake_dataset(app=app)
        fake_label_group()
        fake_team()

    @app.cli.command()
    def clear():
        db.drop_all()
        """Clear the image and model folder"""
        clear_dir(app.config['IMAGE_UPLOAD_FOLDER'])
        clear_dir(app.config['MODEL_UPLOAD_FOLDER'])
