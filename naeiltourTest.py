# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

@author: KSC
"""

import re
import codes
import sys
import requests
import xmltodict
import savefilegethtml
import tourUtil


class clsProduct():
    def __init__(self):
        self.productname = ''
        self.price = ''
        self.dDay = ''
        self.dTime = ''
        self.aDay = ''
        self.aTime = ''
        self.night = ''
        self.period = ''
        self.airCode = ''
        self.status = ''
        self.url = ''
        self.code = ''
        self.productCode = ''
        self.airchk = ''
        self.city = ''
    
    def toString(self):
        val = 'name:'+self.productname+',price:'+self.price+',dDay:'+self.dDay+',dTime:'+self.dTime+',aDay:'+self.aDay+',aTime:'+self.aTime + ',night:'+self.night+',city:'+self.city
        val += ',period:'+self.period+',airCode:'+self.airCode+',status:'+self.status+',url:'+self.url+',code:'+self.code+',productCode:'+self.productCode+',airchk:'+self.airchk
        return val
        
tourkind = 'W'
period = ''
detailHtml = savefilegethtml.getHtml('http://www.naeiltour.co.kr/jagiya/honeymoon/program_include.asp?good_cd=550201054&sel_ym=201407', '', '', 'naeiltourDetailHtml.txt')
departDayList = list()
for detail_each_line in detailHtml:
    if detail_each_line.find("fn_goodDetail('") > -1:
        departDayList.append(detail_each_line.split("fn_goodDetail('")[1].split("'")[0])
        
# 출발 가능 날짜에 항공사 찾아오는 부분
productCls = clsProduct()

for dayInfo in departDayList:
    productListUrl = 'http://www.naeiltour.co.kr/jagiya/honeymoon/program_include.asp?good_cd=550201054&sel_day=20140712'
    print 'ProductListUrl : ' + productListUrl
    productListHtml = savefilegethtml.getHtml(productListUrl, '', '', 'naeiltourproductListHtml.txt')
    print 'ProductListUrl : ' + productListUrl
    for product in productListHtml:
        if product.find("fn_price('") > -1:
            productCls = clsProduct()
            productSplit = product.split('fn_price')[1].split("'")
            productCls.productCode = productSplit[1]
            productCls.dDay = productSplit[3]
            productCls.code = productSplit[5]
            if tourkind == 'W' or tourkind == 'G':
                productCls.airCode = product[product.find('.gif') - 2:product.find('.gif')]
            else:
                productCls.airCode = productSplit[7]            # 한글 공항코드... but 우리는 영문2자리 공항코드가 필요하다...
            productCls.price = productSplit[9].replace(',', '')
            #print productSplit[11]
            productCls.status = codes.getStatus('naeiltour', productSplit[11])                    # 공백 : 예약가능, 03 : 마감임박, 05 : 마감
            #if tourkind == 'W':
                #productCls.city = productSplit[13]
            productCls.url = 'URL'
            productCls.productname = 'productName'
            productCls.dTime = ''
            productCls.aDay = ''
            productCls.aTime = ''
                
        if period != '' and tourkind == 'F':
            if product.find('<td width="134">') > -1:
                productCls.period = period
                #print productCls.toString()
                productCls.airCode = product[product.find('.gif') - 2:product.find('.gif')]
                query = savefilegethtml.getDetailMergeQueryTest1('naeiltour', 'productcode', productCls.code, productCls.productname, '20' + productCls.dDay, '', 'ICN', '', productCls.airCode, productCls.status, productCls.url, productCls.price, '0', '0', '0', '', '') 
                #print query
                #break
        
        if period == '' and tourkind == 'F':
            if product.find('<td class="FRIDAYSPACING" >') > -1 and product.find('.gif') > -1:
                productCls.airCode = product[product.find('.gif') - 2:product.find('.gif')]
            #<td class="FRIDAYSPACING" width="220"><B><FONT COLOR="RED">569,000원</FONT>2박3일 도미인 아사쿠사 호텔(12박 13일)</td>
            #<td class="FRIDAYSPACING" width="220"><B><FONT COLOR="RED">369,000원</FONT> 2박3일<BR>신주쿠 워싱톤 호텔(더블룸)</td>
            #<td class="FRIDAYSPACING" width="220"><B><FONT COLOR="RED">569,000원</FONT>(2박3일) 도미인 아사쿠사 호텔</td>

            if product.find('idth="220">') > -1:
                print product
                print type(product)
                splitText = product.split('박'.decode('utf-8'))
                tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[0]))
                print 'Night : ', tmpText[len(tmpText)-1]
                
                tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[1]))
                print 'day : ', tmpText[0]
                #if product.find('(') > -1:
                    #productCls.night = re.findall(r"\d", product.split('(')[1])[0]
                    #productCls.period = re.findall(r"\d", product.split('(')[1])[1]
                #elif product.find('[') > -1:
                    #productCls.night = re.findall(r"\d", product.split('[')[1])[0]
                    #productCls.period = re.findall(r"\d", product.split('[')[1])[1]
                #print productCls.toString()
                query = savefilegethtml.getDetailMergeQueryTest1('naeiltour', 'productcode', productCls.code, productCls.productname, '20' + productCls.dDay, '', 'ICN', '', productCls.airCode, productCls.status, productCls.url, productCls.price, '0', '0', '0', '', productCls.night) 
                #print 'Query : ' + query
                #break
        
        if period == '' and tourkind == 'W':
            if product.find('valign="middle"') > -1:
                print product
                print type(product)
                splitText = product.split('박'.decode('utf-8'))
                if len(splitText) > 1:
                    tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[0]))
                    print 'Night : ', tmpText[len(tmpText)-1]
                    
                    tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[1]))
                    print 'day : ', tmpText[0]
                else:
                    print 'empty..'
                #print productCls.toString()
                query = savefilegethtml.getDetailMergeQueryTest1('naeiltour', 'productcode', productCls.code, productCls.productname, '20' + productCls.dDay, '', productCls.period, 'ICN', '', productCls.airCode, productCls.status, productCls.url, productCls.price, '0', '0', '0', '', productCls.night) 
                #print 'Query : ' + query
                #break
        
        if period == '' and tourkind == 'G':
            if  product.find('valign="middle"') > -1:
                print product
                print type(product)
                splitText = product.split('박'.decode('utf-8'))
                tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[0]))
                print 'Night : ', tmpText[len(tmpText)-1]
                
                tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[1]))
                print 'day : ', tmpText[0]
                #print productCls.toString()
                query = savefilegethtml.getDetailMergeQueryTest1('naeiltour', 'productcode', productCls.code, productCls.productname, '20' + productCls.dDay, '', productCls.period, 'ICN', '', productCls.airCode, productCls.status, productCls.url, productCls.price, '0', '0', '0', '', productCls.night) 
                #print 'Query : ' + query
                #break
        
        if period == '' and tourkind == 'D':
            if product.find('<td class="FRIDAYSPACING" >') > -1 and product.find('.gif') > -1:
                productCls.airCode = product[product.find('.gif') - 2:product.find('.gif')]
                
            if product.find('idth="220">') > -1:
                print product
                print type(product)
                splitText = product.split('박'.decode('utf-8'))
                tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[0]))
                print 'Night : ', tmpText[len(tmpText)-1]
                
                tmpText = re.findall('[\^0-9]+', tourUtil.getRemovedHtmlTag(splitText[1]))
                print 'day : ', tmpText[0]
                    
                if product.find('COLOR=BLUE>') > -1:
                    departCity = 'PUS'
                else:
                    departCity = 'ICN'
                
                #print productCls.toString()
                query = savefilegethtml.getDetailMergeQueryTest1('naeiltour', 'productcode', productCls.code, productCls.productname, '20' + productCls.dDay, '', productCls.period, 'ICN', '', productCls.airCode, productCls.status, productCls.url, productCls.price, '0', '0', '0', '', productCls.night) 
                #print 'Query : ' + query
                #break
