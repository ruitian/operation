# -*- coding: utf-8 -*-
from flask import request, json, make_response

from ..base_operation import activity
from .. import BaseAction, RETStatus
from .service import SkuService
from ..base_operation import _get_param


@activity.route('/sku/static', methods=['GET', 'POST'])
def get_sku_static_data():
    shake_service = SkuService()
    # 参数异常返回
    params = _get_param()
    if type(params) == tuple:
        return params
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
    resp.set_cookie('token', token)
    return resp