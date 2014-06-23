# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

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

detailUrl = requests.get('http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=06&Pcode=ESP321&Pd=&Type=01').text
tree = xmltodict.parse(detailUrl)
dd = dict()
productCode = tree['ModeSangPum']['SCode']
productName = tree['ModeSangPum']['STitle']
productComment = tree['ModeSangPum']['SCont']
print productCode
print productName
print productComment
#print tree['ModeSangPum']['SangList']['SAirCode']

"""
for t in tree['ModeSangPum']['SangList']:
    prd_nm = t['SName']['#text']
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

"""