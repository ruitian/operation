# -*- coding: utf-8 -*-
import os

from config import config
from flask import Flask
from main.common import db, alembic, redis
from operation import activity as activity_bp
from werkzeug.wsgi import SharedDataMiddleware

__all__ = ['create_app']
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def configure_app(app, config_name):
    if not config_name:
        config_name = os.getenv('CMS_ENV') or 'default'
    app.config.from_object(config[config_name])


def register_extensions(app):
    db.init_app(app)
    alembic.init_app(app)
    redis.init_app(app)


def register_blueprints(app):
    app.register_blueprint(activity_bp, url_prefix='/cms-market')


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(project_path, 'static/static'),
    )
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/cms-market': os.path.join(project_path, 'static')
    })
    configure_app(app, config_name=None)
    register_extensions(app)
    register_blueprints(app)
    return app
