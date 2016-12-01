# -*- coding: utf-8 -*-
import os
from flask import Flask

from config import config
from common import db, alembic, bp as api_bp


__all__ = ['create_app']

def configure_app(app, config_name):
    if not config_name:
        config_name = os.getenv('CMS_ENV') or 'default'
    app.config.from_object(config[config_name])

def register_extensions(app):
    db.init_app(app)
    alembic.init_app(app)

def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/v1')

def create_app():
    app = Flask(__name__)
    configure_app(app, config_name=None)
    register_extensions(app)
    register_blueprints(app)
    return app
