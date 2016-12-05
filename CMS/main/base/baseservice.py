# -*- coding: utf-8 -*-
import urllib2
from flask import current_app, jsonify, json

from ..common import APIStatus, RETStatus


class BaseService(object):

    @staticmethod
    def check_token(token=None):
        try:
            url = current_app.config['SERVICE_URL'] + '/account/user/tokenlogin'
            resp = json.loads(urllib2.urlopen(url, data=token, timeout=15, ).read())
        except Exception, e:
            print str(e)
        else:
            return BaseService.jsonify_with_data(RETStatus.OK, resp)

    @staticmethod
    def verify_param(param=None):
        if param is not None:
            if type(param) == dict or type(param) == list or type(param) == tuple:
                def callback(cb):
                    return cb(param)
                return callback
            else:
                return BaseService.jsonify_with_data(RETStatus.PARMA_ERROR, '')
        else:
            return BaseService.jsonify_with_data(RETStatus.PARMA_ERROR, '')

    @staticmethod
    def jsonify_with_data(ret, args, status=None):
        resp = {'content': args, 'msg': ret[1], 'ret': ret[0]}
        if status is None:
            status = APIStatus.OK
        return jsonify(resp), status[0]
