# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 23:48:18 2014

@author: KSC
"""

import xmltodict
import urllib2
import re
import time, datetime
import cx_Oracle
import sys
import savefilegethtml
import codes

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
        self.detailcode = ''
#print('Product URL : ' + productUrl)
        #productListOpener = urllib2.urlopen(productUrl)
        #productListGet = productListOpener.read()

defaultUrl = 'http://www.ybtour.co.kr/GoodSearch/Area_Menu_XML.asp?'

#targetYear = '2014'
#targetMonth = '07'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

departCity = ''

exceptFile = open('ybtourException' + scrappingStartTime + '.txt', 'w')
print >> exceptFile, "Start : %s" % time.ctime()
ml1List = list()
ml2List = list()
ml3List = list()
productClassList = list()
try:
    print '===========================================MainUrl==========================================='
    mainUrl = defaultUrl + 'ML=1&MCD='
    print 'Main URL : ' + mainUrl
    print >> exceptFile, mainUrl
    packageListXml = urllib2.urlopen(mainUrl).read()
    packageListDict = xmltodict.parse(packageListXml)
    
    urlMap = dict()
    urlMap['A01'] = 'overseas'
    urlMap['A03'] = 'airtel'
    urlMap['A06'] = 'Honeymoon'
    urlMap['A09'] = 'Golf'
    urlMap['A12'] = 'Domestic'
    urlMap['A15'] = 'Busan'
    urlMap['A18'] = 'Cruise'
    
    try:
        for pack in packageListDict['ROOT']['List']:
            package = classPackage()
            package.menuCode = pack['MenuCD']
            package.menuName = pack['MenuNM']
            package.goodTypeCode = pack['GoodTypeCD']
            package.sbar = pack['SBAR']
            ml1List.append(package)
            #print 'MenuCD:' + pack['MenuCD'] + ', MenuNM:' + pack['MenuNM'] + ', GoodTypeCD:' + pack['GoodTypeCD'] + ', SBAR:' + pack['SBAR']
            
            print '===========================================Sub1 URL==========================================='
            subUrl = defaultUrl + 'ML=2&MCD=' + package.menuCode
            print 'Sub URL : ' + subUrl
            
            print >> exceptFile, subUrl
            packageSub1ListXml = urllib2.urlopen(subUrl).read()
            packageSub1ListDict = xmltodict.parse(packageSub1ListXml)
            
            try:
                for packSub1 in packageSub1ListDict['ROOT']['List']:
                    subpackage = classPackage()
                    subpackage.menuCode = packSub1['MenuCD']
                    subpackage.menuName = packSub1['MenuNM']
                    subpackage.goodTypeCode = packSub1['GoodTypeCD']
                    subpackage.sbar = packSub1['SBAR']
                    ml2List.append(subpackage)
                    #print 'MenuCD:' + subpackage.menuCode + ', MenuNM:' + subpackage.menuName + ', GoodTypeCD:' + subpackage.goodTypeCode + ', SBAR:' + str(subpackage.sbar)
                    
                    print '===========================================Sub2 URL==========================================='
                    sub2Url = defaultUrl + 'ML=3&MCD=' + subpackage.menuCode
                    print 'Sub2 URL : ' + sub2Url
                    print >> exceptFile, sub2Url
                    packageSub2ListXml = urllib2.urlopen(sub2Url).read()
                    packageSub2ListDict = xmltodict.parse(packageSub2ListXml)
                    
                    try:
                        for packSub2 in packageSub2ListDict['ROOT']['List']:
                            sub2package = classPackage()
                            sub2package.menuCode = packSub2['MenuCD']
                            sub2package.menuName = packSub2['MenuNM']
                            sub2package.goodTypeCode = packSub2['GoodTypeCD']
                            sub2package.sbar = packSub2['SBAR']
                            ml3List.append(sub2package)
                            #print 'MenuCD:' + sub2package.menuCode + ', MenuNM:' + sub2package.menuName + ', GoodTypeCD:' + sub2package.goodTypeCode + ', SBAR:' + str(sub2package.sbar)
                            
                            print '===========================================productList URL==========================================='
                            if package.menuCode == 'A15':
                                departCity = 'PUS'
                            else:
                                departCity = 'ICN'
                            
                            defaultproductListUrl = 'http://www.ybtour.co.kr/Goods/' + urlMap[package.menuCode] + '/list.asp?sub_area_cd=' + str(sub2package.sbar)
                            print 'List URL : ' + defaultproductListUrl
                            
                            print >> exceptFile, defaultproductListUrl
                            productList = urllib2.urlopen(defaultproductListUrl).read()
                            codeList = re.findall(r"goodFocus\w*", productList)
                            
                            productNameList = list()
                            productCommentList = list()
                            productNameHtml = productList[productList.find('travel_top_section'):productList.find('frmGD')]
                            productNameHtml = savefilegethtml.htmlToList(productNameHtml, 'xxx.txt')
                            for pdName in productNameHtml:
                                if pdName.find('height="110" alt="') > 0:
                                    productNameList.append(pdName.split('alt="')[1].split('"')[0].replace("'", "").strip().decode('utf-8'))
                                if pdName.find('<p class="desc">') > 0:
                                    productCommentList.append(pdName.split('desc">')[1].split('<')[0].replace("'", "").strip().decode('utf-8'))
                            #today = today.replace(month = today.month + 1)
                            codeIdx = 0
                            
                            for pcode in codeList:
                                detailProduct = pcode.split('s')[1]
                                detailProductUrl = 'http://www.ybtour.co.kr/Goods/' + urlMap[package.menuCode] + '/inc_evList_ajax.asp?goodCD=' + detailProduct + '&startDT=' + targetYear + targetMonth
                                print 'Detail Product URL : ' + detailProductUrl
                                
                                print >> exceptFile, detailProductUrl
                                detailProductList = savefilegethtml.getHtml(detailProductUrl, '', '', 'ybtourTempFile.txt')
                                
                                
#노란풍성 자유여행은... 패키지랑 가져오는 부분이 다름... detail list를.. 달력을 뽑아옴.. 시상에... 아래주소 참고바람..
#http://www.ybtour.co.kr/Goods/overseas/inc_view_cal_dev.asp?Current_DateTime=2014-06-25&good_type_cd=5&area_cd=50&good_yy=2007&good_seq=44&start_day_w=20140625                                
                                
                                
                                #detailProductHtml = urllib2.urlopen(detailProductUrl).read()
                                #tempFile = open('ybtourTempFile.txt', 'w')
                                #print >> tempFile, detailProductHtml
                                #tempFile.close()
                                
                                """
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
                                """

                                try:
                                    con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
                                    
                                    # 2014. 06. 29. 여행상품명에서 국가, 도시코드 가져오는 부분으로 적용..
                                    codeList = codes.getCityCode(productNameList[codeIdx], sub2package.menuName)
                                    nationList = codeList[0]
                                    cityList = codeList[1]
                                    #print productNameList[codeIdx]
                                    #print sub2package.menuName
                                    #print codeList
                                    query = savefilegethtml.getMasterMergeQueryTest1('ybtour', detailProduct, '', subpackage.menuName, sub2package.menuName, productNameList[codeIdx], urlMap[package.menuCode], 'A', productCommentList[codeIdx], '', nationList, cityList)
                                
                                    #query = savefilegethtml.getMasterMergeQuery('ybtour', detailProduct, '', subpackage.menuName, sub2package.menuName, productNameList[codeIdx], urlMap[package.menuCode], 'A', productCommentList[codeIdx], '')  # A : 해외(Abroad)
                                    codeIdx += 1
                                    #print query
                                    cursor = con.cursor()
                                    cursor.execute(query)
                                    con.commit()                            
                                            
                                    #detailProductList = open('ybtourTempFile.txt')
                                    flag = False
                                    #ybtourproductfile = open('ybtourproductfile.txt', 'a')
                                    clsProduct = classProduct()
                                    for parcer in detailProductList:
                                        try:
                                            if parcer.strip()[:len('<td><input type="checkbox"')] == '<td><input type="checkbox"':
                                                flag = True
                                                clsProduct = classProduct()
                                            
                                            if flag:
                                                if parcer.find('<td><span class="blue">') > -1:
                                                    spliter = parcer.strip().split(' ')
                                                    clsProduct.departDay = spliter[1].split('>')[1].replace('/', '').strip()
                                                    clsProduct.departTime = spliter[3].split('<')[0].replace(':', '').strip()
                                                    clsProduct.arriveDay = spliter[4].split('>')[2].replace('/', '').strip()
                                                    clsProduct.arriveTime = spliter[6].split('<')[0].replace(':', '').strip()
                                                    #print >> ybtourproductfile, 'departday:' + str(clsProduct.departDay) + ', departtime:'  + str(clsProduct.departTime) + ', arrDay:' + str(clsProduct.arriveDay) + ', arrTime:' + str(clsProduct.arriveTime)
                                                elif parcer.find('absmiddle') > -1:
                                                    clsProduct.airCode = parcer.replace('"', '').replace("'", "").split("alt=")[1].split(" ")[0].decode('utf-8')
                                                    #print >> ybtourproductfile, 'airCode:' + clsProduct.airCode
                                                elif parcer.find('<td class="lt"><a href="') > -1:
                                                    clsProduct.detailcode = parcer.split('ev_seq=')[1].split('&')[0]
                                                    spliter = parcer.strip().split(' ')
                                                    clsProduct.url = 'http://www.ybtour.co.kr' + spliter[2].split('"')[1]
                                                    spliter = parcer.strip().split('>')
                                                    clsProduct.productName = spliter[2].split('<')[0].replace("'", '').decode('utf-8')
                                                    #print >> ybtourproductfile, 'URL:' + clsProduct.url + ', Name:' + clsProduct.productName
                                                elif parcer.find('박') > -1 and len(parcer) < 9:
                                                    clsProduct.period = parcer.strip()[:1]
                                                    #print >> ybtourproductfile, 'Period:' + clsProduct.period
                                                elif parcer.find('<td class="blue">') > -1 and parcer.find('원') > -1:
                                                    spliter = parcer.strip().split('>')
                                                    clsProduct.price = spliter[1].split('원')[0].replace(',', '')
                                                    #print >> ybtourproductfile, 'Price:' + clsProduct.price
                                                elif parcer.find('출발확정') > -1 or parcer.find('예약마감') > -1 or parcer.find('예약가능') > -1:
                                                    spliter = parcer.strip().split('>')
                                                    clsProduct.status = spliter[1].split('<')[0].decode('utf-8')
                                                    #print >> ybtourproductfile, 'Status:' + clsProduct.status
                                                elif parcer.strip() == '</tr>':
                                                    flag = False
                                                    # 2014. 06. 29. 여행상품명에서 국가, 도시코드 가져오는 부분으로 적용..
                                                    
                                                    query = savefilegethtml.getDetailMergeQueryTest1('ybtour', detailProduct, clsProduct.detailcode, clsProduct.productName, targetYear+clsProduct.departDay+clsProduct.departTime, targetYear+clsProduct.arriveDay+clsProduct.arriveTime, clsProduct.period, departCity, '', clsProduct.airCode, clsProduct.status, clsProduct.url, clsProduct.price, '0', '0', '0', '') 
                                                    #query = savefilegethtml.getDetailMergeQuery('ybtour', detailProduct, clsProduct.detailcode, clsProduct.productName, targetYear+clsProduct.departDay+clsProduct.departTime, targetYear+clsProduct.arriveDay+clsProduct.arriveTime, clsProduct.period, departCity, '', clsProduct.airCode, clsProduct.status, clsProduct.url, clsProduct.price, '0', '0', '0', '') 
                                                    #print query
                                                    cursor = con.cursor()
                                                    cursor.execute(query)
                                                    con.commit()
                                                    #break
                                        except:
                                            print "ML5 Parcing Error:", sys.exc_info()[0]
                                            print >> exceptFile, "ML5 Parcing Error:", sys.exc_info()[0]
                                            pass
                                        #productClassList.append(clsProduct)
                                except UnicodeEncodeError as err1:
                                    print >> exceptFile, err1
                                    pass
                                except:
                                    print "ML4 Parcing Error:", sys.exc_info()[0]
                                    print >> exceptFile, "ML4 Parcing Error:", sys.exc_info()[0]
                                    pass
                                finally:
                                    #ybtourproductfile.close()
                                    #detailProductList.close()
                                    con.close()
                            #break
                    except ValueError as err:
                        print 'ML3-2 Parcing Error : ' + err.message
                        pass
                    except:
                        print "ML3 Parcing Error:", sys.exc_info()[0]
                        print >> exceptFile, "ML3 Parcing Error:", sys.exc_info()[0]
                        pass
                    #break
            except:
                print "ML2 Parcing error:", sys.exc_info()[0]
                print >> exceptFile, "ML2 Parcing Error:", sys.exc_info()[0]
                pass
            #break
    except:
        print "ML1 Parcing error:", sys.exc_info()[0]
        print >> exceptFile, "ML1 Parcing Error:", sys.exc_info()[0]
        pass
except:
    print "urllib2 Error(Main) error:", sys.exc_info()[0]
    print >> exceptFile, "urllib2 Error(Main) error:", sys.exc_info()[0]
    pass

print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()





