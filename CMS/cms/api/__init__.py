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
    REQUEST_TIME_OUT = (1001, '网络请求超时')
    PASSWD_ERROR = (1000, '密码错误')
    UPLOAD_FAILE = (-1000, '上传失败')

def jsonify_with_data(args, ret=None, status=None, timestamp=None, paging=None):
    if ret is None:
        ret = RETStatus.OK
    if status is None:
        status = APIStatus.OK
    if paging is None:
        resp = {'content': args, 'msg': ret[1], 'ret': ret[0], 'timestamp': timestamp}
    if paging is not None:
        resp = {'content': args, 'paging': paging, 'msg': ret[1], 'ret': ret[0], 'timestamp': timestamp}
    return jsonify(resp), status[0]


from .operation import *
from .notice import *
