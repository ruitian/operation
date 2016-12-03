# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

__all__ = ['activity']

activity = Blueprint('activity', __name__)

# 加载活动主页
@activity.route('/')
def index():
    return render_template('index.html')

# 导出活动路由
from turnplate import *  # noqa
from shake import *  # noqa

