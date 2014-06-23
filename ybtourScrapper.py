# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 23:48:18 2014

@author: KSC
"""

import xmltodict
import urllib2
import re
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import cx_Oracle
import sys
import savefilegethtml

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
#print('Product URL : ' + productUrl)
        #productListOpener = urllib2.urlopen(productUrl)
        #productListGet = productListOpener.read()

defaultUrl = 'http://www.ybtour.co.kr/GoodSearch/Area_Menu_XML.asp?'

today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)

targetYear = ''#sys.argv[1]
targetMonth = ''#sys.argv[2]
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

exceptFile = open('ybtourException' + scrappingStartTime + '.txt', 'w')
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
            print 'MenuCD:' + pack['MenuCD'] + ', MenuNM:' + pack['MenuNM'] + ', GoodTypeCD:' + pack['GoodTypeCD'] + ', SBAR:' + pack['SBAR']
            
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
                    print 'MenuCD:' + subpackage.menuCode + ', MenuNM:' + subpackage.menuName + ', GoodTypeCD:' + subpackage.goodTypeCode + ', SBAR:' + str(subpackage.sbar)
                    
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
                            print 'MenuCD:' + sub2package.menuCode + ', MenuNM:' + sub2package.menuName + ', GoodTypeCD:' + sub2package.goodTypeCode + ', SBAR:' + str(sub2package.sbar)
                            
                            print '===========================================productList URL==========================================='
                            defaultproductListUrl = 'http://www.ybtour.co.kr/Goods/' + urlMap[package.menuCode] + '/list.asp?sub_area_cd=' + str(sub2package.sbar)
                            print 'List URL : ' + defaultproductListUrl
                            
                            print >> exceptFile, defaultproductListUrl
                            productList = urllib2.urlopen(defaultproductListUrl).read()
                            codeList = re.findall(r"goodFocus\w*", productList)
                            
                            #today = today.replace(month = today.month + 1)
                            
                            for pcode in codeList:
                                detailProduct = pcode.split('s')[1]
                                thisMonth = str(today.year) + str(today.month).zfill(2)
                                detailProductUrl = 'http://www.ybtour.co.kr/Goods/' + urlMap[package.menuCode] + '/inc_evList_ajax.asp?goodCD=' + detailProduct + '&startDT=' + thisMonth
                                print 'Detail Product URL : ' + detailProductUrl
                                
                                print >> exceptFile, detailProductUrl
                                detailProductList = savefilegethtml.getHtml(detailProductUrl, '', '', 'ybtourTempFile.txt')
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
                                    
                                    
                                    #query = savefilegethtml.getMasterMergeQuery('ybtour', productCode, '', '', sublist.name, productName, tourtype, 'A', productComment, '')  # A : 해외(Abroad)
                                    #print query
                                    #cursor = con.cursor()
                                    #cursor.execute(query)
                                    #con.commit()                            
                                            
                                            
                                    #detailProductList = open('ybtourTempFile.txt')
                                    flag = False
                                    ybtourproductfile = open('ybtourproductfile.txt', 'a')
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
                                                
                                                
                                                #query = savefilegethtml.getDetailMergeQuery('ybtour', detailProduct, prd_code, prd_nm, st_dt+st_time, arr_day+arr_time, tr_term, sublist.startLocation, '', air_cd, prd_status, prd_url, prd_fee, '0', '0', '0', '') 
                                                #print query
                                                #cursor = con.cursor()
                                                #cursor.execute(query)
                                                #con.commit()
                                                
                                                
                                                break
                                            
                                        #productClassList.append(clsProduct)
                                    
                                except:
                                    print "Parcing or Query Error:", sys.exc_info()[0]
                                    print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
                                    pass
                                finally:
                                    ybtourproductfile.close()
                                    #detailProductList.close()
                                    con.close()
                            break
                    except ValueError as err:
                        print 'err message : ' + err.message
                    except:
                        print "ML3 Parcing Error:", sys.exc_info()[0]
                        print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
                        pass
                    break
            except:
                print "ML2 Parcing error:", sys.exc_info()[0]
                print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
                pass
            break
    except:
        print "ML1 Parcing error:", sys.exc_info()[0]
        print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
        pass
except:
    print "urllib2 Error(Main) error:", sys.exc_info()[0]
    print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
finally:
    exceptFile.close()





