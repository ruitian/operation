# -*- coding: utf-8 -*-
import os
from flask import current_app as app, json

from cms.models import NoticeModel
from cms.extensions import db
from cms.libs.upload import upload_file

__all__ = ['NoticeService']


class NoticeService(object):

    def upload_img(self, pic):
        content, timestamp, file_url = upload_file(pic)
        if content is None:
            return None
        else:
            img_id = content['id']
            img_url = content['origin']
            self.save_data(img_id, img_url)
            # 删除临时文件
            os.remove(file_url)
            return content, timestamp

    def save_data(self, img_id, img_url):
        notice = NoticeModel(
            img_id=img_id,
            img_url=img_url,
        )
        try:
            db.session.add(notice)
            db.session.commit()
        except:
            db.session.rollback()
        else:
            return True

    def get_notice_list(self, offset, limit):
        notices = (NoticeModel.query.order_by(
            NoticeModel.create_at.desc()).offset(offset).limit(limit).all())
        return [notice.to_dict()for notice in notices]

    def count_all(self):
        return NoticeModel.query.count()

    def update_notice(self, name, img_id):
        notice = NoticeModel.query.filter_by(img_id=img_id).first()
        if notice is None:
            return None
        else:
            notice.name = name
            db.session.add(notice)
            db.session.commit()
            return True