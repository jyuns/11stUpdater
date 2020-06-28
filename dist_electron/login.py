#-*- coding:utf-8 -*-

import sys
import json
import hashlib
import time
import requests

def login(userID, userPW) :
    s = requests.Session()
    
    headers = {
        'User-agent' : 'Mozilla/5.0'
    }

    millis = str(round(time.time() * 1000))

    res = s.get('https://wpartner.wemakeprice.com/salt.json?_=' + millis)
    salt = json.loads(res.text)['data']['salt']
    

    substrSalt = salt[1] + salt[4] + salt[8] + salt[12]

    passwordHash = hashlib.sha1((substrSalt + hashlib.sha1(userPW.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest() + substrSalt
    
    result = s.post('https://wpartner.wemakeprice.com/login.json', data = {
        'userId': userID,
        'userPassword': passwordHash
    }, headers = headers)

    return {
        "status" : result.status_code,
        "cookies" : s.cookies
    }

print(login(sys.argv[1], sys.argv[2]))