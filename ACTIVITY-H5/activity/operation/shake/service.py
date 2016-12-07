# -*- coding: utf-8 -*-
from flask import current_app as app, jsonify, json
import urllib, urllib2
import os
__all__ = ['ShakeService']

# 获取抽奖次数的url
SHAKE_NUM_URL = '/Operate/prize/getUserDrawInfos'

# 获取抽奖接口的url
SHAKE_PLAY_URL= '/Operate/prize/shake'

# 获取我的奖品的url
SHAKE_MY_PRIZE_URL = '/'

# 转义
true = True
false = False


class ShakeService(object):

    # def __init__(self, shake_num_url, shake_play_url, shake_my_prize_url):
    #
    #     # 获取抽奖次数的url
    #     self.shake_num_url = shake_num_url
    #
    #     # 获取抽奖接口的url
    #     self.shake_play_url = shake_play_url
    #
    #     # 获取我的奖品的url
    #     self.shake_my_prize_url = shake_my_prize_url

    def get_static_data(self, activity_id, uid):
        file_folder = app.config['DATA_JSON']+activity_id
        if os.path.exists(file_folder):
            with open(file_folder+'/data.json') as static_file:
                data = json.load(static_file)
            # 添加一些额外的信息
            user_draw_info = self.get_user_draw_info(activity_id, uid)
            data['today_times'] = user_draw_info['today_times']
            data['all_times'] = user_draw_info['all_times']
            data['name'] = user_draw_info['name']
            return json.dumps(data)
        else:
            return json.dumps({
                'type': 1,
                "none": True
            })

    def get_user_draw_info(self, activity_id, uid):
        data = urllib.urlencode({
            'uid': uid,
            'activity_id': activity_id
        })
        url = app.config['SERVICE_URL'] + SHAKE_NUM_URL
        return self._request_url(url, data)

    def shake_play(self, activity_id, uid):
        data = urllib.urlencode({
            'uid': uid,
            'activity_id': activity_id
        })
        url = app.config['SERVICE_URL'] + SHAKE_PLAY_URL
        resp = self._request_url(url, data)
        if resp['got']:
            type = resp['prize']['type']
            item = resp['prize']['item']
            # 从静态数据中读取奖品信息
            file_folder = app.config['DATA_JSON'] + activity_id
            with open(file_folder + '/data.json') as static_file:
                static_data = json.load(static_file)
            prizes = static_data['prize']
            for prize in prizes:
                if prize['type'] == type and prize['item'] == item:
                    break
            prize_info = {
                'got': 1,
                'name': prize['name'],
                'pic': prize['pic'],
                'desc': prize['desc']
            }
            return prize_info
        prize_info = {
            'got': 2,
        }
        return prize_info

    def _request_url(self, url, data):
        try:
            resp = json.loads(urllib2.urlopen(url, data=data, timeout=15).read())
        except Exception, e:
            print str(e)
        else:
            if resp['ret'] != 0:
                return None
            else:
                return resp['content']
