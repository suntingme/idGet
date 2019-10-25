# _*_ coding:utf-8 _*_

import logging
import urllib2
import json


def send_json_request(url, data, method='GET', headers=None, cookies=None):
    try:
        if method.lower() == 'post':
            request = urllib2.Request(url, data=data,headers=headers)
            # 向指定的url地址发送请求，并返回服务器响应的类文件对象
            response = urllib2.urlopen(request)
            # 服务器返回的类文件对象支持python文件对象的操作方法
            # read()方法就是读取文件里的全部内容，返回字符串
            resp = response.read()
        elif method.lower() == 'get':
            request = urllib2.Request(url, headers=headers)
            # 向指定的url地址发送请求，并返回服务器响应的类文件对象
            response = urllib2.urlopen(request)
            # 服务器返回的类文件对象支持python文件对象的操作方法
            # read()方法就是读取文件里的全部内容，返回字符串
            resp = response.read()
        else:
            assert False, "The request method %s is not in ['post','get','put','delete']"
    except Exception, e:
        print "[Request Exception] {0}: {1}".format(type(e), e)
        msg = "send request {%s] %s failed: %s" % (method, url, e.message)
        logging.error(e)
        logging.error(msg)
        assert False, msg
    return resp


# # User-Agent是爬虫与反爬虫的第一步
# ua_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
# # 通过urllib2.Request()方法构造一个请求对象
# formate = {}
# formate['pageSize'] = 10
# formate['keyWord'] = ''
# formate['pageIndex'] = 1
# formate['second'] = '质量保证'
# formate['first'] = '技术类'
# formate['t'] = 0.777777
# data = urllib.urlencode(formate)
# request = urllib2.Request('https://job.alibaba.com/zhaopin/socialPositionList/doList.json',data=data,headers=ua_headers)
# #向指定的url地址发送请求，并返回服务器响应的类文件对象
# response = urllib2.urlopen(request)
# # 服务器返回的类文件对象支持python文件对象的操作方法
# # read()方法就是读取文件里的全部内容，返回字符串
# html = response.read()
# print html