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
import codes

a = ''
b = ''
c = '칼리보'
d = ''
rt = codes.getCityCode(a, b, c, d)
#siteCode = rt[0]
cityCode = rt[0]
ntCode = rt[1]
cnttCode = rt[2]
siteCode = rt[3]

print siteCode
print cityCode
print ntCode
print cnttCode