# -*- coding: utf-8 -*-
from flask import current_app, json
import os
import urllib2

class LuckyDrawService(object):

    @staticmethod
    def get_static_data(**kwargs):
        file_folder = current_app.config['DATA_JSON']+kwargs['activity_id']
        if os.path.exists(file_folder):
            with open(file_folder+'/data.json') as static_file:
                data = json.load(static_file)
            # 获取所有的抽奖活动
            # draws_info 所有的抽奖活动
            # draw_info 对应本次activity_id的活动
            draws_info = LuckyDrawService.get_draws_info(kwargs['get_draw_url'])
            user_draw_info = LuckyDrawService.get_user_draw_info(kwargs['get_user_draw_url'])
            if draws_info is not None and user_draw_info is not None:
                draw_info = LuckyDrawService.get_draw_info(
                    draws_info['prizeInfo'], kwargs['activity_id'])
                if draw_info is not None:
                    data['activity_id'] = draw_info['activity_id']
                    data['activity_name'] = draw_info['name']
                    data['start_time'] = draw_info['begin_at']
                    data['end_time'] = draw_info['end_at']
                    data['prize_list'] = draw_info['prize_list']
                    data['play_count_day'] = int(draw_info['description'])
                    data['play_count_user'] = ((int(draw_info['end_at']) - int(draw_info['begin_at'])) / 86400) * int(draw_info['description'])
                    data['user_info'] = {
                        'all_times': int(user_draw_info['all_times']),
                        'today_times': int(user_draw_info['today_times']),
                        'score': int(user_draw_info['score']),
                        'zone_id': int(user_draw_info['zone_id'])
                    }
                    return json.dumps(data)
                else:
                    return json.dumps({
                        'type': 3,
                        'none': True
                    })
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

    # 获取所有抽奖活动信息
    @staticmethod
    def get_draws_info(url):
        return LuckyDrawService.request_url(url)

    # 获取某个活动信息
    @staticmethod
    def get_draw_info(draws, activity_id):
        for draw in draws:
            if draw['activity_id'] == activity_id:
                return draw

    # 开始抽奖
    @staticmethod
    def draw(url):
        # 封装中奖接口
        draw_play_info = {}
        resp = LuckyDrawService.request_url(url)
        if resp is not None and resp.has_key('draw'):
            return resp
        elif resp is None:
            return resp
        else:
            draw_play_info['score'] = resp['item']
            draw_play_info['grade'] = LuckyDrawService.score_to_grade(resp['item'])
            return draw_play_info

    # 按照分数划分等级,以后需改成可配置
    @staticmethod
    def score_to_grade(score):
        switcher = {
            '5': 1,
            '30': 2,
            '58': 3,
            '111': 4,
            '588': 5,
            '888': 6,
            '1111': 7,
            '2016': 8
        }
        return switcher.get(score)

    # 获取用户抽奖信息
    @staticmethod
    def get_user_draw_info(url):
        return LuckyDrawService.request_url(url)

    # 获取抽奖总排行榜
    @staticmethod
    def get_rank(**kwargs):

        ranking_info = LuckyDrawService.request_url(kwargs['ranking_url'])
        user_ranking_info = LuckyDrawService.request_url(kwargs['user_ranking_url'])
        if ranking_info is not None and user_ranking_info is not None:
            ranking_info['user_ranking'] = user_ranking_info['ranking']
            return ranking_info
        else:
            return None

    # 请求URL通用函数
    @staticmethod
    def request_url(url):
        try:
            resp = json.loads(urllib2.urlopen(url, timeout=15).read())
        except Exception, e:
            print str(e)
        else:
            if resp['ret'] != 0:
                return None
            return resp['content']
