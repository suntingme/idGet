# -*- coding: utf-8 -*-

import requests,json,time,re
import jd_urllib
import logging
import urllib
from bs4 import BeautifulSoup




# import sys   #reload()之前必须要引入模块
# reload(sys)
# sys.setdefaultencoding('utf-8')

LIST_HOST = 'https://job.bytedance.com/api/recruitment/position/list/'



'''获取jd分页列表'''
def get_jd_list_by_page(city,summary_id,keyword,limit,offset,type=1):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    # 通过urllib2.Request()方法构造一个请求对象
    formate = {}
    formate['summary_id'] = summary_id
    formate['sequence'] = ''
    formate['city'] = city
    formate['q1'] = keyword
    formate['limit'] = limit
    formate['offset'] = offset
    formate['position_type'] = ''
    formate['_signature'] = ''
    formate['type'] = type
    data = urllib.urlencode(formate)

    # url首个分隔符就是 ?
    newurl = LIST_HOST + "?" + data
    cookie = None

    resData = jd_urllib.send_json_request(newurl ,None, 'GET', headers, cookie)

    return json.loads(resData)



'''获取jd列表'''
def get_jd_detail_list(city,summary_id,keyword,type=1,size=None):
    location = {
        '全部': '',
        '北京': '11',
        '上海': '125'
    }
    summary = {
        '全部': '',
        '技术': '873',
        '产品': '874'
    }

    list = get_jd_list_by_page(location[city],summary[summary_id],keyword,20,0,type)

    if list['count']:
        count = list['count']
        if not size is None:
            count = size
        for i in range(1, count, 20):
            tmplist = get_jd_list_by_page(location[city],summary[summary_id],keyword,20,i,type)
            jdlist_parser(tmplist)


'''由于detail页面需要signature，暂时只从列表获取每个jd详情'''
def jdlist_parser(list):
    content = {}
    # linkList
    if list['positions']:
        for data in list['positions']:
            positions = data['positions']
            content['标题'] = positions['name']
            content['发布时间'] = positions['create_time']
            content['工作地点'] = positions['city']
            content['工作年限'] = positions['work_year']
            content['所属部门'] = positions['category']
            content['学历'] = ''
            content['招聘人数'] = ''
            content['岗位描述'] = positions['description']
            content['岗位要求'] = positions['requirement']


if __name__ == '__main__':

    location = {
        '北京':'0/4/7/9',
        '上海':'0/4/10/11'
    }
    type = {
        '技术':'0/1227/10002',
        '产品':'0/1227/37850530'
    }

    list = get_jd_detail_list('全部','全部','测试',1,10)
    # content = get_jd_detail(145506)
    # print  json.dumps(content, encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)
    print 'list'

