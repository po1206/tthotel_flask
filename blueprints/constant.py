import os
import requests
import time
import json
from dotenv import load_dotenv
from os.path import join, dirname


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

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USERNAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
BASE_URL = "https://euapi.sciener.com/"

headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = "2722dfdc850c256870d19f319ca002dd"

def displayTime(timestamp):
    return time.strftime('%Y.%m.%d %H:%M', time.localtime(int(timestamp) / 1000))

def getAccessToken() :
    response = requests.post(url=BASE_URL + "oauth2/token", data = {
        'clientId' : CLIENT_ID,
        'clientSecret' : CLIENT_SECRET,
        'username' : USERNAME,
        'password' : PASSWORD
    })
    
    token_json = json.loads(response.text)
    return token_json['access_token']
