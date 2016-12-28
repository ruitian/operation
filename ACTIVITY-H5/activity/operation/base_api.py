# -*- coding: utf-8 -*-
import os
from .base_operation import _get_param
from .shake import get_shake_static_data
from .sku import get_sku_static_data
from .. import BaseAction, APIStatus, RETStatus

from .base_operation import activity
from flask import current_app as app, render_template, json


@activity.route('/')
def index():
    return render_template('index.html')


@activity.errorhandler(400)
def bad_request(error):
    return BaseAction.jsonify_with_data(error, RETStatus.EXPIRE, APIStatus.BAD_REQUEST)


@activity.errorhandler(404)
def not_found(error):
    return BaseAction.jsonify_with_data(error, RETStatus.EXPIRE, APIStatus.NOT_FOUND)

# 活动的通用入口
@activity.route('/static', methods=['GET', 'POST'])
def common_static_info():
    params = _get_param()
    if type(params) == tuple:
        return params
    activity_id, uid, token = params
    file_folder = app.config['DATA_JSON'] + activity_id
    if os.path.exists(file_folder):
        with open(file_folder + '/data.json') as static_file:
            data = json.load(static_file)

        # 摇一摇活动
        if data['dispath'] == 'shake':
            return get_shake_static_data()
        if data['dispath'] == 'sku':
            return get_sku_static_data()
    else:
        return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY)