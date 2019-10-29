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

LIST_HOST = 'https://talent.baidu.com/baidu/web/httpservice/getPostList'



'''获取jd分页列表'''
def get_jd_list_by_page(postType,workPlace,keyWord,pageSize,curPage,curtime,recruitType=2):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    # 通过urllib2.Request()方法构造一个请求对象
    formate = {}
    formate['postType'] = postType
    formate['workPlace'] = workPlace
    formate['keyWord'] = keyWord
    formate['pageSize'] = pageSize
    formate['curPage'] = curPage
    formate['_'] = curtime
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
    location = {
        '北京': '0/4/7/9',
        '上海': '0/4/10/11'
    }
    type = {
        '技术': '0/1227/10002',
        '产品': '0/1227/37850530'
    }

    id_list = []
    curtime = int(round(time.time() * 1000))
    list = get_jd_list_by_page(type[postType],location[workPlace],keyWord,20,1,curtime,recruitType)

    if list['postList']:
        totalPage = list['totalPage']
        if not size is None:
            totalPage = size/20+1
        for i in range(totalPage):
            tmplist = get_jd_list_by_page(type[postType],location[workPlace],keyWord,20,i,curtime,recruitType)
            id_list.extend(jdlist_parser(tmplist))

    return id_list

'''获取每个jd详情'''
def get_jd_detail(id,recruitType=2):
    content = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

    url ='https://talent.baidu.com/baidu/web/httpservice/getPostDetail'
    curtime = int(round(time.time() * 1000))
    formate = {}
    formate['postId'] = id
    formate['recruitType'] = 2
    formate['isTicRecommend'] = 'null'
    formate['_'] = curtime
    formate['recruitType'] = recruitType
    data = urllib.urlencode(formate)

    # url首个分隔符就是 ?
    newurl = url + "?" + data
    cookie = None

    resData = jd_urllib.send_json_request(newurl, None, 'GET', headers, cookie)

    result = json.loads(resData)

    if result['detailInfo']:
        detailInfo = result['detailInfo']
        content['标题'] = detailInfo[0]['name']
        content['发布时间'] = detailInfo[0]['publishDate']
        content['工作地点'] = detailInfo[0]['workPlace']
        content['工作年限'] = ''
        content['所属部门'] = detailInfo[0]['orgName']
        if detailInfo[0].has_key('education'):
            content['学历'] = detailInfo[0]['education']
        else:
            content['学历'] = ''
        content['招聘人数'] = detailInfo[0]['recruitNum']
        content['岗位描述'] = detailInfo[0]['workContent']
        content['岗位要求'] = detailInfo[0]['serviceCondition']

    return content


'''获取jd详情存储至csv'''
def get_jd_detail_list(ids):
    for id in ids:
        content = get_jd_detail(id)

    return content



if __name__ == '__main__':

    listcontent = []
    list = get_jd_list('技术','北京','测试',2)
    # list =[64696]
    for id in list:
        try:
            content = get_jd_detail(id)
            listcontent.append(content)
        except:
            print("baidu get_jd_detail exception occors for id......".join(id))

    headers = ['标题', '发布时间', '工作地点', '工作年限', '所属部门', '学历', '招聘人数', '岗位描述', '岗位要求']
    csvrw.csv_write_dict('xxx\\baidu.csv',listcontent,headers)

    print 'success'



