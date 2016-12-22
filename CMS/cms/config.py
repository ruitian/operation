# -*- coding: utf-8 -*-
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # json upload
    DATA_JSON = BASE_DIR + '/data/'
    LOG_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..'
    ))

    SECRET_KEY = 'NGUzMjc0MjBiYzQxMjkyZTgyZTk5ZTA2MDg2MDU1NDsd'

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 后端服务根URL
    SERVICE_URL = 'http://zs.market-api.wmdev2.lsh123.com'

    # alembic
    ALEMBIC = {
        'script_location': 'alembic'
    }

    # cookie 信息
    COOKIE_NAME = 'remember_token'
    COOKIE_SECURE = None
    COOKIE_DURATION = timedelta(days=21)


class DevelopmentConfig(Config):
    DEBUG = True
    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/lsh_cms'
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
