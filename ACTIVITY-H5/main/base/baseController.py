# -*- coding: utf-8 -*-
from flask import current_app, request, jsonify
from main.common.api import bp
from main.common.api import APIStatus, RETStatus

import time
import urllib2

class BaseController:

    @staticmethod
    def check_token(token=None):
        try:
            url = current_app.config['SERVICE_URL'] + 'account/user/tokenlogin'
            resp = json.loads(urllib2.urlopen(url, data=token, timeout=15, ).read())
        except Exception, e:
            print str(e)
        else:
            return resp

    @staticmethod
    def check_parma(self, parma=None):

        if parma is not None:
            if type(parma) == dict:
                pass
            elif type(parma) == list:
                pass
            elif type(parma) == tuple:
                pass
        
        return BaseController.back(RETStatus.PARMA_ERROR[0],
                                   None,
                                   RETStatus.PARMA_ERROR[2])

    @staticmethod
    def back(ret, args=None, msg=None):

        resp = {'content': args,
                'msg': msg,
                'ret': ret,
                'ts' : time.time()}
        return resp
