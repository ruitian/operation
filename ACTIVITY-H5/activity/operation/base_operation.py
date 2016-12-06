# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from .. import BaseAction, APIStatus, RETStatus

__all__ = ['activity']

activity = Blueprint('activity', __name__)


# 加载活动主页
@activity.route('/')
def index():
    return render_template('index.html')


@activity.errorhandler(400)
def bad_request(error):
    return BaseAction.jsonify_with_data(error, RETStatus.EXPIRE, APIStatus.BAD_REQUEST)


@activity.errorhandler(404)
def not_found(error):
    return BaseAction.jsonify_with_data(error, RETStatus.EXPIRE, APIStatus.NOT_FOUND)
