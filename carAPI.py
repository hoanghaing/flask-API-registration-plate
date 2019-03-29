from flask import Flask, request, url_for, abort, make_response, jsonify
from flask_api import FlaskAPI, status, exceptions
from PIL import Image
import numpy as np
import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = FlaskAPI(__name__)

gioi_han_req = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["150 per day","40 per hour"]
)
ALLOWED_EXTENSION = set(['jpg', 'png', 'jpeg'])

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
#Xu li loi
@app.errorhandler(400)
def authentication_error(error):
    return make_response(jsonify({'error': 'Loi xac thuc, khong ton tai user_key'}), 400)

@app.errorhandler(401)
def file_format_error(error):
    return make_response(jsonify({'error': 'Upload file khong thanh cong, dinh danh file khong phu hop!'}), 401)
@app.errorhandler(411)
def size_error(error):
    return make_response(jsonify({'error': 'Kich thuoc cua file qua lon, vuot qua gioi han 544 * 544'}))

@app.errorhandler(429)
def limit_error(error):
    return make_response(jsonify({'error': 'Toi da 60 req 1 phut!'}), 429)

@app.route("/anpr/v1", methods=['POST'])
@gioi_han_req.limit("60 per minute")
def create_task():
    sample = 'hoanghai123'
    userKey = request.headers.get('user_key')
    if not (userKey == sample):
        abort(400)

    #Kiem tra format cua file
    imagePath = request.files['image']
    image = imagePath.filename

    if (allowed_file(image)):
        abort(401)

    #Kiem tra kich co file anh
    try:
        imgfile = Image.open(imagePath)
    except:
        abort(404)

    chieurong, chieudai = imgfile.size
    if(chieudai > 544 or chieurong > 544):
        abort(411)


if __name__ == "__main__":
    app.run(debug=True)