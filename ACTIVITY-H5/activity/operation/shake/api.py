# -*- coding: utf-8 -*-
from flask import request, json, make_response

from ..base_operation import activity
from .. import BaseAction, RETStatus
from .service import ShakeService
from ..base_operation import _check_params


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
        return BaseAction.jsonify_with_data('', 1221, RETStatus.PARMA_ERROR)
    return resp


@activity.route('/shake/static', methods=['GET', 'POST'])
def get_shake_static_data(params):
    shake_service = ShakeService()
    activity_id, uid, token = params
    # 获取静态数据
    static_resp, timestamp = shake_service.get_static_data(activity_id, uid)
    static_resp = json.loads(static_resp)
    if 'none' in static_resp and static_resp['none'] is True:
        if static_resp['type'] == 1:
            return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY)
        if static_resp['type'] == 2:
            return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY)
    resp = make_response(BaseAction.jsonify_with_data(static_resp, timestamp=timestamp))
    if token is not None:
        resp.set_cookie('token', token)
    return resp


@activity.route('/shake/play', methods=['GET', 'POST'])
def shake_play():
    shake_service = ShakeService()
    if type(_check_params()) == tuple:
        return _check_params()
    activity_id, uid, token = _check_params()
    # 获取抽奖结果
   
    play_resp, timestamp = shake_service.shake_play(activity_id, uid)
    return BaseAction.jsonify_with_data(play_resp, timestamp=timestamp)

@activity.route('/shake/my', methods=['GET', 'POST'])
def get_my_prize():
    shake_service = ShakeService()
    if type(_check_params()) == tuple:
        return _check_params()
    activity_id, uid, token = _check_params()
    my_prize, timestamp = shake_service.get_my_prize(activity_id, uid)
    if my_prize is None:
        return BaseAction.jsonify_with_data('', RETStatus.NO_ACTIVITY, timestamp=timestamp)
    return BaseAction.jsonify_with_data(my_prize, timestamp=timestamp)

