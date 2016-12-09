# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
from flask import current_app, jsonify, json

from ..common import APIStatus, RETStatus


class BaseAction(object):

    @staticmethod
    def check_token(token=None):
        start_time = time.time()
        urllib2_log = current_app.config['LOG_FILE'] + 'urllib2.log'

        data = urllib.urlencode({
            'token': token
        })
        try:
            url = current_app.config['SERVICE_URL'] + '/account/user/tokenlogin'
            resp = json.loads(urllib2.urlopen(url, data=data, timeout=15).read())
            # 请求时间

        except Exception, e:
            process_time = time.time() - start_time
            with open(urllib2_log, 'a') as f:
                f.write(str(time.ctime()) + ' ' + url + ' ' + str(process_time) +' ' + str(e) +'\n')
        else:
            process_time = time.time() - start_time
            with open(urllib2_log, 'a') as f:
                f.write(str(time.ctime()) + ' ' + url + ' ' + str(process_time) + '\n')
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
