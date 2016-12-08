# -*- coding: utf-8 -*-
from flask import current_app as app, jsonify, json
import urllib2
import os
import time
import random
__all__ = ['ShakeService']

# 获取抽奖次数的url
SHAKE_NUM_URL = '/Operate/prize/getusershakeinfo'

# 获取抽奖接口的url
SHAKE_PLAY_URL= '/Operate/prize/shake'

# 获取我的奖品的url
SHAKE_MY_PRIZE_URL = '/'

# 转义
true = True
false = False


class ShakeService(object):

    def get_static_data(self, activity_id, uid):
        file_folder = app.config['DATA_JSON']+activity_id
        if os.path.exists(file_folder):
            with open(file_folder+'/data.json') as static_file:
                data = json.load(static_file)
            # 添加一些额外的信息
            user_draw_info = self.get_user_draw_info(activity_id, uid)
            if user_draw_info['activity'] == 'yes':
                data['user_info'] = {
                    "today_times": user_draw_info['today_shake_times'],
                    "name": user_draw_info['name'],
                    "zone_id": user_draw_info['zone_id']
                }
                return json.dumps(data)
            else:
                return json.dumps({
                    'type': 2,
                    'none': True
                })
        else:
            return json.dumps({
                'type': 1,
                'none': True
            })

    def get_user_draw_info(self, activity_id, uid):

        url = app.config['SERVICE_URL'] + SHAKE_NUM_URL + \
              '?activity_id=%s&uid=%s' % (activity_id, uid)
        return self._request_url(url)

    def shake_play(self, activity_id, uid):

        url = app.config['SERVICE_URL'] + SHAKE_PLAY_URL +\
              '?activity_id=%s&uid=%s' % (activity_id, uid)
        resp = self._request_url(url)
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

    def _request_url(self, url):
        a = random.randint(1, 10)
        with open(app.config['LOG_FILE'] + 'test.log', 'a') as f:
            f.write('开始请求' + str(a) + ' ' + str(time.ctime()) + '\n')
        try:
            resp = json.loads(urllib2.urlopen(url, timeout=15).read())
        except Exception, e:
            print str(e)
        else:
            with open(app.config['LOG_FILE'] + 'test.log', 'a') as f:
                f.write('结束请求' + str(a) + ' ' + str(time.ctime()) + '\n')
            if resp['ret'] != 0:
                return None
            else:
                return resp['content']
