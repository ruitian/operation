# -*- coding: utf-8 -*-
from . import bp, jsonify_with_data, RETStatus
from cms.service import NoticeService
from cms.libs.pagination import to_pagination_with_next_url
from flask import request, json


@bp.route('/notice/upload', methods=['GET', 'POST'])
def notice_upload():
    notice_service = NoticeService()
    upload_pic = request.files['file']
    resp, timestamp = notice_service.request_upload(upload_pic)
    if resp is not None:
        data = {
            'origin': resp['origin'],
            'img_id': resp['id']
        }
        return jsonify_with_data(data, timestamp=timestamp)

@bp.route('/notice/add', methods=['GET', 'POST'])
def add_notice():
    if request.method == 'POST':
        name = request.form['name']
        img_id = request.form['img_id']
    else:
        name = request.args.get('name')
        img_id = request.args.get('img_url')
    notice_service = NoticeService()
    resp = notice_service.update_notice(name, img_id)
    if resp is None:
        return jsonify_with_data('', RETStatus.UPDATE_NOTICE_ERROR)
    else:
        return jsonify_with_data('')

@bp.route('/notice/list', methods=['GET', 'POST'])
def notice_list():
    notice_service = NoticeService()
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 20, type=int)
    notices = notice_service.get_notice_list(offset, limit)
    paging = to_pagination_with_next_url(offset, limit, notice_service.count_all())
    return jsonify_with_data(notices, paging=paging)