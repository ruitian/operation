# -*- coding: utf-8 -*-
import os
from flask import Flask

from cms.config import config
from cms.extensions import db
from cms.extensions import alembic
from cms.api import bp as api_bp

__all__ = ['create_app']

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def configure_app(app, config_name):
    if not config_name:
        config_name = os.getenv('CMS_ENV') or 'default'
    app.config.from_object(config[config_name])

def register_extensions(app):
    db.init_app(app)
    db.init_app(app)
    alembic.init_app(app)

def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='')

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(project_path, 'static/static')
    )
    configure_app(app, config_name=None)
    register_extensions(app)
    register_blueprints(app)
    return app
