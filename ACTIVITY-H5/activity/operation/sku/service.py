# -*- coding: utf-8 -*-
import os
import time
import urllib2
from flask import json, current_app as app

__all__ = ['SkuService']

# 获取商品列表接口地址, 参数为sku_ids（json串）

GET_GOODS = '/goods/sku/getinfos'

class SkuService(object):
    def get_static_data(self, activity_id):
        file_folder = app.config['DATA_JSON']+activity_id
        if os.path.exists(file_folder):
            with open(file_folder+'/data.json') as static_file:
                data = json.load(static_file)
            modules = []
            for sku_list in data['modules']:
                sku_infos = []
                # 请求接口的参数
                skus = sku_list['skuList']
                url = '{0}{1}?sku_ids={2}'.format(
                    app.config['SERVICE_URL'], GET_GOODS, json.dumps(skus)
                )
                resp, timestamp = self._request_url(url)
                # 循环列表，用商品id来检索信息
                for sku in skus:
                    if resp.has_key(str(sku['sku_id'])):
                        sku_info = resp[str(sku['sku_id'])]
                        info = {
                            "sku_id": sku_info['sku_id'],
                            "name": sku_info['name'],
                            "sale_price": sku_info['sale_price'],
                            "img_list": sku_info['img_list']
                        }
                    # 一个模块中的商品列表
                    sku_infos.append(info)
                # 每个模块包含的信息
                if sku_list.has_key('prize_list'):
                    moudle_info = {
                        "skuList": sku_infos,
                        "banner": sku_list['banner'],
                        "name": sku_list['name'],
                        "titleImg": sku_list['titleImg'],
                        "hotSale": sku_list['hotSale'],
                        "prize_list": sku_list['prize_list']
                    }
                else:
                    moudle_info = {
                        "skuList": sku_infos,
                        "banner": sku_list['banner'],
                        "name": sku_list['name'],
                        "titleImg": sku_list['titleImg'],
                        "hotSale": sku_list['hotSale']
                    }
                modules.append(moudle_info)
            data['modules'] = modules
            return json.dumps(data), timestamp
        else:
            return json.dumps({
                'type': 1,
                'none': True
            })

    def get_sku_list(self, skuList):
        pass

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
