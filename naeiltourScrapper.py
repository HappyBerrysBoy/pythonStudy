# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 23:28:28 2014

@author: KSC
"""

#여행 종류 검색(여행 종류 별로 주소 따로 들어가면, 해당 페이지에 모든 지역 URL이 존재 하는듯..)
#내일로 가는 배낭여행(http://www.naeiltour.co.kr/backpack/eu_main.asp?area=40)
#개별자유여행 금까기(http://www.naeiltour.co.kr/friday/index.asp?menuId=DA)
#허니문 자기야(http://www.naeiltour.co.kr/jagiya/main.asp)
#골프(http://www.naeiltour.co.kr/GMT/)
#부산대구출발(http://www.naeiltour.co.kr/naeil21/index.asp)

import urllib2
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import sys
import cx_Oracle

class backpackRegionUrl():
    def __init__(self):
        self.url = ''
        self.menuname = ''

class freetourRegionUrl():
    def __init__(self):
        self.url = ''
        self.region = ''

# 시간 변수들..
today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)

homepageUrl = 'http://www.naeiltour.co.kr/'
#배낭여행 시작========================================
backpackUrl = 'http://www.naeiltour.co.kr/backpack/eu_main.asp?area=40'
mainHtml = urllib2.urlopen(backpackUrl).read()
mainHtml = mainHtml[mainHtml.find('<div id="left_mn">'):mainHtml.find('<div id="left_mn2">')]
mainHtmlFile = open('naeiltourbackpackHtml.txt', 'w')
print >> mainHtmlFile, mainHtml
mainHtmlFile.close()

comment = False
backpackMenuList = list()       #menu들 List
mainHtml = open('naeiltourbackpackHtml.txt')
for each_line in mainHtml:
    if comment == False and each_line.find('/backpack/list.asp?') > -1:
        backpackRegionClass = backpackRegionUrl()
        backpackRegionClass.url = homepageUrl + each_line.split('href="')[1].split('"')[0]
        if each_line.find('">-') > -1:
            backpackRegionClass.menuname = each_line.split('">-')[1].split('<')[0].strip()
        elif each_line.find('alt="') > -1:
            backpackRegionClass.menuname = each_line.split('alt="')[1].split('"')[0]
        backpackMenuList.append(backpackRegionClass)
        
    if each_line.find('<!--') > -1:
        comment = True
        
    if each_line.find('-->') > -1:
        comment = False
print len(backpackMenuList)
mainHtml.close()
#배낭여행 완료========================================
#자유여행 시작========================================
freetourUrl = 'http://www.naeiltour.co.kr/friday/eu/index.asp'
mainHtml = urllib2.urlopen(freetourUrl).read()
mainHtml = mainHtml[mainHtml.find('<div id="Leftmenu" style="align:left;">'):mainHtml.find('<!-- Theme Select -->')]
mainHtmlFile = open('naeiltourfreetourkHtml.txt', 'w')
print >> mainHtmlFile, mainHtml
mainHtmlFile.close()

comment = False
parcingStart = False
freetourMenuList = list()
mainHtml = open('naeiltourfreetourkHtml.txt')
for each_line in mainHtml:
    if each_line.find('<!--') > -1:
        comment = True
        
    if comment == False and each_line.find('3Depth_R') > -1:
        parcingStart = True
       
    if comment == False and parcingStart and each_line.find(' href="') > -1:
        freetourRegionClass = freetourRegionUrl()
        tmpNames = each_line.split('alt="')
        tmpUrls = each_line.split('href="')
        
        chkIdx = 0
        urlIdx = 1
        for name in tmpNames:
            if chkIdx % 2 == 1:
                freetourRegionClass = freetourRegionUrl()
                freetourRegionClass.region = name.split('"')[0]
                freetourRegionClass.url = homepageUrl + tmpUrls[urlIdx].split('"')[0]
                freetourMenuList.append(freetourRegionClass)
                urlIdx += 1
            chkIdx += 1

    if comment == False and each_line.find('</tr>') > -1:
        parcingStart = False

    if each_line.find('-->') > -1:
        comment = False
        
for aa in freetourMenuList:
    print aa.region + ' : ' + aa.url
print len(freetourMenuList)
mainHtml.close()
#116??
#자유여행 완료========================================
honeymoonUrl = 'http://www.naeiltour.co.kr/jagiya/main.asp'
golfUrl = 'http://www.naeiltour.co.kr/GMT/'
notseoulUrl = 'http://www.naeiltour.co.kr/naeil21/index.asp'


