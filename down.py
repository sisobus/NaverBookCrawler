#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import json
import datetime
import commands
import time
import sys

from bs4 import BeautifulSoup
from utils import download_source

currentTime = str(datetime.datetime.now())
ymd = currentTime.split(' ')[0].split('-')
year = int(ymd[0])
month = int(ymd[1])
day = int(ymd[2])
this_year, tot_week, week = datetime.date(year,month,day).isocalendar()

s_year = str(year)
s_month = str(month)
s_day = str(day)

categoryList = [310010, 310020, 320010, 320020, 320030]
tabList = ["top100","new_book","recommand"]

url = 'http://book.naver.com/'
values = {
    'cate_code':'320010',
    'list_type':'list',
    'tab':'top100',
        }
headers = {'Content-Type': 'application/x-www-form-urlencoded',
        }

(source,cookie_jar) =  download_source(url,values,headers,None)

def get_page_number(html):
    soup = BeautifulSoup(html)
    div = soup.find('div',{'class':'paginate'})
    #print div
    a = div.find_all('a')[-1].string
    if a == 'None' or len(str(a)) == 0:
        a = 1
    return int(a)

if not os.path.exists('html'):
    command = "mkdir html"
    ret = commands.getoutput(command)
if not os.path.exists('html/%d' % year):
    command = "mkdir html/%d" % year
    ret = commands.getoutput(command)
if not os.path.exists('html/%d/%d' % (year,month)):
    command = "mkdir html/%d/%d" % (year,month)
    ret = commands.getoutput(command)

path = 'html/%d/%d/' % (year,month)

for category in categoryList:
    category_path = path + str(category)
    if not os.path.exists(category_path):
        command = "mkdir %s" % category_path
        ret = commands.getoutput(command)

    for tab in tabList:
        tab_path = category_path + '/' + str(tab)
        if not os.path.exists(tab_path):
            command = "mkdir %s" % tab_path
            ret = commands.getoutput(command)

        url = 'http://book.naver.com/category/'
        queryString = '?cate_code='+str(category)+'&list_type=list&tab='+tab
        full_url = url+queryString

        values = {}
        (source,cookie_jar) = download_source(full_url,values,headers,cookie_jar)
        page_number = get_page_number(source)

        for i in xrange(1,page_number+1,1):
            now_url = full_url+'&page='+str(i)
            print now_url
            values = {}
            (source,cookie_jar) = download_source(now_url,values,headers,cookie_jar)
            with open(tab_path+'/%d.html'%i,'w') as fp:
                fp.write(source)
