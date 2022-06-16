import logging
import os

import torch.hub
from annotate import create_app
from annotate.models import User, AIModel, Image, Dataset, AnnotationBbox
from annotate.extensions import db
import subprocess
from flask import current_app
from celery import Celery


def make_celery(app=None):
    app = app or create_app()
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()


@celery.task
def train_model(model_id):
    model = AIModel.query.get(model_id)
    # replace 是因为保存 proj url 时环境为 windows, 而 celery 执行的环境为 linux, 其分隔符不一致，如果环境相同则不存在该问题
    work_dir = os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], model.proj_url.replace('\\', '/'))
    result = subprocess.run(['python', 'train.py'], capture_output=True, encoding='utf-8', cwd=work_dir)
    logging.info(result.stdout)
    if result.returncode != 0:
        model.status = 'Error'
    else:
        model.status = 'Finished'
    db.session.commit()


@celery.task
def evaluate_model(model_id):
    model = AIModel.query.get(model_id)
    work_dir = os.path.join(current_app.config['MODEL_UPLOAD_FOLDER'], model.proj_url.replace('\\', '/'))
    result = subprocess.run(['python', 'evaluate.py'], capture_output=True, encoding='utf-8', cwd=work_dir)
    logging.info(result.stdout)

@celery.task
def auto_annotate(dataset_id):
    try:
        dataset = Dataset.query.get(dataset_id)
        model = torch.hub.load(current_app.config['YOLOV5_MODULE_FOLDER'],
                               'custom',
                               path=os.path.join(current_app.config['YOLOV5_WEIGHTS_FOLDER'], 'best.pt'),
                               source='local'
                               )
        unlabeled_images = Image.query.filter_by(dataset_id=dataset_id).filter_by(labeled=False).all()
        images_batch = []
        for image in unlabeled_images:
            img_path = os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], image.img_src)
            images_batch.append(img_path)
        results = model(images_batch)
        results_dict = [result.to_dict(orient='records') for result in results.pandas().xyxy]

        # get dataset labels
        labels = dataset.labels
        labelMap = {}
        # map labelName to id
        for label in labels:
            labelMap[label.name] = label.id

        for index in range(len(unlabeled_images)):
            img_width, img_height = unlabeled_images[index].width, unlabeled_images[index].height
            for annotation in results_dict[index]:
                # 当前预测标注并不在数据集已有标签中
                logging.info(annotation['name'])
                if annotation['name'] not in labelMap:
                    continue
                unlabeled_images[index].labeled = True
                label_id = labelMap[annotation['name']]
                unlabeled_images[index].annotation_bboxes.append(
                    AnnotationBbox(
                        factorX=annotation['xmin'] / img_width,
                        factorY=annotation['ymin'] / img_height,
                        factorWidth=(annotation['xmax'] - annotation['xmin']) / img_width,
                        factorHeight=(annotation['ymax'] - annotation['ymin']) / img_height,
                        dataset_label_id=label_id
                    )
                )
    finally:
        dataset.status = 'None'
        db.session.commit()
