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
import sys


class clsProductGroup():
    def __init__(self):
        self.name = ''
        self.menucode = ''
        self.url = ''

class clsProduct():
    def __init__(self):
        self.sDay = ''
        self.sTime = ''
        self.aDay = ''
        self.aTime = ''
        self.aCode = ''
        self.period = ''
        self.code = ''
        self.status = ''
        self.name = ''
        self.price = ''
        self.booked = ''
        self.url = ''
        
    def toString(self):
        return 'Code:'+self.code+',sDay:'+self.sDay+',sTime:'+self.sTime+',aDay:'+self.aDay+',aTime:'+self.aTime+',aCode:'+self.aCode+',Period:'+self.period+',status:'+self.status+',name:'+self.name+',price:'+self.price+',booked:'+self.booked



today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)

    
productListHtml = urllib2.urlopen('http://www.verygoodtour.com/Product/Package/PackageItem?MasterCode=APP5081&Month=06&Year=2014').read()
productListHtmlFile = open('productListHtml.txt', 'w')
print >> productListHtmlFile, productListHtml
productListHtmlFile.close()

#최종 상품들 잡아넣자..
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")                    
productCls = clsProduct()
productListHtml = open('productListHtml.txt')
for product in productListHtml:
    if product.find('class="pro_date"') > -1:
        productCls = clsProduct()
        productCls.sDay = strftime("%Y", time) + '/' + product.split('pro_date">')[1].split('(')[0].strip()
        productCls.sTime = product.split('<br/>')[0].split(')')[1].strip()
        productCls.aDay = strftime("%Y", time) + '/' + product.split('<span>')[1].split('(')[0].strip()
        productCls.aTime = product.split('<span>')[1].split(')')[1].split('<')[0].strip()
    elif product.find('class="pro_air"') > -1:
        productCls.aCode = product.split('</td>')[0].split('<br/>')[1].decode('utf-8')
    elif product.find('박') > -1 and product.find('class=') < 0:
        productCls.period = product.split('>')[1].split('박')[0]
    elif product.find('class="pro_detail tl"') > -1:
        productCls.code = product.split("DetailPage('")[1].split("'")[0]
        productCls.url = 'http://www.verygoodtour.com/Product/Package/PackageDetail?ProCode=' + productCls.code + '&MenuCode=1010201'
        #http://www.verygoodtour.com/Product/Package/PackageDetail?ProCode=APP5099-140612LJ&MenuCode=1010201
        tmp = len(product.split('</td>')[0].split('>'))
        productCls.name = product.split('</td>')[0].split('>')[tmp - 1].decode('utf-8')
    elif product.find('class="pro_price"') > -1:
        productCls.price = product.split('원')[0].split('>')[1].replace(',', '')
    elif product.find('class="pro_condition"') > -1:
        productCls.booked = product.split('title="')[1].split('"')[0].strip().decode('utf-8')
    elif product.find('</tr>') > -1:
        #query... 등등
        query = "insert into product_test values (product_seq.nextval, 'vgtour','bangkok','" + productCls.name + "','ICN',"
        query += "to_date('" + productCls.sDay + "'),'" + productCls.period + "','package','',to_char(sysdate, 'yyyymmdd'),''," + productCls.price + ",'" + productCls.url
        query += "',to_date('" + productCls.aDay + "'),'','" + productCls.booked + "','" + productCls.aCode +"')"
        print 'query ::: ' + query
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        #print >> productListFile, productCls.toString()
productListHtml.close()
cursor.close()
con.close()
