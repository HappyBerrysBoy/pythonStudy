# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 06:05:04 2014

@author: KSC
"""


import sys
import urllib2
import time, datetime
import codes
import tourQuery
import cx_Oracle
import savefilegethtml
import tourUtil
import json

#롯데 관광은 메인 메뉴에서 전체 여행 URL을 찾을 수 있음
# 1. 메인메뉴에서 전체 여행 URL 검색해서 Class화
# 2. Json으로 정보를 제공하고, 현지 출발시간, 현지 도착 시간등.. 정보는 꽤 있다... 여유좌석도...

class detailProductCls():
    def __init__(self):
        self.dDay = ''
        self.dTime = ''
        self.aDay = ''
        self.aTime = ''
        self.price = ''
        self.night = ''
        self.period = ''
        self.airCode = ''
        self.status = ''
        self.name = ''
        self.seq = ''
        self.departCity = ''
        self.url = ''

class productCls():
    def __init__(self):
        self.name = ''
        self.detailUrl = ''
        self.productCode = ''

class subMenuCls():
    def __init__(self):
        self.name = ''
        self.url = ''

class mainCls():
    def __init__(self):
        self.name = ''
        self.url = ''
        self.subMenuList = list()

# 시간 변수들..
tourAgency = 'lottetour'
mainUrl = 'http://www.lottetour.com'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
#targetYear = '2014'
#targetMonth = '07'
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

exceptFileName = 'lottetourException' + scrappingStartTime + '.txt'
exceptFile = open(exceptFileName, 'w')
print >> exceptFile, "Start : %s" % time.ctime()

mainpageHtml = savefilegethtml.getHtml('http://www.lottetour.com/welcome', '<nav>', '</nav>', 'onlinetourMainPage.txt')


urlDict = dict()
urlDict['package'] = 'package'
urlDict['free'] = 'fit'
urlDict['honeymoon'] = 'honeymoon'
urlDict['golf'] = 'golf'
urlDict['cruise'] = 'cruise'

startComment = False
firstOversea = True
subMenu = False
mainList = list()
clsMain = mainCls()
clsSubMenu = subMenuCls()
for each_line in mainpageHtml:
    #print main
    if each_line.find('<!--') > -1 :
        startComment = True
    elif each_line.find('-->') > -1:
        startComment = False
        
    if firstOversea and each_line.find('해외패키지') > -1:
        clsMain = mainCls()
        clsMain.name = codes.getTourKind('lottetour', 'package')
        firstOversea = False
    elif not startComment and each_line.find('<li') > -1 and each_line.find('<a href=') > -1:
        clsSubMenu = subMenuCls()
        clsSubMenu.url = mainUrl + tourUtil.getTagAttr(each_line, 'a', 'href')
        if each_line.find('title') > -1:
            clsSubMenu.name = tourUtil.getRemovedHtmlTag(each_line).strip()
            clsMain.subMenuList.append(clsSubMenu)
        else:
            subMenu = True
    elif not startComment and subMenu and each_line.find('title=') > -1:
        clsSubMenu.name = each_line.split('>')[1].split('<')[0]
        clsMain.subMenuList.append(clsSubMenu)
        subMenu = False
    elif each_line.find('sub_depth0') > -1:
        if len(clsMain.subMenuList) > 0:
            clsMain.subMenuList.pop()
    elif each_line.find('class="fit"') > -1 or each_line.find('class="honeymoon _open"') > -1 or each_line.find('class="golf"') > -1 or each_line.find('class="fit"') > -1 or each_line.find('class="cruise line"') > -1 or each_line.find('class="air line"') > -1:
        mainList.append(clsMain)
        clsMain = mainCls()
        clsMain.name = codes.getTourKind('lottetour', tourUtil.getTagAttr(each_line, 'li', 'class'))
        

con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")        
for menu in mainList:
    for sub in menu.subMenuList:
        try:
            print sub.name + ':' + sub.url
            print >> exceptFile, sub.name + ':' + sub.url
            subHtml = savefilegethtml.getHtml(sub.url, 'class="event_result"', 'END : event_list', 'lottetourSubHtml.txt')
            
            for subMenu in subHtml:
                try:
                    if subMenu.find('<dt><a href=') > -1:
                        productCode = subMenu.split('/prdt/')[1].split('?')[0]
                        detailListUrl = mainUrl + '/prdt_event/' + productCode + '/' + targetYear + targetMonth
                        #http://www.lottetour.com/prdt/36558?menu=558       => 소스보기에는 이렇게 나오지만... 아래처럼 json으로도 나온다..
                        #http://www.lottetour.com/prdt_event/36558/201407
                        productName = tourUtil.getRemovedHtmlTag(subMenu).strip().replace("'", "")
                        
                        # 2014. 7. 23. 카테고리의 국가는 넣지 않기로 함...
                        #codeList = codes.getCityCode(productName, sub.name)
                        codeList = codes.getCityCode(productName)
                        cityList = codeList[0]
                        nationList = codeList[1]
                        continentList = codeList[2]
                        siteList = codeList[3]              # 2014. 8. 3. site 추가
                        
                        if len(cityList) == 0 and len(nationList) == 0 and len(continentList) == 0:
                            codeList = codes.getCityCode(sub.name)
                            cityList = codeList[0]
                            nationList = codeList[1]
                            continentList = codeList[2]
                            siteList = codeList[3]              # 2014. 8. 3. site 추가
                        
                        # Master 상품 입력
                        query = tourQuery.getMasterMergeQuery(tourAgency, productCode, productName, menu.name, 'A', '', '')
                        #print query
                        cursor = con.cursor()
                        cursor.execute(query)
                        con.commit()
                        # Region Data 삭제
                        codes.insertRegionData(tourAgency, productCode, cityList, nationList, continentList, siteList)
                        
                        # Detail List Url로 부터 비행기 시간, 금액 등등 찾기
                        # 03:예약마감, 01:예약가능, 04:대기예약
                        print >> exceptFile, 'Detail Url : ' + detailListUrl
                        #print 'Detail Url : ' + detailListUrl
                        detailList = urllib2.urlopen(detailListUrl).read()
                        #print detailList
                        
                        json_loaded = json.loads(detailList)
                        for detail in json_loaded:
                            try:
                                clsDetail = detailProductCls()
                                clsDetail.name = detail['name']
                                clsDetail.night = str(detail['night'])
                                clsDetail.period = str(detail['days'])
                                clsDetail.airCode = detail['airMark']
                                clsDetail.status = codes.getStatus('lottetour', detail['status'])
                                clsDetail.seq = detail['id']
                                clsDetail.price = str(detail['sellingPrice'])
                                clsDetail.dDay = detail['departureAir']['departureDate'].strip()
                                clsDetail.dTime = detail['departureAir']['departureTime'].strip()
                                clsDetail.aDay = detail['entryAir']['arrivalDate'].strip()
                                clsDetail.aTime = detail['entryAir']['arrivalTime'].strip()
                                clsDetail.url = mainUrl + '/evt/' + clsDetail.seq
                                #http://www.lottetour.com/evt/A140721565?menu=558
                                if detail['meetPlace'].find('인천'.decode('utf-8')) > -1:
                                    clsDetail.departCity = 'ICN'
                                elif detail['meetPlace'].find('김해'.decode('utf-8')) > -1:
                                    clsDetail.departCity = 'PUS'
                                elif detail['meetPlace'].find('김포'.decode('utf-8')) > -1:
                                    clsDetail.departCity = 'GMP'
                                else:
                                    clsDetail.departCity = 'ETC'
                                
                                query = tourQuery.getDetailMergeQuery(tourAgency, productCode, clsDetail.seq, clsDetail.name, clsDetail.dDay+clsDetail.dTime, clsDetail.aDay+clsDetail.aTime, clsDetail.period, clsDetail.departCity, '', clsDetail.airCode, clsDetail.status, clsDetail.url, clsDetail.price, '0', '0', '0', '', clsDetail.period) 
                                #print query
                                cursor = con.cursor()
                                cursor.execute(query)
                                con.commit()
                                #print detail['name']
                            except:
                                print "Level3 : ", sys.exc_info()[0]
                                print >> exceptFile, "Level3 : ", sys.exc_info()[0]
                                pass
                        #break
                        
                except:
                    print "Level2 : ", sys.exc_info()[0]
                    print >> exceptFile, "Level2 : ", sys.exc_info()[0]
                    pass
            #break
        except:
            print "Level1 : ", sys.exc_info()[0]
            print >> exceptFile, "Level1 : ", sys.exc_info()[0]
            pass
    #break


query = tourQuery.updDepArrYMD(tourAgency, targetYear, targetMonth)
cursor = con.cursor()
cursor.execute(query)

con.close()
print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()