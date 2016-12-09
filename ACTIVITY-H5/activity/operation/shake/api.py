# -*- coding: utf-8 -*-
from flask import request, current_app, json, make_response

from ..base_operation import activity
from .. import BaseAction, RETStatus
from .service import ShakeService

@activity.route('/check_token', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        token = request.form['token']
    else:
        token = request.args.get('token')
    resp = BaseAction.check_token(token)
    print resp
    print token
    # 验证token
    if BaseAction.check_token(token) is None:
        return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
    return resp


@activity.route('/shake', methods=['GET', 'POST'])
def shake():
    return 'hello'


@activity.route('/shake/static', methods=['GET', 'POST'])
def get_shake_static_data():
    shake_service = ShakeService()
    if type(_get_param()) == tuple:
        return _get_param()
    activity_id, uid, token = _get_param()
    # 获取静态数据
    static_resp = shake_service.get_static_data(activity_id, uid)
    static_resp = json.loads(static_resp)
    if 'none' in static_resp and static_resp['none'] is True:
        if static_resp['type'] == 1:
            return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY)
        if static_resp['type'] == 2:
            return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY)
    resp = make_response(BaseAction.jsonify_with_data(static_resp))
    resp.set_cookie('token', token)
    return resp


@activity.route('/shake/play', methods=['GET', 'POST'])
def shake_play():
    shake_service = ShakeService()
    if type(_get_param()) == tuple:
        return _get_param()
    activity_id, uid, token = _get_param()
    # 获取抽奖结果
    play_resp = shake_service.shake_play(activity_id, uid)
    return BaseAction.jsonify_with_data(play_resp)


@activity.route('/shake/my', methods=['GET', 'POST'])
def get_my_prize():
    shake_service = ShakeService()
    if type(_get_param()) == tuple:
        return _get_param()
    activity_id, uid, token = _get_param()
    my_prize = shake_service.get_my_prize(activity_id, uid)
    if my_prize is None:
        return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY)
    return BaseAction.jsonify_with_data(my_prize)

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
        else:
            if len(request.args) != 2:
                return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
            activity_id = request.args.get('activity_id')
            token = request.args.get('token')

    # cookie中含有token只获取activity_id
    else:
        if request.method == "POST":
            activity_id = request.form['activity_id']
        else:
            activity_id = request.args.get('activity_id')
    # 验证token
    user_info = BaseAction.check_token(token)
    if user_info is None:
        return BaseAction.jsonify_with_data('', RETStatus.TOKEN_ERROR)
    # 解析token后，获取uid
    uid = user_info['useraccount']['uid']
    # 验证参数中的值是否为空
    if len(activity_id) == 0 or len(token) == 0:
        return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
    return [activity_id, uid, token]