# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 02:29:14 2014

@author: KSC
"""

import datetime
import sys
import cx_Oracle
import savefilegethtml
import codes
import urllib2

def valueParcing(html, idx1, idx2):
    return html[html.find(idx1) + len(idx1):html.find(idx2)]
 
class clsPackage():
    def __init__(self):
        self.tot_cnt = 0
        self.pub_area_code = ''
        self.pub_country = ''
        self.pub_city = ''
        self.dept_code = ''
        self.DY_LIST = ''
        self.page_num = ''
        self.page_len = ''
        self.flatfile_yn = ''
        self.productList = list()
    
    def toString(self):
        return 'tot_cnt:'+self.tot_cnt+',pub_area_code:'+self.pub_area_code+',pub_country:'+self.pub_country+',pub_city:'+self.pub_city+',dept_code:'+self.dept_code+',DY_LIST:'+self.DY_LIST+',page_num:'+self.page_num+',page_len:'+self.page_len+',flatfile_yn:'+self.flatfile_yn
 
 
class clsProduct():
    def __init__(self):
        self.sort_no = ''
        self.pkg_mst_code = ''
        self.sMonth = ''
        self.min_amt = ''
        self.max_amt = ''
        self.mst_name = ''
        self.t_content = ''
        self.img_seq = ''
        self.dy_list = ''
        self.content = ''
        self.tour_day = ''
        self.start_dy = ''
        self.orderSeq = ''
        
    def toString(self):
        return 'sort_no:'+self.sort_no+',pkg_mst_code:'+self.pkg_mst_code+',sMonth:'+self.sMonth+',min_amt:'+self.min_amt+',max_amt:'+self.max_amt+',mst_name:'+self.mst_name+',t_content:'+self.t_content+',img_seq:'+self.img_seq+',dy_list:'+self.dy_list+',content:'+self.content+',tour_day:'+self.tour_day+',start_dy:'+self.start_dy+',orderSeq:'+self.orderSeq
    

packageClass = clsPackage()
jsonUrl = 'http://www.hanatour.com/asp/booking/productPackage/pk-11000-list.asp?area=A&pub_country=TH&pub_city=PYX&etc_code=P&hanacode=overseas_GNB_AE_TH_PYX'
html = urllib2.urlopen(jsonUrl).read()
packageClass.tot_cnt = valueParcing(html, 'tot_cnt":"', '","pub')
packageClass.pub_area_code = valueParcing(html, 'pub_area_code":"', '","pub_country')
packageClass.pub_country = valueParcing(html, 'pub_country":"', '","pub_city')
packageClass.pub_city = valueParcing(html, 'pub_city":"', '","dept_code')
packageClass.dept_code = valueParcing(html, 'dept_code":"', '","DY_LIST')
packageClass.DY_LIST = valueParcing(html, 'DY_LIST":"', '","page_num')
packageClass.page_num = valueParcing(html, 'page_num":"', '","page_len')
packageClass.page_len = valueParcing(html, 'page_len":"', '","flatfile_yn')
packageClass.flatfile_yn = valueParcing(html, 'flatfile_yn":"', '"}, "cont"')
print packageClass.toString()

#contentsList = savefilegethtml.getHtmlList(html, '{"sort_no":', '] })', savefilegethtml.chkExistFile('contentsFile.txt'), '{', '\r\n{')

contents = html[html.find('[{"sort_no":') + 1:html.find('] })')].replace('{', '\r\n{')
contentsFileName = savefilegethtml.chkExistFile('contentsFile.txt')
#contentsList = savefilegethtml.htmlToList(contents, 'contentsFile.txt')
contentsFile = open(contentsFileName, 'w')
print >> contentsFile, contents
contentsFile.close()
contentsList = open(contentsFileName)

con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")

for product in contentsList:
    con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
    try:
        pkg_mst_code = valueParcing(product, 'pkg_mst_code":"', '","sMonth')
        #print 'product : ' + product
        if len(product.strip()) < 1:
            continue
        
        productClass = clsProduct()
        productClass.sort_no = valueParcing(product, 'sort_no":"', '","pkg_mst_code')
        productClass.pkg_mst_code = pkg_mst_code
        productClass.sMonth = valueParcing(product, 'sMonth":"', '","min_amt')
        productClass.min_amt = valueParcing(product, 'min_amt":"', '","max_amt')
        productClass.max_amt = valueParcing(product, 'max_amt":"', '","mst_name').replace("'", "")
        productClass.mst_name = valueParcing(product, 'mst_name":"', '","t_content').replace("'", "").decode('utf-8')
        productClass.t_content = valueParcing(product, 't_content":"', '","img_seq').replace("'", "")
        productClass.img_seq = valueParcing(product, 'img_seq":"', '","dy_list')
        productClass.dy_list = valueParcing(product, 'dy_list":"', '","content')
        productClass.content = valueParcing(product, '"content":"', '","tour_day').replace("'", "").decode('utf-8')
        productClass.tour_day = valueParcing(product, 'tour_day":"', '","start_dy')
        productClass.start_dy = valueParcing(product, 'start_dy":"', '","orderSeq')
        productClass.orderSeq = valueParcing(product, 'orderSeq":"', '"}')
        
        # 2014. 6. 29. 정규식으로 이름에서 국가, 도시 코드 빼오도록.. 테스트 디비로 저장..
        
        codeList = codes.getCityCode(productClass.mst_name)
        nationList = codeList[0]
        cityList = codeList[1]
        print codeList
        query = savefilegethtml.getMasterMergeQueryTest1('hanatour', productClass.pkg_mst_code, packageClass.pub_area_code, packageClass.pub_country, packageClass.pub_city, productClass.mst_name, 'P', 'A', productClass.content, '', nationList, cityList)
        print query
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
    except:
        pass

con.close()