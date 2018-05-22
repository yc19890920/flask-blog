# -*- coding: utf-8 -*-
#

import json
import requests
from urlparse import urljoin

BASE_URL = 'http://192.168.1.24:6060/'
AUTH = ('admin', '1qaz@WSX')

"""
curl -X POST -d '{"title":"a","code":"print a"}'  http://django2blog.com/api/tag/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

# http -a admin:1qaz@WSX POST http://django2blog.com/api/tag/ name="tag1"
# curl -d "user=admin&passwd=1qaz@WSX" "http://django2blog.com/api/tag/"

"""
from flask.views import MethodView

def get_jwt_token():
    # url = urljoin(BASE_URL, '/api/jwt-auth')
    url = urljoin(BASE_URL, '/jwt-auth')
    rsp = requests.post(
        url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }, data=json.dumps({ "username":"admin", "password":"1qaz@WSX"})
    )
    print(rsp.status_code)
    print(rsp.text)
    print(rsp.content)
    j = rsp.json()
    # print(j)
    return j["access_token"]


def main():
    token = get_jwt_token()
    print(token)


if __name__ == "__main__":
    main()