# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 21:09:59 2014

@author: KSC
"""
import urllib2
import time, datetime
import sys
import savefilegethtml
import re
import codes
import tourQuery
import cx_Oracle

#여행코드 영어4자리 + 숫자
# 영어 4자리가 뜻하는건... 첫번째 자리 : 국가, 두번째 자리 : 지역 세번째 자리 : 여행종류(P:패키지, H:허니문, G:골프, C:크루즈, S:유럽??, 등..), 네번재 자리 : 출발지역(S:서울, B:부산, D:대구)
# 예약마감, 바로예약, 예약접수

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
        self.comment = ''
        #self.arriveAirport = ''
        self.dTime = ''
        self.aTime = ''
        self.airCode = ''
        self.night = ''
    
    def toString(self):
        return 'productCode:'+self.productCode+',productName:'+self.productname+',period:'+self.period+',comment:'+self.comment+',dTime:'+self.dTime+',aTime:'+self.aTime+',airCode:'+self.airCode+',night:'+self.night

class clsDetailProduct():
    def __init__(self):
        self.dDay = ''
        self.price = ''
        self.status = ''
        self.url = ''
        self.detailCode = ''
        
    def toString(self):
        return 'dDay:'+self.dDay+',Price:'+self.price+',status:'+self.status+',url:'+self.url
        
# 시간 변수들..
tourAgency = 'tourbaksa'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
#targetYear = '2014'
#targetMonth = '07'
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

reload(sys)
sys.setdefaultencoding('utf-8')

homepageUrl = 'http://www.tourbaksa.com'
homepageHtml = urllib2.urlopen(homepageUrl).read()
homepageHtml = homepageHtml[homepageHtml.find('<div class="menuList">'):homepageHtml.find('<ul class="etcMenu">') + len('<ul class="etcMenu">')]
homepageHtml = savefilegethtml.htmlToList(homepageHtml, 'tourbaksaHomepageHtml.txt')
#homepageHtmlFile = open('tourbaksaHomepageHtml.txt', 'w')
#print >> homepageHtmlFile, homepageHtml
#homepageHtmlFile.close()

menulist = list()           # 메뉴 Url 들을 담고 있을 clsProduct들의 List
productGroupCls = clsTotalGroup()
tourkindGroupCls = clsTourKindGroup()
regionUrlGroupCls = clsRegionUrlGroup()

#homepageHtml = open('tourbaksaHomepageHtml.txt')
for each_line in homepageHtml:
    if each_line.find('<ul id="city') > -1:
        if len(productGroupCls.tourkindgroup) > 0:
            menulist.append(productGroupCls)
        productGroupCls = clsTotalGroup()
        if each_line.find('city1') > -1:
            productGroupCls.departCity = 'ICN'
        elif each_line.find('city2') > -1:
            productGroupCls.departCity = 'PUS'
        else:
            productGroupCls.departCity = 'TAE'
    elif each_line.find('href="/submain/?') > -1 or each_line.find('href="/SubMain/index.asp?') > -1 or (each_line.find('<li>') < 0 and (each_line.find('Areaindex.asp') > -1 or each_line.find('areaindex.asp') > -1)):
        tourkindGroupCls = clsTourKindGroup()
        tourkindGroupCls.url = each_line.split('href="')[1].split('">')[0]
        #tourkindGroupCls.tourkind = each_line.split('>')[1].split('<')[0]  # Code명 통일하자..
        tourkindGroupCls.tourkind = codes.getTourKind('tourbaksa', each_line.split('>')[1].split('<')[0].strip().decode('cp949'))
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
        
#homepageHtml.close()

exceptFile = open('tourbaksaException'+scrappingStartTime+'.txt', 'w')
print >> exceptFile, "Start : %s" % time.ctime()

print menulist

con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")

# 메뉴에 다 잘들어 갔나 확인..
for level1 in menulist:
    for level2 in level1.tourkindgroup:
        for level3 in level2.regionUrlGroup:
            print 'Depart City : ' + level1.departCity + ', TourKind:' + level2.tourkind + ', Region : ' + level3.region + '(' + level3.url + ')'
            
            try:
                print >> exceptFile, level3.url
                regionHtml = savefilegethtml.getHtml(level3.url, '<div class="leftArea">', '</nav><!-- //lnb -->', 'tourbaksaRegionHtml.txt', '', '')
                
                for each_line in regionHtml:
                    if each_line.find('<li class="') > -1 and each_line.find('M1=') > -1:
                        #print each_line
                        cityClass = clsCityUrlGroup()
                        cityClass.city = each_line.split('</a>')[0].split(">")[2]
                        cityClass.url = homepageUrl + each_line.split("href='")[1].split("'")[0]
                        
                        print 'Depart Url : ' + cityClass.url
                        try:
                            print >> exceptFile, cityClass.url
                            departListHtml = savefilegethtml.getHtml(cityClass.url, '<div class="list"  id="itemList" >', '', 'tourbaksaDepartListHtml.txt')
                            
                            try:
                                productList = clsProductList()
                                
                                for departList in departListHtml:
                                    if departList.find('<h4>') > -1:
                                        productList = clsProductList()
                                        productList.productname = departList.split('>-->')[1].split('</h4>')[0].replace("'", "")
                                    elif departList.find('<p class="note">') > -1:
                                        tmpTxt = departList.split('<p class="note">')[1].split('→')[0]
                                        productList.comment = tmpTxt[:len(tmpTxt)-5].strip()
                                        productList.dTime = tmpTxt[len(tmpTxt)-5:].strip()
                                        tmpList = departList.split(':')
                                        productList.aTime = tmpList[len(tmpList)-2][len(tmpList[len(tmpList)-2])-2:] + ':' + tmpList[len(tmpList)-1][:2]
                                    elif departList.find('class="detail">') > -1:
                                        
                                        productList.night = re.findall(r"\d", departList.split('class="detail">')[1])[0]
                                        productList.period = re.findall(r"\d", departList.split('class="detail">')[1])[1]                                        
                                        
                                        #productList.period = departList.split('class="detail">')[1].split('박'.decode('utf-8'))[0]
                                        #productList.night = departList.split('class="detail">')[1].split('박'.decode('utf-8'))[0]
                                        #productList.airCode = departList.split('alt="')[1].split('"')[0]        # 이거는 한글 여행사 코드이고... 영문가져오는거 새로 아랫줄에서..
                                        productList.airCode = departList[departList.find('.gif') - 2:departList.find('.gif')]
                                        productList.productCode = departList.split('"itemNum detail">')[1].split('<')[0]
                                    elif departList.find('<div style="') > -1:
                                        #sample.. 에릅네...'http://www.tourbaksa.com/xml/item_Index_List.asp?gy=JTBS&gs=215&AirIDX=3&sd=20140601&M1=1&M2=8&M3=9&M4=15&M5=617'
                                        detailProductUrl = homepageUrl + '/xml/item_Index_List.asp?gy='+productList.productCode[:4]+'&gs='+productList.productCode[4:].split('-')[0]
                                        detailProductUrl += '&AirIDX='+productList.productCode.split('-')[1]+'&sd='+targetYear + targetMonth + '01&'
                                        detailProductUrl += cityClass.url.split('?')[1]
                                        print 'Detail Product Url : ' + detailProductUrl
                                        #print productList.toString()

                                        try:
                                            print >> exceptFile, detailProductUrl
                                            detailProductHtml = urllib2.urlopen(detailProductUrl).read()
                                            detailProductHtml = detailProductHtml[detailProductHtml.find('<tbody id'):detailProductHtml.find('<p class="seeMore"')]
                                            detailProductHtml = detailProductHtml.replace('<td class=', '\r\n<td class=')
                                            detailProductHtml = savefilegethtml.htmlToList(detailProductHtml, 'detailProductHtml.txt')
                                            
                                            
                                            codeList = codes.getCityCode(productList.productname, cityClass.city, productList.comment, level3.region)
                                            cityList = codeList[0]
                                            nationList = codeList[1]
                                            continentList = codeList[2]
                                            
                                            
                                            query = tourQuery.getMasterMergeQuery(tourAgency, productList.productCode, productList.productname, level2.tourkind, 'A', productList.comment, '')  # A : 해외(Abroad)
                                            #print query
                                            cursor = con.cursor()
                                            cursor.execute(query)
                                            con.commit()
                                            codes.insertRegionData(tourAgency, productList.productCode, cityList, nationList, continentList)
                                            
                                            
                                            try:
                                                detailProductCls = clsDetailProduct()
                                                waitSeat = False

                                                for detailProduct in detailProductHtml:
                                                    #print 'Detail Product : ' + detailProduct
                                                    if detailProduct.find('startDate">') > -1:
                                                        detailProductCls = clsDetailProduct()
                                                        waitSeat = False
                                                        detailProductCls.dDay = targetYear + detailProduct.split('startDate">')[1].split('(')[0].replace('.', '')    #20140611
                                                    elif detailProduct.find('price">') > -1:
                                                        #detailProductCls.price = detailProduct.split('price">')[1].split('원')[0].replace(',', '')       #130000
                                                        detailProductCls.price = re.findall(r'\d+', detailProduct.split('price">')[1].replace(',', ''))[0]
                                                    elif detailProduct.find('status') > -1:
                                                        if detailProduct.find('대기예약'.encode('cp949')) > -1:
                                                            waitSeat = True
                                                    elif detailProduct.find('<td class="reservation">') > -1:
                                                        detailProductCls.url = homepageUrl + detailProduct.split("location.href='")[1].split("'")[0]
                                                        if detailProduct.find('예약마감'.encode('cp949')) > -1:
                                                            detailProductCls.status = codes.getStatus('tourbaksa', '예약마감')
                                                        elif detailProduct.find('바로예약'.encode('cp949')) > -1:
                                                            detailProductCls.status = codes.getStatus('tourbaksa', '바로예약')
                                                        elif waitSeat and detailProduct.find('예약접수'.encode('cp949')) > -1:
                                                            detailProductCls.status = codes.getStatus('tourbaksa', '대기예약')
                                                        elif detailProduct.find('예약접수'.encode('cp949')) > -1:
                                                            detailProductCls.status = codes.getStatus('tourbaksa', '예약접수')
                                                        else:
                                                            detailProductCls.status = codes.getStatus('tourbaksa', 'None')
                                                        #detailProductCls.status = detailProduct.split('</button>')[0].split('>')[2]
                                                        detailProductCls.detailCode = detailProduct.split('EV_YM=')[1].split('&')[0] + detailProduct.split('EV_SEQ=')[1].split('&')[0]
                                                        #print detailProductCls.toString()
                                                        
                                                        query = tourQuery.getDetailMergeQuery(tourAgency, productList.productCode, detailProductCls.detailCode, productList.productname, detailProductCls.dDay, '', productList.period, level1.departCity, '', productList.airCode, detailProductCls.status, detailProductCls.url, detailProductCls.price, '0', '0', '0', '', productList.night) 
                                                        #print 'Query : ' + query
                                                        cursor = con.cursor()
                                                        cursor.execute(query)
                                                        con.commit()
                                                        #break
                                                        
                                            except:
                                                print >> exceptFile, 'Detail Product Parcing Error', sys.exc_info()[0]
                                                pass
                                            
                                        except:
                                            print >> exceptFile, 'Detail Product URL Error', sys.exc_info()[0]
                                            pass
                                        
                                        #break
                                    
                            except:
                                print >> exceptFile, 'Depart List Parcing Error', sys.exc_info()[0]
                                pass
                            
                        except:
                            print >> exceptFile, 'Depart Url Error', sys.exc_info()[0]
                            pass

            except IndexError as ierr:
                print >> exceptFile, ierr
            except:
                print >> exceptFile, 'Region url error', sys.exc_info()[0]
                pass
    
            #break
        #break
    #break

print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()
con.commit()
con.close()