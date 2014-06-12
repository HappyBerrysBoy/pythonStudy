# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 08:29:53 2014

@author: user
"""

import urllib2
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import sys
import cx_Oracle


# 시간 변수들..
today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)