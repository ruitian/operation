# -*- coding: utf-8 -*-
from urllib import urlencode

from flask import request

def to_pagination_with_next_url(offset, limit, total):
    if  total <= offset + limit:
        next_url = None
    else:
        params = dict(request.args)
        params['offset'] = offset + limit
        params['limit'] = limit
        next_url = '{}?{}'.format(request.base_url,
                                  urlencode(params))
    return dict(next_url=next_url)