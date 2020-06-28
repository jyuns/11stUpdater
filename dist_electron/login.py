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
    
    result = s.post('https://login.11st.co.kr/auth/front/selleroffice/logincheck.tmall', data = {
        'encryptedLoginName': userID,
        'encryptedPassWord': userPW,
        'priority': 92,
        'authMethod': 'login',
        'returnURL': 'http://soffice.11st.co.kr?ts=' + millis,
        'autoId': 'Y'
    }, headers = headers)

    return {
        "status" : result.status_code,
        "cookies" : s.cookies
    }

print(login(sys.argv[1], sys.argv[2]))