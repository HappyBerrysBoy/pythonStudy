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

import sys
import cx_Oracle
import savefilegethtml
import time, datetime
from time import localtime, strftime
from datetime import timedelta

class clsRegionUrl():
    def __init__(self):
        self.url = ''
        self.region = ''
        
    def toString(self):
        return self.region + ' : ' + self.url

class clsProduct():
    def __init__(self):
        self.productname = ''
        self.price = ''
        self.dDay = ''
        self.dTime = ''
        self.aDay = ''
        self.aTime = ''
        self.period = ''
        self.airCode = ''
        self.status = ''
        self.url = ''
        self.code = ''
        self.productCode = ''
        self.airchk = ''
    
    def toString(self):
        val = 'name:'+self.productname+',price:'+self.price+',dDay:'+self.dDay+',dTime:'+self.dTime+',aDay:'+self.aDay+',aTime:'+self.aTime
        val += ',period:'+self.period+',airCode:'+self.airCode+',status:'+self.status+',url:'+self.url+',code:'+self.code+',productCode:'+self.productCode+',airchk:'+self.airchk
        return val

def searchProduct(productcode, productName, period, targetUrl, listUrl, productDetailUrl, departCity, tourkind):
    detailHtml = savefilegethtml.getHtml(targetUrl, '', '', 'naeiltourDetailHtml.txt')
    exceptFile = open('verygoodtourException.txt', 'w')
    print >> exceptFile, targetUrl
    departDayList = list()
    for detail_each_line in detailHtml:
        if detail_each_line.find("fn_goodDetail('") > -1:
            departDayList.append(detail_each_line.split("fn_goodDetail('")[1].split("'")[0])
            
    # 출발 가능 날짜에 항공사 찾아오는 부분
    try:
        con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
        for dayInfo in departDayList:
            productListUrl = listUrl + productcode + '&sel_day=' + dayInfo
            print 'ProductListUrl : ' + productListUrl
            productListHtml = savefilegethtml.getHtml(productListUrl, '', '', 'naeiltourproductListHtml.txt')
            print >> exceptFile, productListUrl
            for product in productListHtml:
                if product.find("fn_price('") > -1:
                    productCls = clsProduct()
                    productSplit = product.split('fn_price')[1].split("'")
                    productCls.productCode = productSplit[1]
                    productCls.dDay = productSplit[3]
                    productCls.code = productSplit[5]
                    productCls.airCode = productSplit[7]
                    productCls.price = productSplit[9].replace(',', '')
                    productCls.status = productSplit[11]                    # 공백 : 예약가능, 03 : 마감임박, 05 : 마감
                    productCls.url = productDetailUrl + productcode + '&sel_day=' + productCls.dDay
                    productCls.productname = productName
                    productCls.period = period
                    productCls.dTime = ''
                    productCls.aDay = ''
                    productCls.aTime = ''
                    query = "insert into product_test values (product_seq.nextval, 'naeiltour','','"   # Region 늘릴필요 있음... 10자리로 모자름..
                    query += productCls.productname + "','" + departCity + "',to_date('" + productCls.dDay + "'),'"
                    query += "','" + tourkind + "','',to_char(sysdate, 'yyyymmdd'),''," + productCls.price + ",'" + productCls.url
                    query += "','','','" + productCls.status + "','" + productCls.airCode +"')"
                    #print 'Query : ' + query
                    cursor = con.cursor()
                    cursor.execute(query)
                    con.commit()
                    #break
                    #print productCls.toString()
    except:
        print >> exceptFile, "Parcing Error:", sys.exc_info()[0]
        pass
    finally:
        exceptFile.close()
        con.close()

print "Start : %s" % time.ctime()

homepageUrl = 'http://www.naeiltour.co.kr'

#배낭여행 시작========================================

print '@@@@@@@@@@@@@ backpack start @@@@@@@@@@@@@@@@@@@@'
backpackUrl = 'http://www.naeiltour.co.kr/backpack/eu_main.asp?area=40'
mainHtml = savefilegethtml.getHtml(backpackUrl, '<div id="left_mn">', '<div id="left_mn2">', 'naeiltourbackpackHtml.txt')

comment = False
backpackMenuList = list()       #menu들 List
try:
    for each_line in mainHtml:
        if comment == False and each_line.find('/backpack/list.asp?') > -1:
            backpackRegionClass = clsRegionUrl()
            backpackRegionClass.url = homepageUrl + each_line.split('href="')[1].split('"')[0]
            if each_line.find('">-') > -1:
                backpackRegionClass.region = each_line.split('">-')[1].split('<')[0].strip()
            elif each_line.find('alt="') > -1:
                backpackRegionClass.region = each_line.split('alt="')[1].split('"')[0]
            backpackMenuList.append(backpackRegionClass)
            
        if each_line.find('<!--') > -1:
            comment = True
            
        if each_line.find('-->') > -1:
            comment = False
except:
    print "Backpack Parcing Error1:", sys.exc_info()[0]
    pass

try:
    for menu in backpackMenuList:
        #tit_position2 부산출발 검색조건..
        productListHtml = savefilegethtml.getHtml(menu.url, '<div id="sub_box2">', 'function btn(ckbtn){', 'productListHtml.txt')
        
        for each_line in productListHtml:
            if each_line.find('<h1 class="bic_h">') > -1:
                productName = each_line.split('bic_h">')[2].split('<')[0]
                productNameSplit = productName.split(' ')
                period = productNameSplit[len(productNameSplit)-1].replace('일', '')
            
            if each_line.find("sview('") > -1:
                productCode = each_line.split("sview('")[1].split("'")[0]
                code2 = each_line.split("sview('")[1].split("'")[2]
                detailUrl = 'http://www.naeiltour.co.kr/backpack/program_include_list.asp?good_cd='+ productCode + '&obj=' + code2
                
                listUrl = 'http://www.naeiltour.co.kr/backpack/program_include_list.asp?good_cd='
                productDetailUrl = 'http://www.naeiltour.co.kr/backpack/show.asp?good_cd='
                searchProduct(productCode, productName, period, detailUrl, listUrl, productDetailUrl, 'seoul', 'backpack')
                break
        break
except:
    print "Backpack Parcing Error2:", sys.exc_info()[0]
    pass
#배낭여행 완료========================================
#자유여행 시작========================================
print '@@@@@@@@@@@@@ freetour start @@@@@@@@@@@@@@@@@@@@'
freetourUrl = 'http://www.naeiltour.co.kr/friday/eu/index.asp'
mainHtml = savefilegethtml.getHtml(freetourUrl, '<div id="Leftmenu" style="align:left;">', '<!-- Theme Select -->', 'naeiltourfreetourkHtml.txt')

comment = False
parcingStart = False
freetourMenuList = list()
try:
    for each_line in mainHtml:
        if each_line.find('<!--') > -1:
            comment = True
            
        if comment == False and each_line.find('3Depth_R') > -1:
            parcingStart = True
           
        if comment == False and parcingStart and each_line.find(' href="') > -1:
            freetourRegionClass = clsRegionUrl()
            tmpNames = each_line.split('alt="')
            tmpUrls = each_line.split('href="')
            
            chkIdx = 0
            urlIdx = 1
            for name in tmpNames:
                if chkIdx % 2 == 1:
                    freetourRegionClass = clsRegionUrl()
                    freetourRegionClass.region = name.split('"')[0]
                    freetourRegionClass.url = homepageUrl + tmpUrls[urlIdx].split('"')[0]
                    freetourMenuList.append(freetourRegionClass)
                    urlIdx += 1
                chkIdx += 1
    
        if comment == False and each_line.find('</tr>') > -1:
            parcingStart = False
    
        if each_line.find('-->') > -1:
            comment = False
except:
    print "Freetour Parcing Error1:", sys.exc_info()[0]
    pass

try:
    for regionList in freetourMenuList:
        #print aa.toString()
        productHtml = savefilegethtml.getHtml(regionList.url, '<td width="200">', '<td width=200>', 'naeiltourproductHtml.txt')
        
        for product_line in productHtml:
            if product_line.find('<td height="137"') > -1:
                productName = product_line.split('alt="')[1].split('"')[0]
                productUrl = homepageUrl + product_line.split('..')[1].split("'")[0]
                productCode = product_line.split('good_cd=')[1].split('&')[0]
                
                #productUrl은 상품 세부 정보를 모두 가지고 있는 url인데... 여기서 한번더 프로그램 조회를 눌러야만 출발일, 항공사가 나오므로.. 바로 출발일 나오는 주소 찾자..
                #바로 출발일 http://www.naeiltour.co.kr/friday/program/program_include.asp?good_cd=24020052
                productScheduleUrl = homepageUrl + '/friday/program/program_include.asp?good_cd=' + productCode
                print productScheduleUrl
                
                #detailProduct = urllib2.urlopen(productScheduleUrl).read()
                #http://www.naeiltour.co.kr/friday/friday.asp?good_cd=24020052&nat_cd=FR&city_cd=&sub_area_cd=
                listUrl = 'http://www.naeiltour.co.kr/friday/program/program_include.asp?good_cd='
                productDetailUrl = 'http://www.naeiltour.co.kr/friday/friday.asp?good_cd='
                
                searchProduct(productCode, productName, '', productScheduleUrl, listUrl, productDetailUrl, 'seoul', 'freetour')
                break
        break
except:
    print "Freetour Parcing Error2:", sys.exc_info()[0]
    pass
#자유여행 완료========================================clsRegionUrl
#허니문 시작========================================
print '@@@@@@@@@@@@@ honeymoon start @@@@@@@@@@@@@@@@@@@@'
honeymoonUrl = 'http://www.naeiltour.co.kr/jagiya/main.asp'
mainHtml = savefilegethtml.getHtml(honeymoonUrl, 'HDropdown-orange-classic', '<map name="cum_event" id="cum_event">', 'naeiltourhoneykHtml.txt')

comment = False
honeymoonMenuList = list()
areacodeList = list()
areacodeList.append('start')
try:
    for each_line in mainHtml:
        if each_line.find('<!--') > -1:
            comment = True
            
        if comment == False and each_line.find('/jagiya/honeymoon/list.asp') > -1:
            sub_area_code = each_line.split('sub_area_cd=')[1].split('"')[0]
            if areacodeList.count(sub_area_code) < 1:
                areacodeList.append(sub_area_code)
                honeymoonCls = clsRegionUrl()
                honeymoonCls.region = each_line.split('alt="')[1].split('"')[0]
                honeymoonCls.url = homepageUrl + each_line.split('href="')[1].split('"')[0]
                honeymoonMenuList.append(honeymoonCls)
    
        if each_line.find('-->') > -1:
            comment = False
except:
    print "Honeymoon Parcing Error1:", sys.exc_info()[0]
    pass

# 부산 출발 조건  <td
try:
    for regionList in honeymoonMenuList:
        regionHtml = savefilegethtml.getHtml(regionList.url, '<td', '<!--<div id="footer">', 'naeiltourproductHtml.txt')
        
        productName = ''
        productListUrl = ''
        
        for region in regionHtml:
            if region.find('<li >') > -1:
                productName = region.split('alt="')[1].split('"')[0]
                productCode = region.split('good_cd=')[1].split('&')[0]
                productListUrl = homepageUrl + '/jagiya/honeymoon/program_include.asp?good_cd=' + productCode
                
                listUrl = 'http://www.naeiltour.co.kr/jagiya/honeymoon/program_include.asp?good_cd='
                productDetailUrl = 'http://www.naeiltour.co.kr/jagiya/honeymoon/view.asp?good_cd='
                searchProduct(productCode, productName, '', productListUrl, listUrl, productDetailUrl, 'seoul', 'honeymoon')
                
                break
        break                    
except:
    print "Honeymoon Parcing Error2:", sys.exc_info()[0]
    pass

#허니문 완료========================================
#골프 시작========================================
print '@@@@@@@@@@@@@ golf start @@@@@@@@@@@@@@@@@@@@'
golfUrl = 'http://www.naeiltour.co.kr/GMT/index.asp'
mainHtml = savefilegethtml.getHtml(golfUrl, 'top_menu', 'function move(num) {', 'naeiltourgolfkHtml.txt')

comment = False
golfMenuList = list()
try:
    for each_line in mainHtml:
        if each_line.find('<!--') > -1:
            comment = True
            
        if comment == False and each_line.find("location.href='") > -1 and each_line.find('community') < 0 and each_line.find('event') < 0:
            golfCls = clsRegionUrl()
            golfCls.region = each_line.split('</td>')[0].split('/>')[1]
            golfCls.url = homepageUrl + each_line.split("location.href='")[1].split("'")[0]
            golfMenuList.append(golfCls)
    
        if each_line.find('-->') > -1:
            comment = False
            golfCls = clsRegionUrl()
except:
    print "Golf Parcing Error1:", sys.exc_info()[0]
    pass            

try:
    for regionList in golfMenuList:
        print regionList.toString() 
        
        regionHtml = savefilegethtml.getHtml(regionList.url, '<ul class="lst_type">', '<div id="foot">', 'naeiltourproductHtml.txt')
        
        productName = ''
        productListUrl = ''
        
        for region in regionHtml:
            if region.find("view.asp?good_cd=") > -1:
                print region
                productName = region.split('title">')[1].split('<')[0]
                productCode = region.split('good_cd=')[1].split('&')[0]
                productListUrl = homepageUrl + '/GMT/goods/program_include.asp?good_cd=' + productCode
                
                listUrl = 'http://www.naeiltour.co.kr/GMT/goods/program_include.asp?good_cd='
                productDetailUrl = 'http://www.naeiltour.co.kr/GMT/goods/view.asp?good_cd='
                searchProduct(productCode, productName, '', productListUrl, listUrl, productDetailUrl, 'seoul', 'golf')
                
                break
        break                    
except:
    print "Golf Parcing Error2:", sys.exc_info()[0]
    pass
#골프 완료========================================
#부산출발 시작========================================
print '@@@@@@@@@@@@@ busan start @@@@@@@@@@@@@@@@@@@@'
notseoulUrl = 'http://www.naeiltour.co.kr/naeil21/list_friday.asp?menuId=DA&step_area=40&sub_area_cd=C409'
mainHtml = savefilegethtml.getHtml(notseoulUrl, '<div id="Leftmenu" style="align:left;">', '<!-- Theme Select -->', 'naeiltourbusankHtml.txt')

comment = False
parcingStart = False
busanMenuList = list()
try:
    for each_line in mainHtml:
        if each_line.find('<!--') > -1:
            comment = True
            
        if comment == False and each_line.find('3Depth_R') > -1:
            parcingStart = True
           
        if comment == False and parcingStart and each_line.find(' href="') > -1:
            freetourRegionClass = clsRegionUrl()
            tmpNames = each_line.split('alt="')
            tmpUrls = each_line.split('href="')
            
            chkIdx = 0
            urlIdx = 1
            for name in tmpNames:
                if chkIdx % 2 == 1:
                    busanMenuClass = clsRegionUrl()
                    busanMenuClass.region = name.split('"')[0]
                    busanMenuClass.url = homepageUrl + tmpUrls[urlIdx].split('"')[0]
                    busanMenuList.append(busanMenuClass)
                    urlIdx += 1
                chkIdx += 1
    
        if comment == False and each_line.find('</tr>') > -1:
            parcingStart = False
    
        if each_line.find('-->') > -1:
            comment = False
except:
    print "Busan Parcing Error1:", sys.exc_info()[0]
    pass

try:
    for regionList in busanMenuList:
        print regionList.toString()
        
        regionHtml = savefilegethtml.getHtml(regionList.url, '<!--loop start-->', '<!--loop end-->', 'naeiltourproductHtml.txt')
        
        productName = ''
        productListUrl = ''
        
        for region in regionHtml:
            if region.find('<td height="137"') > -1:
                productName = region.split('alt="')[1].split('"')[0]
                productCode = region.split('good_cd=')[1].split('&')[0]
                #productListUrl = homepageUrl + region.split("window.open('")[1].split("'")[0]
                productScheduleUrl = homepageUrl + '/friday/program/program_include.asp?good_cd=' + productCode
    
                listUrl = 'http://www.naeiltour.co.kr/friday/program/program_include.asp?good_cd='
                productDetailUrl = 'http://www.naeiltour.co.kr/friday/friday.asp?good_cd='
                searchProduct(productCode, productName, '', productScheduleUrl, listUrl, productDetailUrl, 'busan', 'busan')
                #C4020071
                break
        break  
except:
    print "Busan Parcing Error2:", sys.exc_info()[0]
    pass                
#부산출발 완료========================================

print "End : %s" % time.ctime()