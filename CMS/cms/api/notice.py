# -*- coding: utf-8 -*-
from . import bp, jsonify_with_data
from cms.service import NoticeService
from flask import request, json


@bp.route('/notice/upload', methods=['GET', 'POST'])
def notice_upload():
    notice_service = NoticeService()
    text = json.loads(request.data)['base64']
    resp, timestamp = notice_service.request_upload(text)
    if resp is not None:
        data = {'origin': resp['origin']}
        return jsonify_with_data(data, timestamp=timestamp)
