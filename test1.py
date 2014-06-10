# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 12:54:12 2014

@author: KSC
"""
import urllib2
import json
import requests
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import cx_Oracle

class classPackage():
    def __init__(self):
        self.thing = 0
        self.menuCode = ''
        self.menuName = ''
        self.goodTypeCode = ''
        self.sbar = ''

class classProduct():
    def __init__(self):
        self.departDay = ''
        self.departTime = ''
        self.arriveDay = ''
        self.arriveTime = ''
        self.airCode = ''
        self.productName = ''
        self.url = ''
        self.price = ''
        self.status = ''
        self.period = ''


today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)

    
detailProductHtml = urllib2.urlopen('http://www.ybtour.co.kr/Goods/overseas/inc_evList_ajax.asp?goodCD=180201411&startDT=201406').read()
tempFile = open('ybtourTempFile.txt', 'w')
print >> tempFile, detailProductHtml
tempFile.close()

con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
detailProductList = open('ybtourTempFile.txt')
flag = False
ybtourproductfile = open('ybtourproductfile.txt', 'w')
clsProduct = classProduct()

for parcer in detailProductList:
    
    if parcer.strip()[:len('<td><input type="checkbox"')] == '<td><input type="checkbox"':
        flag = True
        clsProduct = classProduct()
    
    if flag:
        if parcer.strip()[:len('<td><span class="blue">')] == '<td><span class="blue">':
            spliter = parcer.strip().split(' ')
            clsProduct.departDay = spliter[1].split('>')[1]
            clsProduct.departTime = spliter[3].split('<')[0]
            clsProduct.arriveDay = spliter[4].split('>')[2]
            clsProduct.arriveTime = spliter[6].split('<')[0]
            print >> ybtourproductfile, 'departday:' + str(clsProduct.departDay) + ', departtime:'  + str(clsProduct.departTime) + ', arrDay:' + str(clsProduct.arriveDay) + ', arrTime:' + str(clsProduct.arriveTime)
        elif parcer.strip()[:len('<td><span class="logo"')] == '<td><span class="logo"':
            spliter = parcer.strip().split(' ')
            clsProduct.airCode = spliter[2].split('"')[1].decode('utf-8')
            print >> ybtourproductfile, 'airCode:' + clsProduct.airCode
        elif parcer.strip()[:len('<td class="lt"><a href="')] == '<td class="lt"><a href="':
            spliter = parcer.strip().split(' ')
            clsProduct.url = 'http://www.ybtour.co.kr' + spliter[2].split('"')[1]
            spliter = parcer.strip().split('>')
            clsProduct.productName = spliter[2].split('<')[0].replace("'", '').decode('utf-8')
            print >> ybtourproductfile, 'URL:' + clsProduct.url + ', Name:' + clsProduct.productName
        elif parcer.find('박') > -1 and len(parcer) < 9:
            clsProduct.period = parcer.strip()[:1]
            print >> ybtourproductfile, 'Period:' + clsProduct.period
        elif parcer.strip()[:len('<td class="blue">')] == '<td class="blue">' and parcer.find('</td>') < 0:
            spliter = parcer.strip().split('>')
            clsProduct.price = spliter[1].split('원')[0].replace(',', '')
            print >> ybtourproductfile, 'Price:' + clsProduct.price
        elif parcer.find('출발확정') > -1 or parcer.find('예약마감') > -1 or parcer.find('예약가능') > -1:
            spliter = parcer.strip().split('>')
            clsProduct.status = spliter[1].split('<')[0].decode('utf-8')
            print >> ybtourproductfile, 'Status:' + clsProduct.status
        elif parcer.strip() == '</tr>':
            flag = False
            query = "insert into product_test values (product_seq.nextval, 'ybtour','overseas','" + str(clsProduct.productName) + "','ICN',"
            query += "to_date('" + strftime("%Y", time)+'/'+str(clsProduct.departDay) + "'),'" + str(clsProduct.period) + "','','',to_char(sysdate, 'yyyymmdd'),'',"
            query += str(clsProduct.price) + ",'" + str(clsProduct.url) + "',to_date('" + strftime("%Y", time)+'/'+str(clsProduct.arriveDay) + "'),'','"
            query += str(clsProduct.status) + "','" + str(clsProduct.airCode) + "')"
            print query
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            
        #productClassList.append(clsProduct)
    
ybtourproductfile.close()
detailProductList.close()
con.close()
