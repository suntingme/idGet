# -*- coding: utf-8 -*-

import requests,json,time,re
import jd_urllib
import logging
import urllib
from bs4 import BeautifulSoup
import csvrw




# import sys   #reload()之前必须要引入模块
# reload(sys)
# sys.setdefaultencoding('utf-8')

LIST_HOST = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'



'''获取jd分页列表'''
def get_jd_list_by_page(first,second,location,keyWord,pageSize,pageIndex,t):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    # 通过urllib2.Request()方法构造一个请求对象
    formate = {}
    formate['pageSize'] = pageSize
    formate['keyWord'] = keyWord
    formate['pageIndex'] = pageIndex
    formate['second'] = second
    formate['first'] = first
    formate['t'] = t
    formate['location'] = location
    data = urllib.urlencode(formate)
    cookie = None

    resData = jd_urllib.send_json_request(LIST_HOST, data , 'POST', headers, cookie)

    return json.loads(resData)

def jdlist_parser(list):
    # linkList
    id_list = []
    if list['returnValue']:
        returnValue = list['returnValue']
        for data in returnValue['datas']:
            id_list.append(data['id'])

    return id_list



'''获取jd列表'''
def get_jd_list(first,second,location,keyWord,size=None):
    id_list = []
    list = get_jd_list_by_page(first, second, location, keyWord, '10', '1', '0.9388828046472246')

    if list['returnValue']:
        returnValue = list['returnValue']
        totalRecord = int(returnValue['totalRecord'])
        if not size is None:
            totalRecord = size/10+2
        for i in range(1,(totalRecord/10+2)):
            print i
            tmplist = get_jd_list_by_page(first, second, location, keyWord, '10', i, '0.9388828046472246')
            id_list.extend(jdlist_parser(tmplist))

    return id_list

'''获取每个jd详情'''
def get_jd_detail(id):
    content = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    url = 'https://job.alibaba.com/zhaopin/position_detail.htm?positionId='+str(id)
    cookie = None
    data = None
    html = jd_urllib.send_json_request(url, data, 'GET', headers, cookie)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all("h3",class_="bg-title")
    td = soup.find_all("td")
    detail_content= soup.find_all("p", class_="detail-content")

    content['标题'] = title[0].text.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
    content['发布时间'] = td[1].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')
    content['工作地点'] = td[3].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')
    content['工作年限'] = td[5].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')
    content['所属部门'] = td[7].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')
    content['学历'] = td[9].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')
    content['招聘人数'] = td[11].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')
    content['岗位描述']=detail_content[0].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')
    content['岗位要求']=detail_content[1].text.replace('\r','').replace('\n','').replace('\t','').replace(' ', '')

    return content



'''获取jd详情存储至csv'''
def get_jd_detail_list(ids):
    for id in ids:
        content = get_jd_detail(id)

    return content



if __name__ == '__main__':

    listcontent = []
    list = get_jd_list('技术类','质量保证','','')
    # list =[64696,64696]
    for id in list:
        try:
            content = get_jd_detail(id)
            listcontent.append(content)
        except:
            print("alibaba get_jd_detail exception occors for id......".join(id))

    headers = ['标题','发布时间','工作地点','工作年限','所属部门','学历','招聘人数','岗位描述','岗位要求']
    csvrw.csv_write_dict('xxx\\alibaba.csv',listcontent,headers)

    print 'success'



