# -*- coding: utf-8 -*-

import requests,json,time,re
import logging
import hashlib

HOST = 'https://gotest.hz.netease.com'
HEADER = {"Content-type": "application/json;charset=UTF-8"}


'''make user sign for every request
    @:param data
    @:param key
'''
def get_sign(data, key):
    src = json.dumps(data) + "|" + key
    m2 = hashlib.md5()
    m2.update(src)
    sign = m2.hexdigest()
    return sign


'''
    send request
    @param string url
    @param string params: such as &mobile=13212345678&act=check_mobile
    @param dict headers
    @param string method: GET or POST
    @return string data
    '''
def send_json_request(url, data, method='GET', headers=None, cookies=None):
    try:
        if method.lower() == 'post':
            if "https" in url:
                resp = requests.post(url, json=data, headers=headers, verify=False, cookies=cookies)
            else:
                resp = requests.post(url, json=data, headers=headers, cookies=cookies)
        elif method.lower() == 'get':
            if "https" in url:
                resp = requests.get(url, json=data, headers=headers, verify=False, cookies=cookies)
            else:
                resp = requests.get(url, json=data, headers=headers, cookies=cookies)
        elif method.lower() == 'put':
            if "https" in url:
                resp = requests.put(url, json=data, headers=headers, verify=False, cookies=cookies)
            else:
                resp = requests.put(url, json=data, headers=headers, cookies=cookies)
        elif method.lower() == 'delete':
            if "https" in url:
                resp = requests.delete(url, json=data, headers=headers, verify=False, cookies=cookies)
            else:
                resp = requests.delete(url, json=data, headers=headers, cookies=cookies)
        else:
            assert False, "The request method %s is not in ['post','get','put','delete']"
    except Exception, e:
        print "[Request Exception] {0}: {1}".format(type(e), e)
        msg = "send request {%s] %s failed: %s" % (method, url, e.message)
        logging.error(e)
        logging.error(msg)
        assert False, msg
    return resp


def send_url_request(url, data, method='GET', headers=None, cookies=None):
    try:
        if method.lower() == 'post':
            if "https" in url:
                resp = requests.post(url, params=data, headers=headers, verify=False, cookies=cookies)
            else:
                resp = requests.post(url, params=data, headers=headers, cookies=cookies)
        elif method.lower() == 'get':
            if "https" in url:
                resp = requests.get(url, params=data, headers=headers, verify=True, cookies=cookies)
            else:
                resp = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method.lower() == 'put':
            if "https" in url:
                resp = requests.put(url, params=data, headers=headers, verify=False, cookies=cookies)
            else:
                resp = requests.put(url, params=data, headers=headers, cookies=cookies)
        elif method.lower() == 'delete':
            if "https" in url:
                resp = requests.delete(url, params=data, headers=headers, verify=False, cookies=cookies)
            else:
                resp = requests.delete(url, params=data, headers=headers, cookies=cookies)
        else:
            assert False, "The request method %s is not in ['post','get','put','delete']"
    except Exception, e:
        print "[Request Exception] {0}: {1}".format(type(e), e)
        msg = "send request {%s] %s failed: %s" % (method, url, e.message)
        logging.error(e)
        logging.error(msg)
        assert False, msg
    return resp


