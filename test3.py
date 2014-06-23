# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 02:29:14 2014

@author: KSC
"""

import datetime
import sys
import cx_Oracle
import savefilegethtml

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

def getTourType(idx):
    if idx == 0:
        return 'P'
    elif idx == 1:
        return 'F'
    elif idx == 2:
        return 'D'
    elif idx == 3:
        return 'B'
    elif idx == 4:
        return 'W'
    elif idx == 5:
        return 'G'
    elif idx == 6:
        return 'L'
    elif idx == 7:
        return 'A'
    elif idx == 8:
        return 'H'
    elif idx == 9:
        return '법인'
        
productListHtml = savefilegethtml.getHtml('http://www.verygoodtour.com/Product/Package/PackageItem?MasterCode=APP5028&Month=06&Year=2014', '', '', 'productListHtml.txt')

#최종 상품들 잡아넣자..
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")                    
productCls = clsProduct()
#productListHtml = open('productListHtml.txt')
for product in productListHtml:
    #print 'product : ' + product
    if product.find('pro_date') > -1:
        productCls = clsProduct()
        productCls.sDay = '2014' + product.split('pro_date">')[1].split('(')[0].strip().replace('/', '')
        productCls.sTime = product.split('<br/>')[0].split(')')[1].strip().replace(':', '')
        productCls.aDay = '2014' + product.split('<span>')[1].split('(')[0].strip().replace('/', '')
        productCls.aTime = product.split('<span>')[1].split(')')[1].split('<')[0].strip().replace(':', '')
    elif product.find('<img src=') > -1 and product.find('pro_detail') < 0:
        productCls.aCode = product.split("alt='")[1].split("'")[0].decode('utf-8')
    elif (product.find('박') > -1 or product.find('일') > -1) and product.find('class=') < 0:
        productCls.period = product.split('박')[1].split('일')[0].strip()
    elif product.find('class="pro_detail tl"') > -1:
        productCls.code = product.split("DetailPage('")[1].split("'")[0]
        productCls.url = 'http://www.verygoodtour.com/Product/Package/PackageDetail?ProCode=' + productCls.code + '&MenuCode='
        #http://www.verygoodtour.com/Product/Package/PackageDetail?ProCode=APP5099-140612LJ&MenuCode=1010201
        tmp = len(product.split('</td>')[0].split('>'))
        productCls.name = product.split('</td>')[0].split('>')[tmp - 1].decode('utf-8')
    elif product.find('pro_price') > -1:
        productCls.price = product.split('원')[0].split('>')[1].replace(',', '')
    elif product.find('class="pro_condition"') > -1:
        productCls.booked = product.split('title="')[1].split('"')[0].decode('utf-8')
    elif product.find('</tr>') > -1:
        #print productCls.toString()
        #query... 등등
        #print mastercode
        #print productCls.code
        #print productCls.name
        #print productCls.sDay+productCls.sTime
        #print productCls.aDay+productCls.aTime
        #print productCls.period
        #print departCity
        #print productCls.aCode
        #print productCls.booked
        #print productCls.url
        #print productCls.price
        print 'productCls.code : ' + productCls.code
        if productCls.code.strip() == '':
            continue
        
        query = savefilegethtml.getDetailMergeQuery('vgtour', 'APP5028', productCls.code, productCls.name, productCls.sDay+productCls.sTime, productCls.aDay+productCls.aTime, productCls.period, 'ICN', '', productCls.aCode, productCls.booked, productCls.url, productCls.price, '0', '0', '0', '') 
        print query
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        #break


con.close()
