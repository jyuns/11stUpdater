#-*- coding:utf-8 -*-

import sys
import json
import hashlib
import time
import requests

def upload(cookies, path, type) :
    s = requests.Session()
    
    headers = {
        'User-agent' : 'Mozilla/5.0'
    }

    cookiesJSON = json.load(cookies)
    
    if type in ('jpeg', 'jpg', 'png', 'gif', 'bmp') :
        # image upload

        files = open(path, 'rb')

        fileName = files

        upload = { 'fileArr' : files }

        result = s.post('https://wpartner.wemakeprice.com/common/uploadImageAsync.json',
            data = {
                'fileFieldName': 'fileArr',
                'fileName': fileName,
                'imgKey': 'MultipleTemp',
                'baseKeyCd': userID,
                'mode': 'upload'
            }, headers = headers, files = upload, cookies = cookiesJSON['cookies'])
            
        return result.status_code


    elif type in ('xlsx', 'xls') :
        # excel upload
        # excel 업로드의 경우, 파일 업로드 후 다시 네이버 업로드까지 진행해야 됨.

        files = open(path, 'rb')

        fileName = files

        upload = { 'fileArr' : files }

        result = s.post('https://wpartner.wemakeprice.com/common/uploadImageAsync.json',
            data = {
                'fileFieldName': 'fileArr',
                'fileName': fileName,
                'imgKey': 'MultipleTemp',
                'baseKeyCd': userID,
                'mode': 'upload'
            }, headers = headers, files = upload, cookies = cookiesJSON)
            
        return result.status_code


#print(login(sys.argv[1], sys.argv[2]))