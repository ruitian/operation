# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import jsonify

bp = Blueprint('api', __name__)


class APIStatus:
    OK = (200, 'OK')
    BAD_REQUEST = (400, 'Bad_request')
    UNAUTHORIZED = (401, 'Unauthorized')
    NOT_FOUND = (404, 'Not_found')
    FORBIDDEN = (403, 'Forbidden')


class RETStatus:
    OK = (0, '')
    TIME_OUT = (1, '请求超时，请稍后重试')
    REQUEST_TIME_OUT = (1, '网络请求超时')
    DRAW_PLAY_NUMBER = (0, '今天的抽奖次数已用完')
    FORGET_PARAM = (3, '又漏什么参数了?')
    EXPIRE = (-1, '项目已下线')
    NO_ACTIVITY = (-1, '没有该活动!')

def jsonify_with_data(ret, args, status):
    resp = {'content': args, 'msg': ret[1], 'ret': ret[0]}
    return jsonify(resp), status[0]

def jsonify_with_error(status, error=None):
    resp = {'msg': status[1], 'ret': status[0]}
    if error:
        resp['error'] = error
    return jsonify(resp)

@bp.errorhandler(400)
def bad_request(error):
    return jsonify_with_error(APIStatus.BAD_REQUEST)


@bp.errorhandler(404)
def not_found(error):
    return jsonify_with_error(APIStatus.NOT_FOUND)

from .operation import *
