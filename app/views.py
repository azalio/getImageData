# -*- coding: utf-8 -*-
import os
import random
import uuid

import requests
from PIL import Image
from flask import send_file, redirect, url_for
from resizeimage import resizeimage

from app import app
from app.decorators import async
from config import IMAGE_RESIZE_DIR, IMAGE_UPLOAD_DIR


@async
def get_new_image():
    url = 'http://lorempixel.com/800/800/'
    image_path = "{}/{}".format(IMAGE_UPLOAD_DIR, str(uuid.uuid4()))
    req = requests.get(url, stream=True)
    try:
        if req.status_code == 200:
            with open(image_path, 'wb') as f:
                for chunk in req.iter_content(1024):
                    f.write(chunk)
    except Exception:
        pass


def resize_image(filepath, width, height):
    with open(filepath, 'r+b') as fp:
        with Image.open(fp) as image:
            filepath = IMAGE_RESIZE_DIR + "/{}_{}_{}".format(os.path.basename(filepath), width, height)
            thumbnail = resizeimage.resize_thumbnail(image, [width, height])
            thumbnail.save(filepath, image.format)


@app.route('/image/<image_hash>/<int:width>/<int:height>/')
def image(image_hash="test", width=100, height=100):
    filepath = "{}/{}_{}_{}".format(IMAGE_RESIZE_DIR, image_hash, width, height)
    filepath_orig = "{}/{}".format(IMAGE_UPLOAD_DIR, image_hash)
    if os.path.isfile(filepath):
        """If image exist just send file"""
        return send_file("../" + filepath)
    elif os.path.isfile(filepath_orig):
        """If orig path exists - resize and redirect"""
        resize_image(filepath_orig, width, height)
        return redirect(url_for('image', image_hash=image_hash, width=width, height=height, _external=True))
    else:
        """If the path doesn't exist - send any image and download new for future use."""
        image_name = "{}/{}".format(IMAGE_UPLOAD_DIR, random.choice(os.listdir(IMAGE_UPLOAD_DIR)))
        link_filepath = "{}/{}".format(IMAGE_UPLOAD_DIR, image_hash)
        os.link(image_name, link_filepath)
        get_new_image()
        return redirect(url_for('image', image_hash=image_hash, width=width, height=height, _external=True))
