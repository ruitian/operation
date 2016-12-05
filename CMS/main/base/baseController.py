# # -*- coding: utf-8 -*-
# from flask import current_app, request, jsonify, json
# from main.common.api import bp
# from main.common.api import APIStatus, RETStatus
#
# import time
# import urllib2
#
# class BaseController:
#
#     @staticmethod
#     def check_token(token=None):
#         try:
#             url = current_app.config['SERVICE_URL'] + 'account/user/tokenlogin'
#             resp = json.loads(urllib2.urlopen(url, data=token, timeout=15, ).read())
#         except Exception, e:
#             print str(e)
#         else:
#             return resp
#
#     @staticmethod
#     def check_parma(parma=None):
#         if parma is not None:
#             if type(parma) == dict or type(parma) == list or type(parma) == tuple:
#                 return
#         return BaseController.back(
#             RETStatus.PARMA_ERROR[0],
#             None,
#             RETStatus.PARMA_ERROR[1])
#
#     @staticmethod
#     def verify_parma(param):
#         if param is None:
#             return None
#         def callback(func):
#             func(param)
#             return func
#         return callback
#
#     @staticmethod
#     def back(ret, args=None, msg=None):
#
#         resp = {
#             'content': args,
#             'msg': msg,
#             'ret': ret,
#             'timestamp' : int(time.time())
#             }
#         return jsonify(resp)
