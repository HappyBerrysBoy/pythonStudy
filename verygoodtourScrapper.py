# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 23:37:36 2014

@author: KSC
"""

import urllib2
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import sys
import cx_Oracle

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
        
    def toString(self):
        return 'Code:'+self.code+',sDay:'+self.sDay+',sTime:'+self.sTime+',aDay:'+self.aDay+',aTime:'+self.aTime+',aCode:'+self.aCode+',Period:'+self.period+',status:'+self.status+',name:'+self.name+',price:'+self.price+',booked:'+self.booked

# 시간 변수들..
today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)
        
sitemapUrl = 'http://www.verygoodtour.com/Content/SiteMap.html'
sitemapHtml = urllib2.urlopen(sitemapUrl).read()

sitemapHtmlFile = open('sitemapHtml.txt', 'w')
print >> sitemapHtmlFile, sitemapHtml
sitemapHtmlFile.close()

menulist = list()           # 메뉴 Url 들을 담고 있을 clsProduct들의 List
sitemapHtml = open('sitemapHtml.txt')
try:
    for each_line in sitemapHtml:
        if len(each_line.strip()) > 0 and each_line.find('<li>') > -1 and each_line.find('/Product/Package/PackageList') > -1 and each_line.find('id=') < 0:
            productCls = clsProductGroup()
            productCls.name = each_line.split('MenuCode=')[1].split('>')[1].split('<')[0]
            productCls.menucode = each_line.split('MenuCode=')[1].split('"')[0]
            productCls.url = 'http://www.verygoodtour.com' + each_line.split('a href="')[1].split('"')[0]
            menulist.append(productCls)
            #print 'name:' + productCls.name + ', url:' + productCls.url
except:
    print "Parcing or Query Error:", sys.exc_info()[0]
    pass

productListFile = open('verygoodProductList.txt', 'w')
productList = list()        # 중복으로 같은 상품 안가져 오도록 List에 넣고.. 없는 것들만 들고오도록..
productList.append('init')
for menu in menulist:
    try:
        print '=============================================================================================================='
        print 'PackageList Url : ' + menu.url
        regionHtml = urllib2.urlopen(menu.url).read()
        regionHtml = regionHtml[regionHtml.find('<div id="list_proviewM">'):regionHtml.find('function BingPaging()')]
        regionHtmlFile = open('regionHtml.txt', 'w')
        print >> regionHtmlFile, regionHtml
        regionHtmlFile.close()
        
        regionHtml = open('regionHtml.txt')
        try:
            for each_line in regionHtml:
                if each_line.find('img_ov_text2') > -1:
                    #Detail Product List 가져오는 URL...
                    productListUrl = 'http://www.verygoodtour.com/Product/Package/PackageItem?MasterCode=' + each_line.split("('")[1].split("')")[0] + '&Month=' + strftime("%m", time) + '&Year=' + strftime("%Y", time)
                    print 'ProductGroup Url : ' + productListUrl
                    productListHtml = urllib2.urlopen(productListUrl).read()
                    productListHtmlFile = open('productListHtml.txt', 'w')
                    print >> productListHtmlFile, productListHtml
                    productListHtmlFile.close()

                    #최종 상품들 잡아넣자..
                    try:
                        productCls = clsProduct()
                        productListHtml = open('productListHtml.txt')
                        for product in productListHtml:
                            if product.find('class="pro_date"') > -1:
                                productCls = clsProduct()
                                productCls.sDay = strftime("%Y", time) + '/' + product.split('pro_date">')[1].split('(')[0].strip()
                                print productCls.sDay
                                productCls.sTime = product.split('<br/>')[0].split(')')[1].strip()
                                print productCls.sTime
                                productCls.aDay = strftime("%Y", time) + '/' + product.split('<span>')[1].split('(')[0].strip()
                                print productCls.aDay
                                productCls.aTime = product.split('<span>')[1].split(')')[1].split('<')[0].strip()
                                print productCls.aTime
                            elif product.find('class="pro_air"') > -1:
                                productCls.aCode = product.split('</td>')[0].split('<br/>')[1]
                            elif product.find('박') > -1 and product.find('class=') < 0:
                                productCls.period = product.split('>')[1].split('<')[0]
                            elif product.find('class="pro_detail tl"') > -1:
                                productCls.code = product.split("DetailPage('")[1].split("'")[0]
                                tmp = len(product.split('</td>')[0].split('>'))
                                productCls.name = product.split('</td>')[0].split('>')[tmp - 1]
                            elif product.find('class="pro_price"') > -1:
                                productCls.price = product.split('원')[0].split('>')[1].replace(',', '')
                            elif product.find('class="pro_condition"') > -1:
                                productCls.booked = product.split('title="')[1].split('석')[0].strip()
                            elif product.find('</tr>') > -1:
                                #query... 등등
                                print >> productListFile, productCls.toString()
                    except IndexError as iErr:
                        print iErr.message + '(' + product + ')'
                    except:
                        print "Parcing Error:", sys.exc_info()[0]
                        pass
                    finally:
                        productListHtml.close()
                        
        except:
            print "Parcing or URL Error:", sys.exc_info()[0]
            pass
        finally:
            regionHtml.close()
    except:
        print "URL Open Error:", sys.exc_info()[0]
        pass
    
    break
sitemapHtml.close()
productListFile.close()
