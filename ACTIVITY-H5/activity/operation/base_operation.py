# -*- coding: utf-8 -*-
import base64
import os
from flask import (
    Blueprint, request, current_app as app, json)

from .. import BaseAction, RETStatus, redis


__all__ = ['activity']

activity = Blueprint('activity', __name__)
false = False
true = True

# 根据配置确定此活动是否需要用户登录
def _is_user_login(file_folder):

    with open(file_folder+'/data.json') as static_data:
        data = json.load(static_data)
        extend = data['extend']
        return extend['needLogin'], extend['checkZone']

def _check_params():

    if request.method == 'POST':
        if not request.form.has_key('activity_id'):
            return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
        activity_id = request.form['activity_id']
    else:
        if not request.args.has_key('activity_id'):
            return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
        activity_id = request.args.get('activity_id')
    # 判断是否有这个活动
    file_folder = app.config['DATA_JSON'] + activity_id
    if not os.path.exists(file_folder):
        return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY)
    is_login_user, is_check_zone = _is_user_login(file_folder)

    # 需要用户登录，继续验证token
    token = request.cookies.get('token')
    # cookie 没有token
    if not is_login_user:
        return [activity_id, None, None]

    elif is_login_user and token is None:
        if request.method == 'POST':
            if not request.form.has_key('token'):
                return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
            token = request.form['token']
        else:
            if not request.args.has_key('token'):
                return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
            token = request.args.get('token')
    # cookie 含有token
    elif is_login_user and token is not None:
        if len(token) == 0:
            return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)

    # 查找缓存中是否有用户信息数据
    token_base64 = base64.b64encode(token)
    uid = redis.hget(token_base64, 'user_info')
    if uid is None:
        # 验证token
        user_info = BaseAction.check_token(token)
        if user_info is None:
            return BaseAction.jsonify_with_data('', RETStatus.TOKEN_ERROR)
        # 解析token后，获取uid
        if type(user_info) != dict:
            raise 'user_info Type Error'
        uid = user_info['useraccount']['uid']
        # 将uid写入缓存，缓存过期时间为3天
        redis.hset(token_base64, 'user_info', uid)
        redis.expire(token_base64, 259200)
    return [activity_id, uid, token]
