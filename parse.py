#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import json
import datetime
import commands
import time
import sys

import glob

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

if not os.path.exists('json'):
    command = "mkdir json"
    ret = commands.getoutput(command)
if not os.path.exists('json/%d' % year):
    command = "mkdir json/%d" % year
    ret = commands.getoutput(command)
if not os.path.exists('json/%d/%d' % (year,month)):
    command = "mkdir json/%d/%d" % (year,month)
    ret = commands.getoutput(command)

path = 'json/%d/%d/' % (year,month)
html_path = 'html/%d/%d/' %(year,month)

for category in categoryList:
    category_path = path + str(category)
    html_category_path = html_path + str(category)
    if not os.path.exists(category_path):
        command = "mkdir %s" % category_path
        ret = commands.getoutput(command)

    for tab in tabList:
        tab_path = category_path + '/' + str(tab)
        html_tab_path = html_category_path + '/' + str(tab)
        if not os.path.exists(tab_path):
            command = "mkdir %s" % tab_path
            ret = commands.getoutput(command)
        tab_path = tab_path + '/'
        html_tab_path = html_tab_path + '/'
        print tab_path
        
        filenames = glob.glob(html_tab_path+'*.html')
    
        allBook = []
        rank = 1
        for filename in filenames:
            if not os.path.exists(filename):
                print 'html file is not exists'
            with open(filename,'r') as fp:
                s = fp.read()

            soup = BeautifulSoup(s)
            ol = soup.find('ol')
            if ol == None:
                print 'error : ol is none!'
                continue
            lis = ol.find_all('li')
            for li in lis:
                img_src = (li.find_all('a'))[0].find('img')['src']
                dt = li.find('dt')
                book_url = dt.find('a')['href']
                book_title = dt.find('a').string
                if book_title == None:
                    continue

                dds = li.find_all('dd')
                date = dds[0].contents[-1].lstrip().rstrip()

                star = dds[1].contents[2].lstrip().rstrip()

                authors = []
                aa = dds[0].find_all('a')

                publisher = ""
                if dds[0].contents[-3] <> None:
                    publisher = dds[0].contents[-3].string.lstrip().rstrip()
                else:
                    publisher = ""

                for a in aa:
                    now = a['href']
                    now = now.lstrip().rstrip()
                    t = {
                        'author_name':a.string,
                        'author_url':now
                    }
                    authors.append(t)

                body = dds[2].contents[1].lstrip().rstrip()
                t = {
                    'img_url':img_src,
                    'book_url':book_url,
                    'book_title':book_title,
                    'authors':authors,
                    'body':body,
                    'date':date,
                    'rank':rank,
                    'star':star,
                    'publisher':publisher
                }
                allBook.append(t)
                rank = rank+1
        with open(tab_path+'books.json','w') as fp:
            fp.write(json.dumps(allBook))
