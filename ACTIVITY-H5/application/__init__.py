# coding=utf-8
from .controllers import *
from main.common.api import bp

from flask import render_template

@bp.route('/')
def index():
    return render_template('index.html')