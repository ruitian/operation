# -*- coding: utf-8 -*-
import urllib
import urllib2
from time import ctime, time

from flask import current_app as app
from flask import json

__all__ = ['BaseService']


class BaseService(object):

    @staticmethod
    def request_url(url):
        # 开始请求的时间
        start_time = time()
        try:
            resp = json.loads(urllib2.urlopen(url, timeout=15).read())
        except Exception, e:
            print str(e)
        else:
            # 请求信息写入log
            process_time = time() - start_time
            urllib2_log = app.config['LOG_DIR'] + 'urllib2.log'
            with open(urllib2_log, 'a') as f:
                f.write(str(ctime()) + ' ' + url + ' ' + str(process_time) + '\n')

            # 接口返回的数据
            if resp['ret'] != 0:
                return None, resp['timestamp']
            else:
                return resp['content'], resp['timestamp']
