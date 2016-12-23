# -*- coding: utf-8 -*-
from flask import current_app as app, jsonify, json
import urllib2
import os
import time
import random
import pickle

from .. import redis
__all__ = ['ShakeService']

# 获取抽奖次数的url
SHAKE_NUM_URL = '/Operate/prize/getusershakeinfo'

# 获取抽奖接口的url
SHAKE_PLAY_URL= '/Operate/prize/shake'

# 获取我的奖品的url
SHAKE_MY_PRIZE_URL = '/Operate/prize/getUserDrawHistory'

# 获取中奖信息的url
SHAKE_Shake_Infos_URL = '/Operate/prize/getPrizeShakeInfos'

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
            # 用户抽奖的信息
            user_draw_info, timestamp = self.get_user_draw_info(activity_id, uid)
            if type(user_draw_info) != dict:
                raise 'user_draw_info Type Error'
            if user_draw_info['activity'] == 'yes':
                data['user_info'] = {
                    "today_times": user_draw_info['today_shake_times'],
                    "name": user_draw_info['name'],
                    "zone_id": user_draw_info['zone_id']
                }
                data['show_prizes'] = self._get_prize_shake_infos(activity_id)
                return json.dumps(data), timestamp
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
        resp, timestamp = self._request_url(url)
        print resp
        # got = 1 =>  抽到奖品
        # got = 2 =>  没有抽到奖品
        # got = 3 =>  根据draw返回信息
        if 'got' in resp and resp['got']:
            type = resp['prize']['type']
            item = resp['prize']['item']
            # 从静态数据中读取奖品信息
            file_folder = app.config['DATA_JSON'] + activity_id
            with open(file_folder + '/data.json') as static_file:
                static_data = json.load(static_file)
            prizes = static_data['prize']
            for prize in prizes:
                if prize['type'] == type and prize['item'] == item:
                    prize_info = {
                        'got': 1,
                        'name': prize['name'],
                        'pic': prize['pic'],
                        'desc': prize['desc']
                    }
                    return prize_info, timestamp
        elif 'draw' in resp and resp['draw'] == 2:
            prize_info = {
                'got': 3,
                'msg': u'今日抽奖次数已用完'
            }
        elif 'draw' in resp and resp['draw'] == 1:
            prize_info = {
                'got': 3,
                'msg': u'抽奖时间已结束'
            }
        elif 'draw' in resp and resp['draw'] == 3:
            prize_info = {
                'got': 3,
                'msg': u'您所在区域不能参与抽奖'
            }
        else:
            prize_info = {
                'got': 2,
            }
        return prize_info, timestamp

    # 获取我的奖品
    def get_my_prize(self, activity_id, uid):
        my_prizes = []
        timestamp = int(str(time.time()).split('.')[0])
        file_folder = app.config['DATA_JSON'] + activity_id
        if os.path.exists(file_folder):
            with open(file_folder + '/data.json') as static_file:
                static_data = json.load(static_file)
            url = app.config['SERVICE_URL'] + SHAKE_MY_PRIZE_URL + \
                  '?activity_id=%s&uid=%s' % (activity_id, uid)
            static_prizes = static_data['prize']
            prizes, timestamp = self._request_url(url)
            prizes = prizes['history']
            for prize in prizes:
                for info in static_prizes:
                    if prize['type'] == info['type'] and prize['item'] == info['item']:
                        prize_info = {
                            'name': info['name'],
                            'pic': info['pic'],
                            'desc': info['desc']
                        }
                my_prizes.append(prize_info)
            return my_prizes, timestamp
        else:
            return None, timestamp

    # 获取一等奖中奖信息
    def _get_prize_shake_infos(self, activity_id):

        # 缓存中获取展示的中奖信息
        show_prizes_pickle = redis.hget('show_prizes', 'show_prizes')
        if show_prizes_pickle is None:
            # 展示奖品列表
            show_prizes = []
            # 获取配置信息
            file_folder = app.config['DATA_JSON']+activity_id
            with open(file_folder + '/data.json') as static_file:
                data = json.load(static_file)

            prizes = data['show_prizes']
            # 展示将品奖配置
            url = app.config['SERVICE_URL'] + SHAKE_Shake_Infos_URL + \
                  '?activity_id=%s&type=%s&item_min=%s&item_max=%s' % (
                      activity_id, prizes['type'], prizes['item_min'], prizes['item_max'])
            resp, timestamp = self._request_url(url)


            for prize in resp['list']:
                show_prize = {
                    'time': int(prize['time']),
                    'phone': prize['cellphone'],
                    'name': prize['name'],
                    'prize': ''
                }
                for prize_info in data['prize']:
                    if prize['item'] == prize_info['item'] and prize['type'] == prize['type']:
                        show_prize['prize'] = prize_info['name']
                show_prizes.append(show_prize)
            show_prizes_pickle = pickle.dumps(show_prizes)
            show_prizes = redis.hset('show_prizes', 'show_prizes', show_prizes_pickle)
            redis.expire('show_prizes', 600)
        show_prizes = pickle.loads(show_prizes_pickle)
        return show_prizes

    def _request_url(self, url):
        # 开始向后台接口发起请求的时间
        start_time = time.time()
        try:
            resp = json.loads(urllib2.urlopen(url, timeout=10).read())
        except Exception, e:
            print str(e)
        else:
            # 将请求信息写入log
            process_time = time.time() - start_time
            urllib2_log = app.config['LOG_FILE'] + 'urllib2.log'
            with open(urllib2_log, 'a') as f:
                f.write(str(time.ctime()) + ' ' + url + ' ' + str(process_time) + '\n')

            if resp['ret'] != 0:
                return None
            else:
                return resp['content'], resp['timestamp']
