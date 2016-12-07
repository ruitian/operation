# -*- coding: utf-8 -*-
class APIStatus:
    def __init__(self):
        pass

    OK = (200, 'OK')
    BAD_REQUEST = (400, 'Bad_request')
    UNAUTHORIZED = (401, 'Unauthorized')
    NOT_FOUND = (404, 'Not_found')
    FORBIDDEN = (403, 'Forbidden')


class RETStatus:
    def __init__(self):
        pass

    OK = (0, '')
    TIME_OUT = (1000, '请求超时，请稍后重试')
    REQUEST_TIME_OUT = (1001, '网络请求超时')
    PARMA_ERROR = (1002, '参数错误')

    DRAW_PLAY_NUMBER = (2000, '今天的抽奖次数已用完')
    FORGET_PARAM = (2001, '又漏什么参数了?')
    EXPIRE = (2002, '项目已下线')
    NO_ACTIVITY = (2003, '没有该活动!')
    TOKEN_ERROR = (2004, 'token验证失败')
