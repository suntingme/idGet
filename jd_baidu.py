# -*- coding: utf-8 -*-

import requests,json,time,re
import jd_urllib
import logging
import urllib
from bs4 import BeautifulSoup




# import sys   #reload()之前必须要引入模块
# reload(sys)
# sys.setdefaultencoding('utf-8')

LIST_HOST = 'https://talent.baidu.com/baidu/web/httpservice/getPostList'



'''获取jd分页列表'''
def get_jd_list_by_page(postType,workPlace,keyWord,pageSize,curPage,time,recruitType=2):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    # 通过urllib2.Request()方法构造一个请求对象
    formate = {}
    formate['postType'] = postType
    formate['workPlace'] = workPlace
    formate['keyWord'] = keyWord
    formate['pageSize'] = pageSize
    formate['curPage'] = curPage
    formate['time'] = time
    formate['recruitType'] = recruitType
    data = urllib.urlencode(formate)

    # url首个分隔符就是 ?
    newurl = LIST_HOST + "?" + data
    cookie = None

    resData = jd_urllib.send_json_request(newurl ,None, 'GET', headers, cookie)

    return json.loads(resData)

def jdlist_parser(list):
    # linkList
    id_list = []
    if list['postList']:
        for data in list['postList']:
            id_list.append(data['postId'])

    return id_list



'''获取jd列表'''
def get_jd_list(postType,workPlace,keyWord,recruitType=2,size=None):
    id_list = []
    list = get_jd_list_by_page(postType,workPlace,keyWord,20,1,time,recruitType=2)

    if list['postList']:
        totalPage = list['totalPage']
        if not size is None:
            totalPage = size/20
        for i in totalPage:
            tmplist = get_jd_list_by_page(postType,workPlace,keyWord,20,i,time,recruitType=2)
            id_list.extend(jdlist_parser(tmplist))

    return id_list

'''获取每个jd详情'''
def get_jd_list(id):
    content = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    url = 'https://job.alibaba.com/zhaopin/position_detail.htm?positionId='+str(id)
    cookie = None
    data = None
    html = jd_urllib.send_json_request(url, data, 'GET', headers, cookie)
    soup = BeautifulSoup(html, 'html.parser')

    td = soup.find_all("td")
    detail_content= soup.find_all("p", class_="detail-content")

    content['发布时间'] = td[1].text.replace('\r','').replace('\n','').replace('\t','')
    content['工作地点'] = td[3].text.replace('\r','').replace('\n','').replace('\t','')
    content['工作年限'] = td[5].text.replace('\r','').replace('\n','').replace('\t','')
    content['所属部门'] = td[7].text.replace('\r','').replace('\n','').replace('\t','')
    content['学历'] = td[9].text.replace('\r','').replace('\n','').replace('\t','')
    content['招聘人数'] = td[11].text.replace('\r','').replace('\n','').replace('\t','')
    content['岗位描述']=detail_content[0].text.replace('\r','').replace('\n','').replace('\t','')
    content['岗位要求']=detail_content[1].text.replace('\r','').replace('\n','').replace('\t','')
    return content


'''获取jd详情存储至csv'''
def get_jd_list(ids):
    for id in ids:
        content = get_jd_list(id)

    return content



if __name__ == '__main__':

    # list = get_jd_list('技术类','质量保证','','',10)
    content = get_jd_list(64696)
    print  json.dumps(content, encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)
    print 'list'


