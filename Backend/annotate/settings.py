import os
import datetime

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IMAGE_UPLOAD_FOLDER = os.path.join(basedir, 'data/images')
    MODEL_UPLOAD_FOLDER = os.path.join(basedir, 'data/models')

    YOLOV5_MODULE_FOLDER = os.path.join(basedir, 'yolov5')
    YOLOV5_WEIGHTS_FOLDER = os.path.join(basedir, 'yolov5/runs/weights')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class DevelopmentConfig(BaseConfig):
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_BACKEND_URL = 'redis://localhost:6379'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/annotate'


class ProductionConfig(BaseConfig):
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    CELERY_BACKEND_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'mysql+pymysql://root:123456@localhost:3306/annotate')  # 使用 pymysql driver


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
