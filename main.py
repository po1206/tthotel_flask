from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from os.path import join, dirname
import requests
import time
import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USERNAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
BASE_URL = "https://euapi.sciener.com/"

ACCESS_TOKEN = "2722dfdc850c256870d19f319ca002dd"
record_types = {
    1: "unlock by app",
    4: "unlock by passcode",
    5: "Rise the lock (for parking lock)",
    6: "Lower the lock (for parking lock)",
    7: "unlock by IC card",
    8:"unlock by fingerprint",
    9:"unlock by wrist strap",
    10:"unlock by Mechanical key ",
    11:"lock by app",
    12:"unlock by gateway",
    29:"apply some force on the Lock",
    30:"Door sensor closed",
    31:"Door sensor open",
    32:"open from inside",
    33:"lock by fingerprint",
    34:"lock by passcode",
    35:"lock by IC card",
    36:"lock by Mechanical key ",
    37:"Remote Control",
    42:"received new local mail",
    43:"received new other cities' mail",
    44:"Tamper alert",
    45:"Auto Lock",
    46:"unlock by unlock key",
    47:"lock by lock key",
    48:"System locked ( Caused by, for example: Using INVALID Passcode/Fingerprint/Card several times)",
    49:"unlock by hotel card",
    50:"Unlocked due to the high temperature",
    51:"Try to unlock with a deleted card",
    52:"Dead lock with APP",
    53:"Dead lock with passcode",
    54:"The car left (for parking lock)",
    55:"Unlock with key fob",
    57:"Unlock with QR code success",
    58:"Unlock with QR code failed, it's expired",
    59:"Double locked",
    60:"Cancel double lock",
    61:"Lock with QR code success",
    62:"Lock with QR code failed, the lock is double locked",
    63:"Auto unlock at passage mode",
    64:"Door unclosed alarm",
    65:"Failed to unlock",
    66:"Failed to lock",
    67:"Face unlock success",
    68:'Face unlock failed :" door locked from inside',
    69:"Lock with face",
    71:'Face unlock failed :" expired or ineffective',
    75:"Unlocked by App granting",
    76:"Unlocked by remote granting",
    77:"Authenticated with App",
    78:"Authenticated with passcode",
    79:"Authenticated with fingerprint",
    80:"Authenticated with card",
    81:"Authenticated with face",
    82:"Authenticated with wireless key",
    83:"Authenticated with palm vein",
    84:"Palm vein unlock success",
    85:"Palm vein unlock success",
    86:"Lock with palm vein",
    88:'Palm vein unlock failed :" expired or ineffective',
}




def displayTime(timestamp):
    return time.strftime('%Y.%m.%d %H:%M', time.localtime(timestamp / 1000))

app = Flask(__name__)
headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }

def getAccessToken() :
    response = requests.post(url=BASE_URL + "oauth2/token", data = {
        'clientId' : CLIENT_ID,
        'clientSecret' : CLIENT_SECRET,
        'username' : USERNAME,
        'password' : PASSWORD
    })
    
    token_json = json.loads(response.text)
    return token_json['access_token']

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/lock')
def lock_page() :
    ACCESS_TOKEN = getAccessToken()
    cur_time = time.time()
    print(cur_time)
    
    
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
    return render_template('lock.html', data=lock_data)



@app.route('/lock/data', methods=["GET"])
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
    print(f"{params}")
    record_response = requests.get(url, params=params)
    record_data = json.loads(record_response.text)
    print(f"{record_data}")
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
