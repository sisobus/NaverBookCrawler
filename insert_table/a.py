#!/usr/bin/python
#-*- coding: utf-8 -*-
import json
import sqlite3
import sys

info_db = sqlite3.connect('info.sqlite')
new_db = sqlite3.connect('new_table.sqlite')

info_cur = info_db.cursor()
new_cur = new_db.cursor()

query = 'CREATE TABLE "final_info"("LBRRY_NAME" TEXT, "PFLAG" INTEGER, "HFLAG" INTEGER, "CFLAG" INTEGER, "CODE_VALUE" TEXT, "ADRES" TEXT, "TEL_NO" TEXT, "HMPG_URL" TEXT, "FDRM_CLOSE_DATE" TEXT, "XCNTS" FLOAT, "YDNTS" FLOAT, "INFO_1" TEXT,"INFO_2" TEXT, "INFO_3" TEXT, "INFO_4" TEXT, "INFO_5" TEXT, "INFO_6" TEXT)'

#query = 'select * from db_310020_new_book_2014_11;'
#info_cur.execute(query)
'''
ss = info_cur.fetchall()
for s in ss:
    for t in s:
        print t
        '''
query = 'select * from final_info;'
new_cur.execute(query)
datas = new_cur.fetchall()

for data in datas:
    b = []
    for r in data:
        b.append(r)
    query = 'INSERT INTO final_info("LBRRY_NAME","PFLAG","HFLAG","CFLAG","CODE_VALUE","ADRES","TEL_NO","HMPG_URL","FDRM_CLOSE_DATE","XCNTS","YDNTS","INFO_1","INFO_2","INFO_3","INFO_4","INFO_5","INFO_6") VALUES ("%s",%d,%d,%d,"%s","%s","%s","%s","%s",%f,%f,"%s","%s","%s","%s","%s","%s");' %(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12],b[13],b[14],b[15],b[16])
    info_cur.execute(query)
    info_db.commit()
