# -*- coding: utf-8 -*-
from cms.extensions import db

__all__ = ['NoticeModel']


class NoticeModel(db.Model):

    __tablename__ = 'cms_notice'
    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.String(64), index=True, unique=True)
    img_url = db.Column(db.String(128))
    name = db.Column(db.String(128), default=None, index=True)
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

    def to_dict(self):
        return dict(
            id=self.id,
            img_id=self.img_id,
            img_url=self.img_url,
            name=self.name
        )
