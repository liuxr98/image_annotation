# from celery import Celery
#
# import os
#
# from flask import Flask, send_from_directory
# from flask.json import JSONEncoder
# from datetime import date
#
# from annotate.settings import config
# from annotate.extensions import db, cors, jwt
#
#
# class MyJSONEncoder(JSONEncoder):
#     def default(self, o):
#         if isinstance(o, date):
#             return o.isoformat()
#         return super().default(o)
#
#
# def create_app(config_name=None):
#     if config_name is None:
#         config_name = os.getenv('FLASK_CONFIG', 'development')
#     app = Flask('acelery')
#     app.config.from_object(config[config_name])
#     app.json_encoder = MyJSONEncoder
#
#     @app.route('/data/<string:image_name>')
#     def get_image(image_name):
#         return send_from_directory(app.config['IMAGE_UPLOAD_FOLDER'], image_name)
#
#     register_extensions(app)
#     return app
#
#
# def register_extensions(app):
#     db.init_app(app)
#     cors.init_app(app, expose_headers=["Content-Disposition"])
#     jwt.init_app(app)
#
#
# def make_celery(app=None):
#     app = app or create_app()
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase):
#         abstract = True
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
