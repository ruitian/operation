# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from ..main import BaseService, APIStatus, RETStatus

__all__ = ['activity']

activity = Blueprint('activity', __name__)


# 加载活动主页
@activity.route('/')
def index():
    return render_template('index.html')

@activity.errorhandler(400)
def bad_request(error):
    return BaseService.jsonify_with_data(RETStatus.EXPIRE, error, APIStatus.BAD_REQUEST)

@activity.errorhandler(404)
def not_found(error):
    return BaseService.jsonify_with_data(RETStatus.EXPIRE, error, APIStatus.NOT_FOUND)

# 导出活动路由
from turnplate import *  # noqa
from shake import *  # noqa