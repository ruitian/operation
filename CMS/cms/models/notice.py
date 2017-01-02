# -*- coding: utf-8 -*-
from cms.extensions import db

__all__ = ['NoticeModel']


class NoticeModel(db.Model):

    __tablename__ = 'cms_notice'
    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.String(64))
    img_url = db.Column(db.String(128))
    name = db.Column(db.String(128), default=None)
    create_at = db.Column(
        db.TIMESTAMP,
        index=True,
        server_default=db.func.current_timestamp()
    )
    update_at = db.Column(
        db.TIMESTAMP,
        index=True,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return '<%s >' % self.name
