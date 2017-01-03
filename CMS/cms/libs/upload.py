# -*- coding: utf-8 -*-
from flask import current_app as app, json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

import random
import os
import urllib2

UPLOAD_URI = '/res/img/upload?scene=common'

def upload_file(file):
    if file and allow_file(file.filename):
        file_type = file.filename.rsplit('.', 1)[1]
        file.filename = '{0}.{1}'.format(
            str(random.randint(6, 1000000)), file_type
        )
        file_url = os.path.join(
            app.config['TEMP_DIR'], file_type
        )
        # 保存文件
        file.save(file_url)
        # 上传文件到阿里云
        register_openers()
        datagen, headers = multipart_encode({"fileUp": open(file_url, 'rb')})
        url = '{0}{1}'.format(app.config['SERVICE_URL'], UPLOAD_URI)
        request = urllib2.Request(
            url,
            datagen, headers)
        # 判断返回值
        resp = json.loads(urllib2.urlopen(request).read())
        if resp['ret'] == 0:
            return resp['content'], resp['timestamp'], file_url
        return None
    return None


def allow_file(self, filename):
    return '.' in filename and filename.rsplit('.', 1)[1] \
                               in app.config['ALLOWED_EXTENSIONS']