# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 23:37:36 2014

@author: KSC
"""

import time, datetime
import sys
import savefilegethtml
import codes
import tourUtil
import tourQuery
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
        self.url = ''
        self.night = ''
        
    def toString(self):
        return 'Code:'+self.code+',sDay:'+self.sDay+',sTime:'+self.sTime+',aDay:'+self.aDay+',aTime:'+self.aTime+',aCode:'+self.aCode+',Period:'+self.period+',status:'+self.status+',name:'+self.name+',price:'+self.price+',booked:'+self.booked

def getTourType(idx):
    if idx == 0:
        return codes.getTourKind('verygoodtour', 'P')
    elif idx == 1:
        return codes.getTourKind('verygoodtour', 'F')
    elif idx == 2:
        return codes.getTourKind('verygoodtour', 'D')
    elif idx == 3:
        return codes.getTourKind('verygoodtour', 'PUS')
    elif idx == 4:
        return codes.getTourKind('verygoodtour', 'W')
    elif idx == 5:
        return codes.getTourKind('verygoodtour', 'G')
    elif idx == 6:
        return codes.getTourKind('verygoodtour', 'Luxury')
    elif idx == 7:
        return codes.getTourKind('verygoodtour', 'Air')
    elif idx == 8:
        return codes.getTourKind('verygoodtour', 'Hotel')
    elif idx == 9:
        return codes.getTourKind('verygoodtour', 'Company')
    else:
        return 'No'
    
# 시간 변수들..
tourAgency = 'vgtour'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
#targetYear = '2014'
#targetMonth = '07'
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

exceptFile = open('verygoodtourException' + scrappingStartTime + '.txt', 'w')
print >> exceptFile, "Start : %s" % time.ctime()
        
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
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
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
                print '=============================================================================================================='
                print 'PackageList Url : ' + productGroupCls.url
                print >> exceptFile, 'PackageList Url : ' + productGroupCls.url
                #if productGroupCls.url.find('1020101') < 0:
                    #continue
                regionHtml = savefilegethtml.getHtml(productGroupCls.url, '<div id="list_proviewM">', 'function BingPaging()', 'regionHtml.txt')
                #regionHtml = urllib2.urlopen(menu.url).read()
                #regionHtml = regionHtml[regionHtml.find('<div id="list_proviewM">'):regionHtml.find('function BingPaging()')]
                #regionHtmlFile = open('regionHtml.txt', 'w')
                #print >> regionHtmlFile, regionHtml
                #regionHtmlFile.close()
                
                #regionHtml = open('regionHtml.txt')
                try:
                    mastercode = ''
                    
                    con = tourQuery.getOracleConnection()
                    for each_line in regionHtml:
                        if each_line.find('img_ov_text2') > -1:
                            #Detail Product List 가져오는 URL...
                            mastercode = each_line.split("('")[1].split("')")[0]
                        elif each_line.find('class="title"') > -1:
                            if productList.count(mastercode) > 0:
                                #print 'MasterCode : ' + mastercode + '  ==>filtering.. same mastercode'
                                print >> exceptFile, 'MasterCode : ' + mastercode + '  ==>filtering.. same mastercode'
                            else:
                                productList.append(mastercode)
                                productListUrl = 'http://www.verygoodtour.com/Product/Package/PackageItem?MasterCode=' + mastercode + '&Month=' + targetMonth + '&Year=' + targetYear
                                print 'ProductGroup Url : ' + productListUrl
                                print >> exceptFile, 'ProductGroup Url : ' + productListUrl
                                productListHtml = savefilegethtml.getHtml(productListUrl, '', '', 'productListHtml.txt')
                                productName = each_line.split('<a href="#n">')[1].split('</a')[0].replace("'", "").strip().decode('utf-8')
                                productComment = each_line.split('pkg_list_centents">')[1].split('</a')[0].replace("'", "").strip().decode('utf-8')
                                
                                if mastercode.strip() == '' or productName.strip() == '' or productComment.strip() == '':
                                    continue
                                
                                # 2014. 7. 23. 카테고리의 국가는 넣지 않기로 함...
                                #codeList = codes.getCityCode(productName, productGroupCls.name, productComment)
                                codeList = codes.getCityCode(productName, productComment)
                                cityList = codeList[0]
                                nationList = codeList[1]
                                continentList = codeList[2]
                                siteList = codeList[3]              # 2014. 8. 3. site 추가
                                
                                if len(cityList) == 0 and len(nationList) == 0 and len(continentList) == 0:
                                    codeList = codes.getCityCode(productGroupCls.name)
                                    cityList = codeList[0]
                                    nationList = codeList[1]
                                    continentList = codeList[2]
                                    siteList = codeList[3]              # 2014. 8. 3. site 추가
                                
                                query = tourQuery.getMasterMergeQuery(tourAgency, mastercode, productName, tourType, region, productComment, '')  # A : 해외(Abroad)
                                #query = savefilegethtml.getMasterMergeQuery('vgtour', mastercode, '', '', productGroupCls.name, productName, tourType, region, productComment, '')  # A : 해외(Abroad)
                                #print query
                                cursor = con.cursor()
                                cursor.execute(query)
                                con.commit()
                                codes.insertRegionData(tourAgency, mastercode, cityList, nationList, continentList, siteList)
                                
                                
                                #최종 상품들 잡아넣자..
                                try:
                                    productCls = clsProduct()
                                    #productListHtml = open('productListHtml.txt')
                                    departConfirm = False
                                    for product in productListHtml:
                                        #print 'product : ' + product
                                        if product.find('pro_date') > -1:
                                            productCls = clsProduct()
                                            departConfirm = False
                                            #productCls.sDay = targetYear + product.split('pro_date">')[1].split('(')[0].strip().replace('/', '')
                                            #productCls.sTime = product.split('<br/>')[0].split(')')[1].strip().replace(':', '')
                                            #productCls.aDay = targetYear + product.split('<span>')[1].split('(')[0].strip().replace('/', '')
                                            #productCls.aTime = product.split('<span>')[1].split(')')[1].split('<')[0].strip().replace(':', '')
                                            daySplit = tourUtil.getNumArray(tourUtil.getRemovedHtmlTag(product))
                                            productCls.sDay = ''
                                            productCls.sTime = ''
                                            productCls.aDay = ''
                                            productCls.aTime = ''
                                            
                                            if len(daySplit) > 1:
                                                productCls.sDay = targetYear + daySplit[0] + daySplit[1]
                                            if len(daySplit) > 3:
                                                productCls.sTime = daySplit[2] + daySplit[3]
                                            if len(daySplit) > 5:
                                                productCls.aDay = targetYear + daySplit[4] + daySplit[5]
                                            if len(daySplit) > 7:
                                                productCls.aTime = daySplit[6] + daySplit[7]
                                        elif product.find('<img src=') > -1 and product.find('pro_detail') < 0:
                                            #productCls.aCode = product.split("alt='")[1].split("'")[0].decode('utf-8')      # 이건 한글 항공사 뽑아오는부분.. 영문2자리로 뽑자.. gif 파일명에서 뽑자
                                            productCls.aCode = product[product.find('.gif') - 4:product.find('.gif') - 2]
                                        elif (product.find('박') > -1 or product.find('일') > -1) and product.find('class=') < 0:
                                            productCls.night = product.split('박')[0].split('>')[1].strip()
                                            productCls.period = product.split('박')[1].split('일')[0].strip()
                                        elif product.find('class="pro_detail tl"') > -1:
                                            productCls.code = product.split("DetailPage('")[1].split("'")[0]
                                            productCls.url = 'http://www.verygoodtour.com/Product/Package/PackageDetail?ProCode=' + productCls.code + '&MenuCode=' + productGroupCls.menucode
                                            #http://www.verygoodtour.com/Product/Package/PackageDetail?ProCode=APP5099-140612LJ&MenuCode=1010201
                                            tmp = len(product.split('</td>')[0].split('>'))
                                            #print >> exceptFile, product.split('</td>')[0].split('>')[tmp - 1]
                                            if product.find('출발확정') > -1:
                                                departConfirm = True
                                            productCls.name = product.split('</td>')[0].split('>')[tmp - 1].replace("'", "").decode('utf-8')
                                        elif product.find('pro_price') > -1:
                                            productCls.price = product.split('원')[0].split('>')[1].replace(',', '')
                                        elif product.find('class="pro_condition"') > -1:
                                            #print >> exceptFile, product.split('title="')[1].split('"')[0]
                                            
                                            if product.find('예약마감') > -1:
                                                productCls.booked = codes.getStatus('verygoodtour', '예약마감')
                                            elif product.find('대기예약') > -1:
                                                productCls.booked = codes.getStatus('verygoodtour', '대기예약')
                                            elif departConfirm:
                                                productCls.booked = codes.getStatus('verygoodtour', '출발확정')
                                            elif product.find('예약하기') > -1 or product.find('석') > -1:
                                                productCls.booked = codes.getStatus('verygoodtour', '예약하기')
                                            else:
                                                productCls.booked = codes.getStatus('verygoodtour', 'None')
                                                
                                            #productCls.booked = product.split('title="')[1].split('"')[0].split(' ')[0].decode('utf-8')
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
                                            
                                            query = tourQuery.getDetailMergeQuery(tourAgency, mastercode, productCls.code, productCls.name, productCls.sDay+productCls.sTime, productCls.aDay+productCls.aTime, productCls.period, departCity, '', productCls.aCode, productCls.booked, productCls.url, productCls.price, '0', '0', '0', '', productCls.night) 
                                            #print query
                                            cursor = con.cursor()
                                            cursor.execute(query)
                                            con.commit()
                                            #break
                                except:
                                    print 'data base error!!!'
                                    print >> exceptFile, "Parcing Error:", sys.exc_info()[0]
                                    pass
                                
                            #break
                except:
                    print >> exceptFile, "Parcing or URL Error:", sys.exc_info()[0]
                    pass
                    
            except:
                print >> exceptFile, "URL Open Error:", sys.exc_info()[0]
                pass
            
            #break
except:
    print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
    pass

#sitemapHtml.close()
print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()

query = tourQuery.updDepArrYMD(tourAgency, targetYear, targetMonth)
cursor = con.cursor()
cursor.execute(query)
con.commit()
con.close()