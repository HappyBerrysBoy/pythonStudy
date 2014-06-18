# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 12:36:21 2014

@author: user
"""

import urllib2
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import sys
import cx_Oracle
import savefilegethtml
import xmltodict
import requests
import json

asiaUrl = 'http://www.wemakeprice.com/main/get_deal_more/990100/990102?curr_deal_cnt=0&r_cnt=500' # 동남아
asiaMainHtml = requests.get(asiaUrl).text
#asiaDict = xmltodict.parse(asiaMainHtml)
jsonload = json.loads(asiaMainHtml)

print jsonload