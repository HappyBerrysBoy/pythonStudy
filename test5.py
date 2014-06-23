# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 21:35:22 2014

@author: KSC
"""

import time, datetime
from time import localtime, strftime
from datetime import timedelta
import urllib2
import cx_Oracle
import savefilegethtml
import sys
import random
import requests
import xmltodict


detailUrl = requests.get('http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=06&Pcode=ATP203&Pd=&Type=01').text
tree = xmltodict.parse(detailUrl)
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")

productCode = tree['ModeSangPum']['SCode']
productName = tree['ModeSangPum']['STitle'].replace("'", "")
productComment = tree['ModeSangPum']['SCont'].replace("'", "")
query = savefilegethtml.getMasterMergeQuery('modetour', productCode, '', '', 'AAA', productName, 'P', 'A', productComment, '')
print query
cursor = con.cursor()
cursor.execute(query)
con.commit()  

for t in tree['ModeSangPum']['SangList']:
    prd_nm = t['SName']['#text'].replace("'", "")
    air_cd = t['SAirCode']
    st_dt = t['SPriceDay']['#text']
    st_time = t['SstartTime'].replace(':', '')
    arr_day = t['SArrivalDay']['#text']
    arr_time = t['SArrivalTime'].replace(':', '')
    tr_term = t['SDay']
    prd_fee = t['SPrice']
    prd_status = t['SDetailState']['#text']
    prd_code = t['SPriceNum']['#text']
    flynum = t['SstartAir']
    airline = t['SAirName']
    query = savefilegethtml.getDetailMergeQuery('modetour', productCode, prd_code, prd_nm, st_dt+st_time, arr_day+arr_time, tr_term, 'DDD', '', air_cd, prd_status, 'URL', prd_fee, '0', '0', '0', '') 
    print query
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    
con.close()