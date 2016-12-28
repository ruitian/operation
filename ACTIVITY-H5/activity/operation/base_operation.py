# -*- coding: utf-8 -*-
import base64
import os
from flask import (
    Blueprint, request)

from .. import BaseAction, RETStatus, redis


__all__ = ['activity']

activity = Blueprint('activity', __name__)


def _get_param():
    # 在cookie中获取token
    token = request.cookies.get('token')
    # 判断cookie是否含有token
    if token is None:
        if request.method == 'POST':
            # 验证请求参数的个数
            if len(request.form) != 2:
                return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
            activity_id = request.form['activity_id']
            token = request.form['token']
            # 验证参数是否为空
            if len(token) == 0:
                return BaseAction.jsonify_with_data('', RETStatus.TOKEN_NONE)
            if len(activity_id) == 0:
                return BaseAction.jsonify_with_data('', RETStatus.ACTIVITY_NONE)

        else:
            if len(request.args) != 2:
                return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
            activity_id = request.args.get('activity_id')
            token = request.args.get('token')
            # 验证参数是否为空
            if len(token) == 0:
                return BaseAction.jsonify_with_data('', RETStatus.TOKEN_NONE)
            if len(activity_id) == 0:
                return BaseAction.jsonify_with_data('', RETStatus.ACTIVITY_NONE)


    # cookie中含有token只获取activity_id
    else:
        if request.method == "POST":
            activity_id = request.form['activity_id']
            # 验证活动id是否为空
            if len(activity_id) == 0:
                return BaseAction.jsonify_with_data('', RETStatus.ACTIVITY_NONE)
        else:
            activity_id = request.args.get('activity_id')
            # 验证活动id是否为空
            if len(activity_id) == 0:
                return BaseAction.jsonify_with_data('', RETStatus.ACTIVITY_NONE)

    # 验证参数中的值是否为空
    if len(activity_id) == 0 or len(token) == 0:
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
