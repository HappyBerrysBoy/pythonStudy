# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

@author: KSC
"""

import time, datetime
from time import localtime, strftime
from datetime import timedelta
import urllib2
import cx_Oracle
import savefilegethtml
import sys

#fnSetMstList({"head":{"tot_cnt":"17","pub_area_code":"A","pub_country":"TH","pub_city":"","dept_code":"","DY_LIST":"","page_num":"1","page_len":"20","flatfile_yn":"N"}, 
#"cont":[
#{"sort_no":"0","pkg_mst_code":"AAP700","sMonth":"201406","min_amt":"199000","max_amt":"1269000","mst_name":"방콕/파타야 4,5,6일[부산출발] 특가 상품",
#"t_content":"특가 이벤트 상품으로 저렴한 금액으로 즐기는 여행입니다.","img_seq":"P000294303","dy_list":"1,2,3,4,5,6,7","content":"특가 이벤트 상품으로 저렴한 금액으로 즐기는 여행입니다.","tour_day":"5~6",
#"start_dy":"매일","orderSeq":""},

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
        print 'tot_cnt:'+self.tot_cnt+',pub_area_code:'+self.pub_area_code+',pub_country:'+self.pub_country+',pub_city:'+self.pub_city+',dept_code:'+self.dept_code+',DY_LIST:'+self.DY_LIST+',page_num:'+self.page_num+',page_len:'+self.page_len+',flatfile_yn:'+self.flatfile_yn
        
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
        print 'sort_no:'+self.sort_no+',pkg_mst_code:'+self.pkg_mst_code+',sMonth:'+self.sMonth+',min_amt:'+self.min_amt+',max_amt:'+self.max_amt+',mst_name:'+self.mst_name+',t_content:'+self.t_content+',img_seq:'+self.img_seq+',dy_list:'+self.dy_list+',content:'+self.content+',tour_day:'+self.tour_day+',start_dy:'+self.start_dy+',orderSeq:'+self.orderSeq

class clsDetailProduct():
    def __init__(self):
        self.pcode = ''
        self.sday = ''
        self.stime = ''
        self.aday = ''
        self.atime = ''
        self.acode = ''
        self.aline = ''
        self.tday = ''
        self.grade = ''
        self.gname = ''
        self.pname = ''
        self.amt = ''
        self.lminute = ''

    def toString(self):
        print 'pcode:'+self.pcode+',sday:'+self.sday+',stime:'+self.stime+',aday:'+self.aday+',atime:'+self.atime+',acode:'+self.acode+',aline:'+self.aline+',tday:'+self.tday+',grade:'+self.grade+',gname:'+self.gname+',pname:'+self.pname+',amt:'+self.amt+',lminute:'+self.lminute

def valueParcing(html, idx1, idx2):
    return html[html.find(idx1) + len(idx1):html.find(idx2)]


# 시간 변수들..
today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
thisMonth = strftime("%Y", time) + strftime("%m", time)

mode = 'P' # w:honeymoon, p:packages, g:golf, c:cruise
packagesUrl = 'http://www.hanatour.com/asp/booking/oversea/oversea-main.asp?hanacode=overseas_M_bi'
honeymoonUrl = 'http://www.hanatour.com/asp/booking/honeymoon/hr-main.asp?hanacode=main_q_pack_honey'
golfUrl = 'http://www.hanatour.com/asp/booking/golf/golf-main.asp?hanacode=main_q_pack_golf'
cruiseUrl = 'http://www.hanatour.com/asp/booking/cruise/cruise-main.asp?hanacode=main_q_pack_cruise'

exceptFile = open('hanatourException.txt', 'w')

packagesUrlHtml = urllib2.urlopen(packagesUrl).read()
packagesUrlList = packagesUrlHtml[packagesUrlHtml.find('</form><span class="free_go">'):packagesUrlHtml.find('</dl></div></div>')]
packagesUrlList = packagesUrlList.replace('http://', '\r\nhttp://')
packagesUrlList = savefilegethtml.htmlToList(packagesUrlList, 'packagesUrlFile.txt')
#packagesUrlFile = open('packagesUrlFile.txt', 'w')
#print >> packagesUrlFile, packagesUrlList
#packagesUrlFile.close()

#packagesUrlList = open('packagesUrlFile.txt')
#packageRealUrlList = open('packageRealUrlFile.txt', 'w')
currCountry = ''
for packageUrl in packagesUrlList:
    #print packageUrl
    if packageUrl.find('/productPackage/pk-') > -1 and packageUrl.find('etc_code=' + mode) > -1:
        #print 'original : ' + packageUrl
        if packageUrl.find('target="_self') > -1 and mode == 'P':
            currCountry = packageUrl.split('>')[1].split('<')[0]
            print 'currcountry : ' + currCountry
        else:
            #print packageUrl
            jsonUrl = ''
            if mode == 'P':
                jsonUrl = packageUrl.split("'")[0].replace('amp;', '').replace('pk-11000.asp', 'pk-11000-list.asp')
            else:
                jsonUrl = packageUrl.split('"')[0].replace('amp;', '').replace('pk-11000.asp', 'pk-11000-list.asp')
            print jsonUrl
            #print >> packageRealUrlList, jsonUrl
            #http://www.hanatour.com/asp/booking/productpackage/pk-11000-list.asp?area=A&pub_country=TH&pub_city=HKT&etc_code=W&hanacode=honey_GNB_HKT
            try:
                con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
                packageClass = clsPackage()
                print >> exceptFile, jsonUrl
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
                packageClass.toString()
                contentsList = savefilegethtml.getHtmlList(html, '{"sort_no":', '] })', 'contentsFile.txt', '{', '\r\n{')
                
                #contents = html[html.find('[{"sort_no":') + 1:html.find('] })')].replace('{', '\r\n{')
                #contentsFile = open('contentsFile.txt', 'w')
                #print >> contentsFile, contents
                #contentsFile.close()
                #contentsList = open('contentsFile.txt')
                
                for product in contentsList:
                    print 'product : ' + product
                    if len(product.strip()) < 1:
                        continue
                    productClass = clsProduct()
                    productClass.sort_no = valueParcing(product, 'sort_no":"', '","pkg_mst_code')
                    productClass.pkg_mst_code = valueParcing(product, 'pkg_mst_code":"', '","sMonth')
                    productClass.sMonth = valueParcing(product, 'sMonth":"', '","min_amt')
                    productClass.min_amt = valueParcing(product, 'min_amt":"', '","max_amt')
                    productClass.max_amt = valueParcing(product, 'max_amt":"', '","mst_name')
                    productClass.mst_name = valueParcing(product, 'mst_name":"', '","t_content')
                    productClass.t_content = valueParcing(product, 't_content":"', '","img_seq')
                    productClass.img_seq = valueParcing(product, 'img_seq":"', '","dy_list')
                    productClass.dy_list = valueParcing(product, 'dy_list":"', '","content')
                    productClass.content = valueParcing(product, 'content":"', '","tour_day')
                    productClass.tour_day = valueParcing(product, 'tour_day":"', '","start_dy')
                    productClass.start_dy = valueParcing(product, 'start_dy":"', '","orderSeq')
                    productClass.orderSeq = valueParcing(product, 'orderSeq":"', '"}')
                    #productClass.toString()
                    
                    #query = "insert into t_prd values ('" + productClass.pkg_mst_code + "','" + 
                    #cursor = con.cursor()
                    #cursor.execute(query)
                    #con.commit()                           
                    
                    
                    cityCode = jsonUrl[jsonUrl.find('&hanacode=') + len('&hanacode='):]
                    detailProductUrl = 'http://www.hanatour.com/asp/booking/productPackage/pk-11001-list.asp?'
                    detailProductUrl += 'area=' + packageClass.pub_area_code + '&pub_country=' +packageClass.pub_country+ '&pub_city=' + packageClass.pub_city
                    detailProductUrl += '&tour_scheduled_year='+strftime("%Y", time)+'&tour_scheduled_month='+strftime("%m", time)+'&tour_scheduled_day=&pkg_code=&tour_old_year='+strftime("%Y", time)
                    detailProductUrl += '&tour_old_month='+strftime("%m", time)+'&pkg_mst_code='+productClass.pkg_mst_code
                    detailProductUrl += '&tour_scheduled_dt='+strftime("%Y", time)+'-'+strftime("%m", time)+'&etc_code=P&hanacode='+ cityCode
                    print 'last url.....: ' + detailProductUrl
                    
                    print >> exceptFile, detailProductUrl
                    detailProducthtml = urllib2.urlopen(detailProductUrl).read()
                    
                    #cont":[{"pcode":"PPP411140612KE5","sdate":"06/12 (목) 20:50","adate":"06/16 (월) 08:05","acode":"KE","aline":"대한항공","tday":"5","grade":"12","gname":"하나팩클래식","pname":"팔라우 5일[Luxury]팔라우퍼시픽리조트[용궁+유네스코+젤리피쉬]","amt":"1999000","lminute":"2"},                    
                    
                    if detailProducthtml.find('[{"pcode"') < 0:
                        continue
                    detailProductList = savefilegethtml.getHtmlList(detailProducthtml, '{"pcode"', '] })', 'detailProductFile.txt', '{', '\r\n{')
                    #temp = detailProducthtml[detailProducthtml.find('[{"pcode"') + 1:detailProducthtml.find('] })')].replace('{', '\r\n{')
                    #detailProductFile = open('detailProductFile.txt', 'w')
                    #print >> detailProductFile, temp
                    #detailProductFile.close()
                    #detailProductList = open('detailProductFile.txt')
                    
                    #con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
                    #idx = 1;
                    try:
                        for detailProduct in detailProductList:
                            #print 'detail Product : ' + detailProduct
                            if len(detailProduct.strip()) < 1:
                                continue
                            detailClass = clsDetailProduct()
                            detailClass.pcode = valueParcing(detailProduct, 'pcode":"', '","sdate')
                            sDate = valueParcing(detailProduct, 'sdate":"', '","adate')
                            aDate = valueParcing(detailProduct, 'adate":"', '","acode')
                            detailClass.sday = strftime("%Y", time) + '/' + sDate.split('(')[0].strip()
                            detailClass.stime = sDate.split(')')[1].strip()
                            detailClass.aday = strftime("%Y", time) + '/' + aDate.split('(')[0].strip()
                            detailClass.atime = aDate.split(')')[1].strip()
                            detailClass.acode = valueParcing(detailProduct, 'acode":"', '","aline')
                            detailClass.aline = valueParcing(detailProduct, 'aline":"', '","tday')
                            detailClass.tday = valueParcing(detailProduct, 'tday":"', '","grade')
                            detailClass.grade = valueParcing(detailProduct, 'grade":"', '","gname')
                            detailClass.gname = valueParcing(detailProduct, 'gname":"', '","pname').decode('utf-8')
                            detailClass.pname = valueParcing(detailProduct, 'pname":"', '","amt').decode('utf-8')
                            detailClass.amt = valueParcing(detailProduct, 'amt":"', '","lminute')
                            detailClass.lminute = valueParcing(detailProduct, 'lminute":"', '"}')
                            
                            lastUrl = 'http://www.hanatour.com/asp/booking/productPackage/pk-12000.asp?pkg_code=' + detailClass.pcode
                            #detailClass.toString()
                            #print idx
                            #idx += 1
                            #query = "insert into product_test values(product_seq.nextval,'hanatour','"
                            #query += cityCode + "','" + detailClass.pname + "','" + 
                            
                           # query = "insert into product_test values (product_seq.nextval, '" + tag_div + "','" + reg_div + "','" + prd_nm + "','" + air_cd + "','" + st_city
                            #query += "',to_date('" + st_dt + "'),'" + tr_term + "','" + tr_div + "','" + dmst_div + "','" + sel_dt + "','" + st_time + "'," + prd_fee + ",'" + prd_url
                            #query += "',to_date('" + arr_day + "'),'" + arr_time + "','" + prd_status + "')"                        
                            
                            query = "insert into product_test values (product_seq.nextval, 'hanatour','" + cityCode[len(cityCode)-3:] + "','" + detailClass.pname + "','ICN',"
                            query += "to_date('" + detailClass.sday + "'),'" + detailClass.tday + "','package','',to_char(sysdate, 'yyyymmdd'),''," + detailClass.amt + ",'" + lastUrl
                            query += "',to_date('" + detailClass.aday + "'),'','" + detailClass.lminute + "','" + detailClass.acode +"')"
                            
                            cursor = con.cursor()
                            cursor.execute(query)
                            con.commit()
                            
                            #break
                            #>>> con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
                        #>>> cursor = con.cursor()
                        #>>> cursor.execute("select * from tab")
                        #<cx_Oracle.Cursor on <cx_Oracle.Connection to bigtour@hnctech73.iptime.org:1521/ora11g>>
                        #>>> print cursor.fetchall()
                        #[('T_PRD', 'TABLE', None), ('T_PRD_DTL', 'TABLE', None)]
                        #>>> cursor.close()
                        #>>> con.close() 
                    except:
                        print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
                        pass
                    finally:
                        #detailProductList.close()
                        con.close() 
                    
                    break
                #contentsList.close()
                    
            except:
                print >> exceptFile, "Parcing or Query Error:", sys.exc_info()[0]
                pass
            
            break

#packagesUrlList.close()
#packageRealUrlList.close()
exceptFile.close()

#productPackage/pk- 값이 존재하고... etc_code=P 인것..이 패키지
#pkg_mst_code 값이 있는 경우는.. 바로 세부조회 내용임...(날짜 선택하는..) 이런 경우도 있김 있음..
#etc_code=W/P/A/B/K/Y/J/C  'W' : honeymoon, 'A': free, 'P' : package, 'B' : AirTel, 'K' : Tracking, 'Y' : Leports, 'J' : 성지순례, 'C' : Cruise
#</form><span class="free_go">
#</dl></div></div>
"""
http://www.hanatour.com/asp/booking/productPackage/pk-11000-list.asp?
callback=jQuery18307540583240417797_1402302755082
&area=A
&pub_country=TH
&pub_city=BKK
&tour_scheduled_year=2014
&tour_scheduled_month=06
&tour_scheduled_day=
&pkg_code=
&tour_old_year=2014
&tour_old_month=06
&start_city=
&cost_cont_div=
&cost_cont_code=
&start_air_code=
&subject=
&product_name=
&goods_property=
&cost_code=
&cost_name=
&pkg_mst_code=
&product_property=
&ad_code=
&goods_grade=
&re_subject=
&sort_value=
&tour_scheduled_dt=2014-06
&promo_doumi_code=
&etc_code=P
&hanacode=overseas_GNB_AE_TH_NKK
&dy_list=
&dept_code=
&adult_smin_amt=
&adult_smax_amt=
&_=1402302755495"""
