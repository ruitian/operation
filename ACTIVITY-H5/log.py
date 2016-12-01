# -*- coding: utf-8 -*-
from datetime import datetime
import urllib2
import json
import time
import os


def logging():
    dir_name = os.getcwd()
    today_date = datetime.today().strftime("%Y-%m-%d")


    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=1)

    opener = urllib2.build_opener(httpHandler, httpsHandler)

    urllib2.install_opener(opener)
    # 请求开始时间
    start_time = time.time()
    response = urllib2.urlopen('http://qa2.market-api.wmdev2.lsh123.com/Operate/prize/getprizeinfo',
                               timeout=10).read()
    # 请求时间
    request_time = (time.time() - start_time) * 1000
    with open('%s/log/%s-urllib2.txt' % (dir_name, today_date), 'a') as f:
        f.write(response+str(request_time))

logging()
