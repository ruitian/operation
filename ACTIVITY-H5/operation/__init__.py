# -*- coding: utf-8 -*-
from flask import Blueprint

__all__ = ['activity']

activity = Blueprint('activity', __name__)

from turnplate import *  # noqa
from shake import *  # noqa