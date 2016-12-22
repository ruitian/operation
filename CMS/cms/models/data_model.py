# -*- coding: utf-8 -*-
from cms.extensions import db


class ChannelModel(db.Model):
    '''
    频道表
    '''

    __tablename__ = 'cms_channel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
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


class CategoryModel(db.Model):
    '''
    目录表
    '''

    __tablename__ = 'cms_category'

    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer)
    name = db.Column(db.String(128), index=True)
    # 0 => 公告
    # 1 => 大转盘
    # 2 => 摇一摇
    # 99 => 通用
    type = db.Column(db.Integer, default=0)
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


class DetailModel(db.Model):
    '''
    json数据表
    '''
    __tablename__ = 'cms_detail'

    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer)
    content = db.Column(db.Text)
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
