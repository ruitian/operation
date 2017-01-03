# -*- coding: utf-8 -*-
from . import bp, jsonify_with_data
from cms.service import NoticeService
from cms.libs.pagination import to_pagination_with_next_url
from flask import request, json


@bp.route('/notice/upload', methods=['GET', 'POST'])
def notice_upload():
    notice_service = NoticeService()
    text = json.loads(request.data)['base64']
    resp, timestamp = notice_service.request_upload(text)
    if resp is not None:
        data = {
            'origin': resp['origin'],
            'img_id': resp['id']
        }
        return jsonify_with_data(data, timestamp=timestamp)


@bp.route('/notice/list', methods=['GET', 'POST'])
def notice_list():
    notice_service = NoticeService()
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 20, type=int)
    notices = notice_service.get_notice_list(offset, limit)
    paging = to_pagination_with_next_url(offset, limit, notice_service.count_all())
    return jsonify_with_data(notices, paging=paging)