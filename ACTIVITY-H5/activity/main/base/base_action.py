# -*- coding: utf-8 -*-
import urllib2
import urllib
from flask import current_app, jsonify, json

from ..common import APIStatus, RETStatus


class BaseAction(object):

    @staticmethod
    def check_token(token=None):
        data = urllib.urlencode({
            'token': token
        })
        try:
            url = current_app.config['SERVICE_URL'] + '/account/user/tokenlogin'
            resp = json.loads(urllib2.urlopen(url, data=data, timeout=15).read())
        except Exception, e:
            print str(e)
        else:
            if resp['ret'] != 0:
                return None
            return resp['content']

    @staticmethod
    def check_param(param=None):
        if param is not None:
            if type(param) == dict or type(param) == list or type(param) == tuple:
                def callback(cb):
                    return cb(param)
                return callback
            else:
                return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)
        else:
            return BaseAction.jsonify_with_data('', RETStatus.PARMA_ERROR)

    @staticmethod
    def jsonify_with_data(args, ret=None, status=None):
        if ret is None:
            ret = RETStatus.OK
        if status is None:
            status = APIStatus.OK
        resp = {'content': args, 'msg': ret[1], 'ret': ret[0]}
        return jsonify(resp), status[0]
