import logging
import os
import sys
import base64

from annotate.models import User
from annotate.extensions import db
import torch.hub
from io import BytesIO
from flask import Blueprint, request, current_app, jsonify
from annotate.models import Image
from time import sleep
from PIL import Image as PILImage

detection_bp = Blueprint('detection', __name__)


# @detection_bp.route('/<int:image_id>', methods=['POST'])
# def predict(image_id):
#     image_obj = Image.query.get(image_id)
#     model = torch.hub.load(current_app.config['YOLOV5_MODULE_FOLDER'],
#                            'custom',
#                            path=os.path.join(current_app.config['YOLOV5_WEIGHTS_FOLDER'], 'best.pt'),
#                            source='local'
#                            )
#     if image_obj:
#         img_path = os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], image_obj.img_src)
#         try:
#             results = model(img_path, size=640)
#         finally:
#             pass
#         results_dict = results.pandas().xyxy[0].to_dict(orient='records')
#         for result in results_dict:
#             result['factorX'] = result['xmin'] / image_obj.width
#             result['factorY'] = result['ymin'] / image_obj.height
#             result['factorWidth'] = (result['xmax'] - result['xmin']) / image_obj.width
#             result['factorHeight'] = (result['ymax'] - result['ymin']) / image_obj.height
#         return jsonify(results_dict)


@detection_bp.route('/', methods=['POST'])
def predict_local_image():
    image = request.files.get('file')
    image_bytes = image.read()

    img = PILImage.open(BytesIO(image_bytes))
    model = torch.hub.load(current_app.config['YOLOV5_MODULE_FOLDER'],
                           'custom',
                           path=os.path.join(current_app.config['YOLOV5_WEIGHTS_FOLDER'], 'best.pt'),
                           source='local'
                           )
    results = model(img, size=640)
    results.render()  # updates results.imgs with boxes and labels
    image_base64_arr = []
    for im in results.imgs:
        buffered = BytesIO()
        im_base64 = PILImage.fromarray(im)
        im_base64.save(buffered, format="JPEG")
        image_base64_arr.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))
    return jsonify(image_base64_arr)


@detection_bp.route('/test', methods=['GET'])
def test():
    # print(sys.platform)
    # from acelery.tasks import add
    # add.delay()
    return "Success"
