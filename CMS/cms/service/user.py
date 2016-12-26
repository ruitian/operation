# -*- coding: utf-8 -*-
from flask import current_app as app

from . import BaseService

__all__ = ['UserService']
LOGIN_URI = '/account/user/login'


class UserService(object):

    def login(self, account, pwd):
        url = app.config['SERVICE_URL'] + LOGIN_URI + '?account=%s&pwd=%s' % (account, pwd)
        print url
        resp = BaseService.request_url(url)
        return resp

