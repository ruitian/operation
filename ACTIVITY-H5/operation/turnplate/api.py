# -*- coding: utf-8 -*-
from flask import current_app, request, jsonify
import json

# from main.common.api import bp, jsonify_with_data, jsonify_with_error, \
#      APIStatus, RETStatus
from service import LuckyDrawService
from .. import activity
from .. import BaseService, APIStatus, RETStatus
@activity.route('/index')
def operation():
    a = ['a']
    resp = BaseService.verify_param(a)
    if hasattr(resp, '__call__'):
        return resp(get)
    return resp

@activity.route('/token')
def token():
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI5MzA2MDM5NzYzNTY4NTUyNzQiLCJjcmVhdGVkX2F0IjoxNDgwNjYyMDE2fQ.FSmm__ZupF8pK9fcpPG3S2AIJ0TUGKsbaorrXjXaj80'
    resp = BaseService.check_token(token)
    print resp
    return resp

def get(param):
    return BaseService.jsonify_with_data(RETStatus.OK, param)
# def number_to_func(arg):
#     switcher = {
#         '1': 'get_static_data',
#         '2': 'draw_prize',
#         '3': 'get_ranking',
#         '4': 'get_user_draw_info'
#     }
#     return switcher.get(arg)
#
# @bp.route('/operate', methods=['GET', 'POST'])
# def provide_req():
#     # 用户ID
#     uid = request.args.get('uid')
#     # 活动ID
#     activity_id = request.args.get('activity_id')
#     # 请求功能
#     # 1 => cms静态配置
#     # 2 => 抽奖结果
#     # 3 => 排行榜
#     action = request.args.get('action')
#     if uid is None or activity_id is None or action is None:
#         return jsonify_with_error(RETStatus.FORGET_PARAM)
#     else:
#         return eval(number_to_func(action))(activity_id, uid)
#
# # 静态数据 API
# @bp.route('/operate/prize/static/info', methods=['GET', 'POST'])
# def get_static_data(activity_id, uid):
#     resp = LuckyDrawService.get_static_data(
#         get_draw_url=current_app.config['ACTIVITY_INFO_URL'],
#         get_user_draw_url = '{0}?uid={1}&activity_id={2}'.format(
#             current_app.config['USER_DRAWINFO_URL'], uid, activity_id),
#             activity_id=activity_id
#     )
#     resp = json.loads(resp)
#     if resp.has_key('none') and resp['none'] is True:
#         if resp['type'] == 1:
#             return jsonify_with_error(RETStatus.NO_ACTIVITY)
#         elif resp['type'] == 2:
#             return jsonify_with_error(RETStatus.REQUEST_TIME_OUT)
#         elif resp['type'] == 3:
#             return jsonify_with_error(RETStatus.EXPIRE)
#     else:
#         return jsonify_with_data(RETStatus.OK, resp, APIStatus.OK)
# # 抽奖API
# @bp.route('/operate/prize/play')
# def draw_prize(activity_id, uid):
#     draw_url = '{0}?uid={1}&activity_id={2}'.format(
#         current_app.config['DRAW_URL'], uid, activity_id)
#     resp = LuckyDrawService.draw(draw_url)
#     if resp is not None and resp.has_key('draw'):
#         return jsonify_with_data(RETStatus.DRAW_PLAY_NUMBER, resp, APIStatus.OK)
#     elif resp is not None and resp.has_key('draw') is False:
#         return jsonify_with_data(RETStatus.OK, resp, APIStatus.OK)
#     return jsonify_with_error(RETStatus.TIME_OUT)
#
# # 排行榜 API
# @bp.route('/operate/prize/ranking')
# def get_ranking(activity_id, uid):
#     ranking_url = '{0}?activity_id={1}'.format(
#         current_app.config['RANKING_URL'], activity_id)
#     user_ranking_url = '{0}?activity_id={1}&uid={2}'.format(
#         current_app.config['USER_RANKING_URL'], activity_id, uid)
#     resp = LuckyDrawService.get_rank(
#         ranking_url=ranking_url,
#         user_ranking_url=user_ranking_url)
#     if resp is not None:
#         return jsonify_with_data(RETStatus.OK, resp, APIStatus.OK)
#     else:
#         return jsonify_with_error(RETStatus.REQUEST_TIME_OUT)
#
# # 单独获取用户抽奖信息
# @bp.route('/operate/prize/user')
# def get_user_draw_info(activity_id, uid):
#     user_info = {}
#     get_user_draw_url = '{0}?uid={1}&activity_id={2}'.format(
#         current_app.config['USER_DRAWINFO_URL'], uid, activity_id)
#     resp = LuckyDrawService.get_user_draw_info(get_user_draw_url)
#     if resp is not None:
#         user_info['all_times'] = resp['all_times']
#         user_info['today_times'] = resp['today_times']
#         user_info['score'] = resp['score']
#         return jsonify_with_data(RETStatus.OK, user_info, APIStatus.OK)
#     else:
#         return jsonify_with_error(RETStatus.OK)
