# -*- coding: utf-8 -*-
from flask import current_app as app, json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import os
import urllib2
import base64
import random

from cms.models import NoticeModel
from cms.extensions import db

__all__ = ['NoticeService']


class NoticeService(object):

    upload_uri = '/res/img/upload?scene=common'
    def request_upload(self, text):
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

        url = '{0}{1}'.format(app.config['SERVICE_URL'], self.upload_uri)
        request = urllib2.Request(
            url,
            datagen, headers)
        # 删除图片
        os.remove(file_name)
        resp = json.loads(urllib2.urlopen(request).read())

        img_id = resp['content']['id']
        img_url = resp['content']['origin']

        self.save_data(img_id, img_url)

        if resp['ret'] == 0:
            return resp['content'], resp['timestamp']
        return None

    def save_data(self, img_id, img_url, img_name=None):
        notice = NoticeModel(
            img_id=img_id,
            img_url=img_url,
            name=img_name
        )
        try:
            db.session.add(notice)
            db.session.commit()
        except:
            db.session.rollback()
        else:
            return True

    def get_notice_list(self, offset, limit):
        notices = (NoticeModel.query.order_by(NoticeModel.create_at.desc())\
            .all().offset(offset).limit(limit))
        return [notice.to_dict for notice in notices]