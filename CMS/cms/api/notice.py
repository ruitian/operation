# -*- coding: utf-8 -*-
from . import bp

from flask import request
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import os
import urllib2
import base64
import random

@bp.route('/notice/upload', methods=['GET', 'POST'])
def upload_img():
    pass

def request_upload():
    with open('a.txt', 'r') as data:
        text = data.read()

    split_text = text.split(';')
    file_type = split_text[0].split('/')[1]
    file_name = '.'.join([str(random.randint(6, 1000000)), file_type])

    image_text = split_text[1].split(',')[1]
    img_data = base64.b64decode(image_text)

    file = open(file_name, 'wb')
    file.write(img_data)
    file.close()

    register_openers()
    datagen, headers = multipart_encode({"fileUp": open(file_name, 'rb')})

    request = urllib2.Request(
        "http://zs.market-api.wmdev2.lsh123.com/res/img/upload?scene=common",
        datagen, headers)
    os.remove(file_name)

    print urllib2.urlopen(request).read()
