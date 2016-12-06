# -*- coding: utf-8 -*-
from flask import request

from ..base_operation import activity
from .. import BaseAction


@activity.route('/check_token')
def check():
    token = request.args.get('token')
    resp = BaseAction.check_token(token)
    return resp