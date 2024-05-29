from flask import Blueprint, render_template, request
import time
import requests
import json
from .constant import BASE_URL, CLIENT_ID, getAccessToken, record_types, displayTime  

lock_bp = Blueprint('lock', __name__, url_prefix='/lock')

ACCESS_TOKEN = ''

@lock_bp.route('/')
def index():
    ACCESS_TOKEN = getAccessToken()
    cur_time = time.time()
    url = BASE_URL + "v3/lock/list"
    lock_response = requests.post(url, data= {
        'clientId' : CLIENT_ID,
        'accessToken' : ACCESS_TOKEN,
        'pageNo' : 1,
        'pageSize' : 100,
        'date' : int(cur_time) * 1000
    })
    lock_data = json.loads(lock_response.text)
    for item in lock_data['list']:
        item['electricQuantityUpdateDate'] = time.strftime('%Y.%m.%d %H:%M', time.localtime(item['electricQuantityUpdateDate'] / 1000))
    return render_template('lock.html', data=lock_data, current_route='lock')


@lock_bp.route('/data', methods=["GET"])
def getRecords():
    cur_time = time.time()
    url = BASE_URL + "v3/lockRecord/list"
    lockId = request.args.get('lockId')
    pageNo = request.args.get('page', default=0)
    startDate = int(request.args.get('startDate', default=-1))
    endDate = int(request.args.get('endDate', default=-1))

    params={
        'clientId' : CLIENT_ID,
        'accessToken': ACCESS_TOKEN,
        'lockId': lockId,
        'pageNo': int(pageNo) + 1,
        'pageSize': 20,
        'date': int(cur_time) * 1000
    }
    if startDate != -1 and endDate != -1:
        params["startDate"] = startDate
        params["endDate"] = endDate

    record_response = requests.get(url, params=params)
    record_data = json.loads(record_response.text)

    data = []

    for item in record_data['list']:
        data.append({
            "username": item["username"],
            "recordType": record_types[item["recordType"]],
            "lockDate": displayTime(item["lockDate"]),
            "success": 'Success' if item["success"]==1 else 'Failed'
        })

    return {
        "data": data,
        "total": record_data['total']
    }
