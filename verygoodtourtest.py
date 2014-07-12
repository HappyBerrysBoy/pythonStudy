# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 12:54:12 2014

@author: KSC
"""
import re
import tourUtil
import savefilegethtml
import codes
import sys
import cx_Oracle

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


print '=============================================================================================================='
print 'PackageList Url : http://www.verygoodtour.com/Product/Package/PackageList?MenuCode=101092103&PageSize=200'
regionHtml = savefilegethtml.getHtml('http://www.verygoodtour.com/Product/Package/PackageList?MenuCode=101092103&PageSize=200', '<div id="list_proviewM">', 'function BingPaging()', 'regionHtml.txt')
#regionHtml = urllib2.urlopen(menu.url).read()
#regionHtml = regionHtml[regionHtml.find('<div id="list_proviewM">'):regionHtml.find('function BingPaging()')]
#regionHtmlFile = open('regionHtml.txt', 'w')
#print >> regionHtmlFile, regionHtml
#regionHtmlFile.close()

#regionHtml = open('regionHtml.txt')
mastercode = ''

con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
for each_line in regionHtml:
    if each_line.find('img_ov_text2') > -1:
        #Detail Product List 가져오는 URL...
        mastercode = each_line.split("('")[1].split("')")[0]
    elif each_line.find('class="title"') > -1:
        productListUrl = 'http://www.verygoodtour.com/Product/Package/PackageItem?MasterCode=' + mastercode + '&Month=07&Year=2014'
        print 'ProductGroup Url : ' + productListUrl
        productListHtml = savefilegethtml.getHtml(productListUrl, '', '', 'productListHtml.txt')
        productName = each_line.split('<a href="#n">')[1].split('</a')[0].replace("'", "").strip().decode('utf-8')
        productComment = each_line.split('pkg_list_centents">')[1].split('</a')[0].replace("'", "").strip().decode('utf-8')
        
        if mastercode.strip() == '' or productName.strip() == '' or productComment.strip() == '':
            continue
        
        print productName
        print type(productName)
        print productComment
        print type(productComment)
        codeList = codes.getCityCode(productName, '', productComment)
        nationList = codeList[0]
        cityList = codeList[1]
        print nationList
        print cityList        
        
        query = savefilegethtml.getMasterMergeQueryTest1('vgtour', mastercode, '', '', 'AA', productName, 'P', 'ICN', productComment, '', '', '')  # A : 해외(Abroad)
        #query = savefilegethtml.getMasterMergeQuery('vgtour', mastercode, '', '', productGroupCls.name, productName, tourType, region, productComment, '')  # A : 해외(Abroad)
        #print query
        productCls = clsProduct()
        #productListHtml = open('productListHtml.txt')
        departConfirm = False
        
        
        for product in productListHtml:
            #print 'product : ' + product
            if product.find('pro_date') > -1:
                productCls = clsProduct()
                departConfirm = False
                #<td class="pro_date">07/07 (월) 16:15<br/><span>07/09 (수) 21:05</span></td>
                #<td class="pro_date">07/07 (월) <br/><span></span></td>
                #<td class="pro_date">07/28 (월) 09:10<br/><span>08/17 (<span style="color:red;margin-bottom:0;">일</span>) 05:50</span></td>
                daySplit = tourUtil.getNumArray(tourUtil.getRemovedHtmlTag(product))
                productCls.sDay = ''
                productCls.sTime = ''
                productCls.aDay = ''
                productCls.aTime = ''
                
                if len(daySplit) > 1:
                    productCls.sDay = '2014' + daySplit[0] + daySplit[1]
                if len(daySplit) > 3:
                    productCls.sTime = daySplit[2] + daySplit[3]
                if len(daySplit) > 5:
                    productCls.aDay = '2014' + daySplit[4] + daySplit[5]
                if len(daySplit) > 7:
                    productCls.aTime = daySplit[6] + daySplit[7]
                #productCls.sDay = '2014' + product.split('pro_date">')[1].split('(')[0].strip().replace('/', '')
                #productCls.sTime = product.split('<br/>')[0].split(')')[1].strip().replace(':', '')
                #productCls.aDay = '2014' + product.split('<span>')[1].split('(')[0].strip().replace('/', '')
                #productCls.aTime = product.split('<span>')[1].split(')')[1].split('<')[0].strip().replace(':', '')
            elif product.find('<img src=') > -1 and product.find('pro_detail') < 0:
                #productCls.aCode = product.split("alt='")[1].split("'")[0].decode('utf-8')      # 이건 한글 항공사 뽑아오는부분.. 영문2자리로 뽑자.. gif 파일명에서 뽑자
                productCls.aCode = product[product.find('.gif') - 4:product.find('.gif') - 2]
            elif (product.find('박') > -1 or product.find('일') > -1) and product.find('class=') < 0:
                productCls.period = product.split('박')[1].split('일')[0].strip()
            elif product.find('class="pro_detail tl"') > -1:
                productCls.code = product.split("DetailPage('")[1].split("'")[0]
                productCls.url = 'URL'
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
                    
            elif product.find('</tr>') > -1:
                if productCls.code.strip() == '':
                    continue
                
                query = savefilegethtml.getDetailMergeQueryTest1('vgtour', mastercode, productCls.code, productCls.name, productCls.sDay+productCls.sTime, productCls.aDay+productCls.aTime, productCls.period, 'ICN', '', productCls.aCode, productCls.booked, productCls.url, productCls.price, '0', '0', '0', '') 
                #print query
                #cursor = con.cursor()
                #cursor.execute(query)
                #con.commit()
                #break
        #break
con.close()