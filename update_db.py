#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import json
import datetime
import commands
import time
import sys

import glob
import sqlite3

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

if not os.path.exists('db'):
    command = "mkdir db"
    ret = commands.getoutput(command)
if not os.path.exists('db/%d' % year):
    command = "mkdir db/%d" % year
    ret = commands.getoutput(command)
if not os.path.exists('db/%d/%d' % (year,month)):
    command = "mkdir db/%d/%d" % (year,month)
    ret = commands.getoutput(command)

path = 'db/%d/%d/' % (year,month)
html_path = 'html/%d/%d/' %(year,month)
json_path = 'json/%d/%d/' % (year,month)

for category in categoryList:
    category_path = path + str(category)
    html_category_path = html_path + str(category)
    json_category_path = json_path + str(category)
    if not os.path.exists(category_path):
        command = "mkdir %s" % category_path
        ret = commands.getoutput(command)

    for tab in tabList:
        tab_path = category_path + '/' + str(tab)
        html_tab_path = html_category_path + '/' + str(tab)
        json_tab_path = json_category_path + '/' + str(tab)
        if not os.path.exists(tab_path):
            command = "mkdir %s" % tab_path
            ret = commands.getoutput(command)

        tab_path = tab_path + '/'
        html_tab_path = html_tab_path + '/'
        json_tab_path = json_tab_path + '/'
        print tab_path

        if os.path.exists(tab_path+'ok'):
            print 'db update is aleady complete'
            continue

        if not os.path.exists(tab_path+'ok'):
            command = "touch %sok" % tab_path
            ret = commands.getoutput(command)

        db = sqlite3.connect('info.sqlite')
        cur = db.cursor()

        query = 'CREATE TABLE "db_%s_%s_%d_%d"("RANKING" INTEGER PRIMARY KEY NOT NULL, "BOOK_NAME" TEXT, "AUTHOR" TEXT, "STAR" FLOAT, "IMAGE_URL" TEXT, "ISBN" INTEGER, "PUBLISHER" TEXT, "PUB_DATE" TEXT)' % (str(category),str(tab),year,month)
        cur.execute(query)
        
        with open(json_tab_path+'books.json') as fp:
            books = json.loads(fp.read())
        
        for book in books:
            rank = book['rank']
            book_name = book['book_title']
            author = book['authors'][0]['author_name']
            star = book['star']
            image_url = book['img_url']
            publisher = book['publisher']
            pub_date = book['date']
            query = 'INSERT INTO db_%s_%s_%d_%d("RANKING","BOOK_NAME","AUTHOR","STAR","IMAGE_URL","PUBLISHER","PUB_DATE") VALUES (%d,"%s","%s","%s","%s","%s","%s"); ' % (str(category),str(tab),year,month,rank,book_name,author,star,image_url,publisher,pub_date)
#    print query
    #ret = ret + query
    #cur = db.cursor()    
            cur.execute(query)
            db.commit()
