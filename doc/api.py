# -*- coding: utf-8 -*-
#
import json
import requests
from urlparse import urljoin

BASE_URL = 'http://192.168.1.24:5000/'
AUTH = ('admin', '1qaz@WSX')


def get_article_list():
    url = urljoin(BASE_URL, '/api/v1/posts/')
    print(url)
    rsp = requests.get(
        url, auth=AUTH, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    # assert rsp.ok
    print('get_article_list: ', rsp.ok, rsp.status_code, rsp.text)

def main():
    get_article_list()


if __name__ == "__main__":
    main()