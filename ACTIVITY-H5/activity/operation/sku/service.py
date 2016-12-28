# -*- coding: utf-8 -*-
import os
from flask import json, current_app as app

__all__ = ['SkuService']


class SkuService(object):
    def get_static_data(self, activity_id, uid):
        file_folder = app.config['DATA_JSON']+activity_id
        if os.path.exists(file_folder):
            with open(file_folder+'/data.json') as static_file:
                data = json.load(static_file)
            return json.dumps(data), 1482913615
        else:
            return json.dumps({
                'type': 1,
                'none': True
            })