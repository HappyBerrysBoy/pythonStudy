# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 23:37:36 2014

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
    
# 시간 변수들..
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

exceptFile = open('verygoodtourException' + scrappingStartTime + '.txt', 'w')
        
sitemapUrl = 'http://www.verygoodtour.com/Content/SiteMap.html'
sitemapHtml = savefilegethtml.getHtml(sitemapUrl, '', '', 'sitemapHtml.txt')
#sitemapHtml = urllib2.urlopen(sitemapUrl).read()
#sitemapHtmlFile = open('sitemapHtml.txt', 'w')
#print >> sitemapHtmlFile, sitemapHtml
#sitemapHtmlFile.close()
#sitemapHtml = open('sitemapHtml.txt')
#menulist = list()           # 메뉴 Url 들을 담고 있을 clsProduct들의 List
tourType = ''
departCity = ''
region = ''
depthIdx = 0
idx = 0
productList = list()        # 중복으로 같은 상품 안가져 오도록 List에 넣고.. 없는 것들만 들고오도록..
productList.append('START')

try:
    for each_line in sitemapHtml:
        if each_line.find('class="depth_2 ') > -1:
            tourType = getTourType(idx)
            if idx == 2:
                region = 'D'
            else:
                region = 'A'
                
            if idx == 3:
                departCity = 'PUS'
            else:
                departCity = 'ICN'
                
            idx += 1
        elif len(each_line.strip()) > 0 and each_line.find('<li>') > -1 and each_line.find('/Product/Package/PackageList') > -1 and each_line.find('id=') > -1:
            if each_line.find('부산출발') > -1:
                departCity = 'PUS'
            else:
                departCity = 'ICN'            
        elif len(each_line.strip()) > 0 and each_line.find('<li>') > -1 and each_line.find('/Product/Package/PackageList') > -1 and each_line.find('id=') < 0:
            #print each_line
            productGroupCls = clsProductGroup()
            productGroupCls.name = each_line.split('MenuCode=')[1].split('>')[1].split('<')[0].decode('utf-8')
            productGroupCls.menucode = each_line.split('MenuCode=')[1].split('"')[0]
            productGroupCls.url = 'http://www.verygoodtour.com' + each_line.split('a href="')[1].split('"')[0] + '&PageSize=200'
            #menulist.append(productCls)
            #print 'name:' + productCls.name + ', url:' + productCls.url
            
            try:
                idx += 1
                print '=============================================================================================================='
                print 'PackageList Url : ' + productGroupCls.url
                print >> exceptFile, 'PackageList Url : ' + productGroupCls.url
                regionHtml = savefilegethtml.getHtml(productGroupCls.url, '<div id="list_proviewM">', 'function BingPaging()', 'regionHtml.txt')
                #regionHtml = urllib2.urlopen(menu.url).read()
                #regionHtml = regionHtml[regionHtml.find('<div id="list_proviewM">'):regionHtml.find('function BingPaging()')]
                #regionHtmlFile = open('regionHtml.txt', 'w')
                #print >> regionHtmlFile, regionHtml
                #regionHtmlFile.close()
                
                #regionHtml = open('regionHtml.txt')
                try:
                    mastercode = ''
                    
                    con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
                    for each_line in regionHtml:
                        if each_line.find('img_ov_text2') > -1:
                            #Detail Product List 가져오는 URL...
                            mastercode = each_line.split("('")[1].split("')")[0]
                        elif each_line.find('class="title"') > -1:
                            if productList.count(mastercode) > 0:
                                print 'MasterCode : ' + mastercode + '  ==>filtering.. same mastercode'
                                print >> exceptFile, 'MasterCode : ' + mastercode + '  ==>filtering.. same mastercode'
                            else:
                                productList.append(mastercode)
                                productListUrl = 'http://www.verygoodtour.com/Product/Package/PackageItem?MasterCode=' + mastercode + '&Month=' + targetMonth + '&Year=' + targetYear
                                print 'ProductGroup Url : ' + productListUrl
                                print >> exceptFile, 'ProductGroup Url : ' + productListUrl
                                productListHtml = savefilegethtml.getHtml(productListUrl, '', '', 'productListHtml.txt')
                                productName = each_line.split('<a href="#n">')[1].split('</a')[0].replace("'", "").strip().decode('utf-8')
                                productComment = each_line.split('pkg_list_centents">')[1].split('</a')[0].replace("'", "").strip().decode('utf-8')
                                #productListHtml = urllib2.urlopen(productListUrl).read()
                                #productListHtmlFile = open('productListHtml.txt', 'w')
                                #print >> productListHtmlFile, productListHtml
                                #productListHtmlFile.close()
                                
                                #print 'mastercode : ' + mastercode
                                if mastercode.strip() == '' or productName.strip() == '' or productComment.strip() == '':
                                    continue
                                
                                query = savefilegethtml.getMasterMergeQuery('vgtour', mastercode, '', '', productGroupCls.name, productName, tourType, region, productComment, '')  # A : 해외(Abroad)
                                #print query
                                cursor = con.cursor()
                                cursor.execute(query)
                                con.commit()
            
                                #최종 상품들 잡아넣자..
                                try:
                                    con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")                    
                                    productCls = clsProduct()
                                    #productListHtml = open('productListHtml.txt')
                                    for product in productListHtml:
                                        #print 'product : ' + product
                                        if product.find('pro_date') > -1:
                                            productCls = clsProduct()
                                            productCls.sDay = targetYear + product.split('pro_date">')[1].split('(')[0].strip().replace('/', '')
                                            productCls.sTime = product.split('<br/>')[0].split(')')[1].strip().replace(':', '')
                                            productCls.aDay = targetYear + product.split('<span>')[1].split('(')[0].strip().replace('/', '')
                                            productCls.aTime = product.split('<span>')[1].split(')')[1].split('<')[0].strip().replace(':', '')
                                        elif product.find('<img src=') > -1 and product.find('pro_detail') < 0:
                                            productCls.aCode = product.split("alt='")[1].split("'")[0].decode('utf-8')
                                        elif (product.find('박') > -1 or product.find('일') > -1) and product.find('class=') < 0:
                                            productCls.period = product.split('박')[1].split('일')[0].strip()
                                        elif product.find('class="pro_detail tl"') > -1:
                                            productCls.code = product.split("DetailPage('")[1].split("'")[0]
                                            productCls.url = 'http://www.verygoodtour.com/Product/Package/PackageDetail?ProCode=' + productCls.code + '&MenuCode=' + productGroupCls.menucode
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
                                            if productCls.code.strip() == '':
                                                continue
                                            
                                            query = savefilegethtml.getDetailMergeQuery('vgtour', mastercode, productCls.code, productCls.name, productCls.sDay+productCls.sTime, productCls.aDay+productCls.aTime, productCls.period, departCity, '', productCls.aCode, productCls.booked, productCls.url, productCls.price, '0', '0', '0', '') 
                                            #print query
                                            cursor = con.cursor()
                                            cursor.execute(query)
                                            con.commit()
                                            #break
                                except IndexError as iErr:
                                    print iErr
                                    pass
                                except:
                                    print 'data base error!!!'
                                    print >> exceptFile, "Parcing Error:", sys.exc_info()[0]
                                    pass
                            #break
                except cx_Oracle.IntegrityError as dberr2:
                    print dberr2
                    print >> exceptFile, dberr2
                    pass
                except cx_Oracle.DatabaseError as dberr:
                    print dberr
                    print >> exceptFile, dberr
                    pass
                except UnicodeDecodeError as err:
                    print err
                    print >> exceptFile, err
                    pass
                except:
                    print >> exceptFile, "Parcing or URL Error:", sys.exc_info()[0]
                    pass
                finally:
                    con.close()
                    
            except:
                print >> exceptFile, "URL Open Error:", sys.exc_info()[0]
                pass
            
            #break
except:
    print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
    pass

#sitemapHtml.close()
exceptFile.close()