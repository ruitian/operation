# -*- coding: utf-8 -*-
import hmac
from flask import request
from flask import current_app as app
from hashlib import sha512

from . import bp, jsonify_with_data, RETStatus

from cms.service import UserService

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # print _create_indentifier()
    user_service = UserService()
    account = 'dongbingwei@lsh123.com'
    pwd = '123456'
    user, timestamp = user_service.login(account, pwd)
    uid = user['uid']
    username = user['name']
    user_account = user['useraccount']
    role_type = user['role_type']
    role_zone = user['role_zone']

    if user is None:
        return jsonify_with_data('', RETStatus.PASSWD_ERROR, timestamp=timestamp)
    return jsonify_with_data(user, timestamp=timestamp)

def login_user(user):
    pass

def _set_cookie(response):
    config = app.config
    cookie_name = config.get('REMEMBER_COOKIE_NAME', COOKIE_NAME)
    duration = config.get('REMEMBER_COOKIE_DURATION', COOKIE_DURATION)
    domain = config.get('REMEMBER_COOKIE_DOMAIN')
    path = config.get('REMEMBER_COOKIE_PATH', '/')

    secure = config('REMEMBER_COOKIE_SECURE', COOKIE_SECURE)

def _get_remote_addr():
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        address = address.encode('utf-8').split(b',')[0].strip()
    return address

def _create_indentifier():
    user_agent = request.headers.get('User-Agent')
    if user_agent is not None:
        user_agent = user_agent.encode('utf-8')
    base = '{0}|{1}'.format(_get_remote_addr(), user_agent)
    h = sha512()
    h.update(base.encode('utf8'))
    return h.hexdigest()

def encode_cookie(payload):
    return u'{0}|{1}'.format(payload, _cookie_digest(payload))

def decode_cookie(cookie):
    try:
        payload, digest = cookie.rsplit(u'|', 1)
        if hasatrr(digest, 'decode'):
            digest = digest.decode('ascii')
    except ValueError:
        return
    if safe_str_cmp(_cookie_digest(payload), digest):
        return payload

def _cookie_digest(payload, key=None):
    key = _secret_key(key)
    return hmac.new(key, payload.encode('utf-8'), sha512).hexdigest()

def _secret_key(key=None):
    if key == None:
        key = app.config['SECRET_KEY']
    return key

def safe_str_cmp(a, b):
    """This function compares strings in somewhat constant time.  This
    requires that the length of at least one string is known in advance.

    Returns `True` if the two strings are equal, or `False` if they are not.

    .. versionadded:: 0.7
    """
    if isinstance(a, text_type):
        a = a.encode('utf-8')
    if isinstance(b, text_type):
        b = b.encode('utf-8')

    if _builtin_safe_str_cmp is not None:
        return _builtin_safe_str_cmp(a, b)

    if len(a) != len(b):
        return False

    rv = 0
    if PY2:
        for x, y in izip(a, b):
            rv |= ord(x) ^ ord(y)
    else:
        for x, y in izip(a, b):
            rv |= x ^ y

    return rv == 0
