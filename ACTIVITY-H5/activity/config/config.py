# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')
)

LOG_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')
)

class Config(object):

    # json upload
    DATA_JSON = BASE_DIR + '/data/'
    LOG_FILE = LOG_DIR + '/log/'

    SECRET_KEY = 'NGUzMjc0MjBiYzQxMjkyZTgyZTk5ZTA2MDg2MDU1NDsd'

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 后端服务根URL
    SERVICE_URL = 'http://zs.market-api.wmdev2.lsh123.com'
    # 抽奖活动信息URL
    ACTIVITY_INFO_URL = SERVICE_URL + '/Operate/prize/getprizeinfo'
    # 抽奖根URL
    DRAW_URL = SERVICE_URL + '/Operate/prize/draw'
    # 当前用户抽奖信息URL
    USER_DRAWINFO_URL = SERVICE_URL + '/Operate/prize/getUserDrawInfos'
    # 总排行榜URL
    RANKING_URL = SERVICE_URL + "/Operate/prize/getrank"
    # 当前用户排名情况
    USER_RANKING_URL = SERVICE_URL + "/Operate/prize/getuserrank"
    # alembic
    ALEMBIC = {
        'script_location': 'alembic'
    }


class DevelopmentConfig(Config):
    DEBUG = True
    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/active'
    # mongodb
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'cms'


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/active'


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/active'


config = {
    'default': DevelopmentConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
