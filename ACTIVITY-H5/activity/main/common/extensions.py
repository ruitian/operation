# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from flask_redis import Redis


db = SQLAlchemy()
alembic = Alembic()
redis = Redis()
