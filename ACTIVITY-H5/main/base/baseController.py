# -*- coding: utf-8 -*-
from flask import current_app, json
import urllib2
from main.common.api import bp

class BaseController:

    @bp.route('/check_token')
    def check_token(token):
        # account / user / tokenlogin
        try:
            url = current_app.config['SERVICE_URL'] + 'account/user/tokenlogin'
            resp = json.loads(urllib2.urlopen(url, data=token, timeout=15, ).read())
        except Exception, e:
            print str(e)
        else:
            return resp