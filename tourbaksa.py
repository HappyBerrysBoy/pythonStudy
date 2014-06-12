# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 21:09:59 2014

@author: KSC
"""
import urllib2
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import sys
import cx_Oracle

#여행코드 영어4자리 + 숫자
# 영어 4자리가 뜻하는건... 첫번째 자리 : 국가, 두번째 자리 : 지역 세번째 자리 : 여행종류(P:패키지, H:허니문, G:골프, C:크루즈, S:유럽??, 등..), 네번재 자리 : 출발지역(S:서울, B:부산, D:대구)

class clsRegionUrlGroup():
    def __init__(self):
        self.region = ''
        self.url = ''

class clsTourKindGroup():
    def __init__(self):
        self.tourkind = ''
        self.url = ''
        self.regionUrlGroup = list()        
        
class clsTotalGroup():
    def __init__(self):
        self.departCity = ''
        self.tourkindgroup = list()
        
class clsCityUrlGroup():
    def __init__(self):
        self.city = ''
        self.url = ''
        
class clsProductList():
    def __init__(self):
        self.productCode = ''
        self.productname = ''
        self.period = ''
        self.departAirport = ''
        self.arriveAirport = ''
        self.dTime = ''
        self.aTime = ''
        self.airCode = ''

class clsDetailProduct():
    def __init__(self):
        self.dDay = ''
        self.price = ''
        self.status = ''
        self.url = ''
        
#oracle 10g 접속정보
host = 'hnctech73.iptime.org'
port = 1521
dbase = 'ora11g'
login = 'bigtour'
passwrd = 'bigtour'
#dsn = cx_Oracle.makedsn(host, port, dbase)
#con = cx_Oracle.connect(login, passwrd, dsn)

# 시간 변수들..
today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)


homepageUrl = 'http://www.tourbaksa.com'
homepageHtml = urllib2.urlopen(homepageUrl).read()
homepageHtml = homepageHtml[homepageHtml.find('<div class="menuList">'):homepageHtml.find('<ul class="etcMenu">') + len('<ul class="etcMenu">')]
homepageHtmlFile = open('tourbaksaHomepageHtml.txt', 'w')
print >> homepageHtmlFile, homepageHtml
homepageHtmlFile.close()

menulist = list()           # 메뉴 Url 들을 담고 있을 clsProduct들의 List
productGroupCls = clsTotalGroup()
tourkindGroupCls = clsTourKindGroup()
regionUrlGroupCls = clsRegionUrlGroup()

homepageHtml = open('tourbaksaHomepageHtml.txt')
for each_line in homepageHtml:
    if each_line.find('<ul id="city') > -1:
        if len(productGroupCls.tourkindgroup) > 0:
            menulist.append(productGroupCls)
        productGroupCls = clsTotalGroup()
        if each_line.find('city1') > -1:
            productGroupCls.departCity = 'seoul'
        elif each_line.find('city2') > -1:
            productGroupCls.departCity = 'busan'
        else:
            productGroupCls.departCity = 'daegu'
    elif each_line.find('href="/submain/?') > -1 or each_line.find('href="/SubMain/index.asp?') > -1 or (each_line.find('<li>') < 0 and (each_line.find('Areaindex.asp') > -1 or each_line.find('areaindex.asp') > -1)):
        tourkindGroupCls = clsTourKindGroup()
        tourkindGroupCls.url = each_line.split('href="')[1].split('">')[0]
        tourkindGroupCls.tourkind = each_line.split('>')[1].split('<')[0]
    elif each_line.find('<li>') > -1 and each_line.find('<!--') < 0 and each_line.find('-->') < 0 and (each_line.find('Areaindex') > -1 or each_line.find('areaindex') > -1 or each_line.find('M1=') > -1):
        regionUrlGroupCls = clsRegionUrlGroup()
        regionUrlGroupCls.region = each_line.split('</a>')[0].split('">')[1]
        regionUrlGroupCls.url = homepageUrl + each_line.split('href="')[1].split('"')[0]
        tourkindGroupCls.regionUrlGroup.append(regionUrlGroupCls)
    elif each_line.find('</ul>') > -1:
        if productGroupCls.tourkindgroup.count(tourkindGroupCls) < 1:
            productGroupCls.tourkindgroup.append(tourkindGroupCls)
    elif each_line.find('class="etcMenu"') > -1:
        menulist.append(productGroupCls)
        
homepageHtml.close()

exceptFile = open('tourbaksaException.txt', 'w')

# 메뉴에 다 잘들어 갔나 확인..
for level1 in menulist:
    for level2 in level1.tourkindgroup:
        for level3 in level2.regionUrlGroup:
            print 'Depart Cith : ' + level1.departCity + ', TourKind:' + level2.tourkind + ', Region : ' + level3.region + '(' + level3.url + ')'
            
            try:
                print >> exceptFile, level3.url
                regionHtml = urllib2.urlopen(level3.url).read()
                regionHtml = regionHtml[regionHtml.find('<div class="leftArea">'):regionHtml.find('</nav><!-- //lnb -->')]
                regionHtmlFile = open('tourbaksaRegionHtml.txt', 'w')
                print >> regionHtmlFile, regionHtml
                regionHtmlFile.close()
                
                regionHtml = open('tourbaksaRegionHtml.txt')
                for each_line in regionHtml:
                    if each_line.find('<li class="') > -1 and each_line.find('M1=') > -1:
                        cityClass = clsCityUrlGroup()
                        cityClass.city = each_line.split('</a>')[0].split("' >")[1]
                        cityClass.url = homepageUrl + each_line.split("href='")[1].split("'")[0]
                        
                        print 'Depart Url : ' + cityClass.url
                        try:
                            print >> exceptFile, cityClass.url
                            departListHtml = urllib2.urlopen(cityClass.url).read()
                            departListHtml = departListHtml[departListHtml.find('<div class="list"  id="itemList" >'):]
                            departListHtmlFile = open('tourbaksaDepartListHtml.txt', 'w')
                            print >> departListHtmlFile, departListHtml
                            departListHtmlFile.close()
                            
                            departListHtml = open('tourbaksaDepartListHtml.txt')
                            try:
                                productList = clsProductList()
                                for departList in departListHtml:
                                    if departList.find('<h4>') > -1:
                                        productList = clsProductList()
                                        productList.productname = departList.split('>-->')[1].split('</h4>')[0]
                                    elif departList.find('<p class="note">') > -1:
                                        tmpTxt = departList.split('<p class="note">')[1].split('→')[0]
                                        productList.departAirport = tmpTxt[:len(tmpTxt)-5].strip()
                                        productList.dTime = tmpTxt[len(tmpTxt)-5:].strip()
                                        tmpList = departList.split(':')
                                        productList.aTime = tmpList[len(tmpList)-2][len(tmpList[len(tmpList)-2])-2:] + ':' + tmpList[len(tmpList)-1][:2]
                                    elif departList.find('class="detail">') > -1:
                                        productList.period = departList.split('class="detail">')[1].split('박'.decode('utf-8'))[0]
                                        productList.airCode = departList.split('alt="')[1].split('"')[0]
                                        productList.productCode = departList.split('"itemNum detail">')[1].split('<')[0]
                                    elif departList.find('<div style="') > -1:
                                        #sample.. 에릅네...'http://www.tourbaksa.com/xml/item_Index_List.asp?gy=JTBS&gs=215&AirIDX=3&sd=20140601&M1=1&M2=8&M3=9&M4=15&M5=617'
                                        detailProductUrl = homepageUrl + '/xml/item_Index_List.asp?gy='+productList.productCode[:4]+'&gs='+productList.productCode[4:].split('-')[0]
                                        detailProductUrl += '&AirIDX='+productList.productCode.split('-')[1]+'&sd='+strftime("%Y", time) + strftime("%m", time) + strftime("%d", time)+'&'
                                        detailProductUrl += cityClass.url.split('?')[1]
                                        print 'Detail Product Url : ' + detailProductUrl

                                        try:
                                            print >> exceptFile, detailProductUrl
                                            detailProductHtml = urllib2.urlopen(detailProductUrl).read()
                                            detailProductHtml = detailProductHtml[detailProductHtml.find('<tbody id'):detailProductHtml.find('<p class="seeMore"')]
                                            detailProductHtml = detailProductHtml.replace('<td class=', '\r\n<td class=')
                                            detailProductHtmlFile = open('detailProductHtml.txt', 'w')
                                            print >> detailProductHtmlFile, detailProductHtml
                                            detailProductHtmlFile.close()
                                            
                                            detailProductHtml = open('detailProductHtml.txt')
                                            try:
                                                detailProductCls = clsDetailProduct()
                                                #con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
                                                dsn = cx_Oracle.makedsn(host, port, dbase)
                                                con = cx_Oracle.connect(login, passwrd, dsn)
                                                for detailProduct in detailProductHtml:
                                                    #print 'Detail Product : ' + detailProduct
                                                    if detailProduct.find('startDate">') > -1:
                                                        detailProductCls = clsDetailProduct()
                                                        detailProductCls.dDay = strftime("%Y", time) + detailProduct.split('startDate">')[1].split('(')[0].replace('.', '')    #20140611
                                                    elif detailProduct.find('price">') > -1:
                                                        detailProductCls.price = detailProduct.split('price">')[1].split('원'.decode('utf-8'))[0].replace(',', '')       #130000
                                                    elif detailProduct.find('<td class="reservation">') > -1:
                                                        detailProductCls.url = homepageUrl + detailProduct.split("location.href='")[1].split("'")[0]
                                                        detailProductCls.status = detailProduct.split('</button>')[0].split('>')[2]
                                                        query = "insert into product_test values (product_seq.nextval, 'tourbaksa','" + level3.region[:5] + "','"   # Region 늘릴필요 있음... 10자리로 모자름..
                                                        query += productList.productname + "','" + level1.departCity + "',to_date('" + detailProductCls.dDay + "'),'" + productList.period 
                                                        query += "','package','',to_char(sysdate, 'yyyymmdd'),''," + detailProductCls.price + ",'" + detailProductCls.url
                                                        query += "','','','" + detailProductCls.status + "','" + productList.airCode +"')"
                                                        #print 'Query : ' + query
                                                        cursor = con.cursor()
                                                        cursor.execute(query)
                                                        con.commit()
                                                        
                                            except:
                                                print >> exceptFile, 'Detail Product Parcing Error', sys.exc_info()[0]
                                                pass
                                            finally:
                                                detailProductHtml.close()
                                                con.close()
                                        except:
                                            print >> exceptFile, 'Detail Product URL Error', sys.exc_info()[0]
                                            pass
                                        
                                        break
                                    
                            except:
                                print >> exceptFile, 'Depart List Parcing Error', sys.exc_info()[0]
                                pass
                            
                            departListHtml.close()
                        except:
                            print >> exceptFile, 'Depart Url Error', sys.exc_info()[0]
                            pass

                regionHtml.close()
            except:
                print >> exceptFile, 'Region url error', sys.exc_info()[0]
                pass
    
            break
        break
    break

exceptFile.close()