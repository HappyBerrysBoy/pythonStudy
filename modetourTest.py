# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

@author: KSC
"""

import requests
import xmltodict
import urllib2
import re
import cx_Oracle
import savefilegethtml

#classes..
class subMain():
    def __init__(self):
        self.thing = 0
    
    def getParam(self, line):
        #dicts = dict()
        self.startLocation = line[line.find('startLocation=') + len('startLocation='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        #print(line)
        self.id = line[line.find('id=') + len('id='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        #print(line)
        self.type = line[line.find('type=') + len('type='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        #print(line)
        self.MLoc = line[line.find('MLoc=') + len('MLoc='):line.find(' ') - 1]
        return self
    
    def printToString(self):
        print('SubMain ==> startlocation:' + self.startLocation + ', id:' + self.id + ', type:' + self.type + ', Mloc:' + self.MLoc)
        
    def makeURL(self):
        return 'http://www.modetour.com/Package/subMain2.aspx?startLocation=' + self.startLocation + '&id=' + self.id + '&type=' + self.type + '&MLoc=' + self.MLoc

class subList():
    def __init__(self):
        self.thing = 0
    
    def getParam(self, line):
        self.startLocation = line[line.find('startLocation=') + len('startLocation='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        self.location = line[line.find('location=') + len('location='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        self.location1 = line[line.find('location1=') + len('location1='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        if line.find('Theme=') > -1:
            self.Theme = line[line.find('Theme=') + len('Theme='):line.find('amp;') - 1]
            line = line[line.find('amp;') + len('amp;'):]
        else:
            self.Theme = ''

        if line.find('Theme1=') > -1:
            self.Theme1 = line[line.find('Theme1=') + len('Theme1='):line.find('amp;') - 1]
            line = line[line.find('amp;') + len('amp;'):]
        else:
            self.Theme1 = ''
        self.MLoc = line[line.find('MLoc=') + len('MLoc='):line.find(' ') - 1]
        return self
    
    def printToString(self):
        print('SubList ==> startlocation:' + self.startLocation + ', location:' + self.location + ', location1:' + self.location1 + ', Theme:' + self.Theme + ', Theme1:' + self.Theme1 + ', Mloc:' + self.MLoc)
        
    def makeURL(self):
        return 'http://www.modetour.com/Package/List.aspx?startLocation=' + self.startLocation + '&location=' + self.location + '&location1=' + self.location1 + '&Theme=' + self.Theme + '&Theme1=' + self.Theme1 + '&MLoc=' + self.MLoc


sleepTime = 0.5

mainpage = ''
mainpage = requests.get('http://www.modetour.com/').text

overseas = mainpage[mainpage.find('<div class="overseas">'):mainpage.find('<div class="domestic">')]
domestics = mainpage[mainpage.find('<div class="domestic">'):mainpage.find('<div class="total_categories">')]

overseasFile = open('overseas.txt', 'w')
domesticsFile = open('domestics.txt', 'w')

print >> overseasFile, overseas.encode('utf-8')
print >> domesticsFile, domestics.encode('utf-8')

overseasFile.close()
domesticsFile.close()
#print(overseas)
#print('=========================================================================================================================================')
#print(domestics)

openOverseas = open('overseas.txt')
openDomestics = open('domestics.txt')

#전체 List 말고 대표 메뉴만 가도 다 나오는듯...
overseasMainUrls = list()
overseasMainUrlsFile = open('mainUrls.txt', 'w')
for each_line in openOverseas:
    if each_line.strip()[:3] == '<li':
        if each_line.find('subMain') > -1 and each_line.find('span') > -1:
        #print(each_line.strip())
            submain = subMain()
            result = submain.getParam(each_line)
            #submain.printToString()
            #print(submain.makeURL())
            print >> overseasMainUrlsFile, submain.makeURL()
            overseasMainUrls.append(submain.makeURL())
        """elif each_line.find('List') > -1:
            sublist = subList()
            result = sublist.getParam(each_line)
            #sublist.printToString()
            #print(sublist.makeURL())
            print >> mainUrls, sublist.makeURL()
            overseasMainUrls.append(submain.makeURL())"""
overseasMainUrlsFile.close()
openOverseas.close()
openDomestics.close()

menuDistrict = overseasMainUrls.pop()
menuPremium = overseasMainUrls.pop()
menuCruise = overseasMainUrls.pop()
menuGolf = overseasMainUrls.pop()
menuHoney = overseasMainUrls.pop()
menuFree= overseasMainUrls.pop()
menuPackage = overseasMainUrls.pop()

travle_kind = 'package'

try:
    packageResponse = requests.get(menuPackage).text
    packageResponse = packageResponse[packageResponse.find('<div class="submain">'):packageResponse.find('<div class="total_categories">')]
    menuPackageFile = open('packageUrls.txt', 'w')
    print >> menuPackageFile, packageResponse.encode('utf-8')
    menuPackageFile.close()
except:
    print('Error Second Page Loading...')

#print(packageResponse)

subUrls = open('modePackageUrls.txt', 'w')
openPackageFile = open('packageurls.txt')
for each_line in openPackageFile:
    if each_line.strip()[:3] == '<dt' or each_line.strip()[:3] == '<dd':
        #print(each_line)
        sublist = subList()
        result = sublist.getParam(each_line)
        #print(sublist.makeURL())
        #print >> subUrls, each_line
        print >> subUrls, sublist.makeURL()
subUrls.close()
openPackageFile.close()

# 시간 변수들..
targetYear = '2014'#sys.argv[1]
targetMonth = '07'#sys.argv[2]

idx = 0
normalCnt = 0
parcingErr = 0
parcingErr2 = 0
urlErr = 0
productList = list()
productList.append('START')
subUrls = open('modePackageUrls.txt')
exceptFile = open('modeTourException.txt', 'w')

for each_line in subUrls:
    anCode = each_line[each_line.find('location=') + len('location=LOC'):each_line.find('&location1=')]
    themeCode = each_line[each_line.find('Theme=') + len('Theme='):each_line.find('&Theme1=')]
    productUrl = 'http://www.modetour.com/XML/Package/Get_ProductList.aspx?AN=' + anCode + '&Ct=&PL=10000&Pd=&Pn=1&TN=' + themeCode
    
    print('Product URL : ' + productUrl)
    print >> exceptFile, productUrl
    productListOpener = urllib2.urlopen(productUrl)
    productListGet = productListOpener.read()


    pcodeList = re.findall(r'\bPcode="[\w]*', productListGet)
    
    for pcode in pcodeList:
        detailProduct = pcode.split('"')[1]
        type(detailProduct)
        #print('detailProduct : ' + detailProduct)
        
        if productList.count(detailProduct) == 0:
            productList.append(detailProduct)
            #print('productList : ' + productList)
            
            tmpUrl = 'http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=' + targetMonth + '&Pcode=' + detailProduct + '&Pd=&Type=01'
            print('Detail Product URL : ' + tmpUrl)
            print >> exceptFile, tmpUrl
            #import cx_Oracle
            #>>> con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
            #>>> cursor = con.cursor()
            #>>> cursor.execute("select * from tab")
            #<cx_Oracle.Cursor on <cx_Oracle.Connection to bigtour@hnctech73.iptime.org:1521/ora11g>>
            #>>> print cursor.fetchall()
            #[('T_PRD', 'TABLE', None), ('T_PRD_DTL', 'TABLE', None)]
            #>>> cursor.close()
            #>>> con.close() 
            
            con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")

            detailUrl = requests.get(tmpUrl).text
            tree = xmltodict.parse(detailUrl)
            for t in tree['ModeSangPum']['SangList']:
                reg_div = anCode
                print reg_div
                prd_nm = t['SName']['#text']
                print prd_nm
                air_cd = t['SAirCode']
                print air_cd
                st_city = ''
                st_dt = t['SPriceDay']['#text']
                print st_dt
                #st_time = t['SstartTime']
                st_time = ''
                arr_day = t['SArrivalDay']['#text']
                print arr_day
                #arr_time = t['SArrivalTime']
                arr_time = ''
                tr_term = t['SDay']
                print tr_term
                tr_div = themeCode
                print tr_div
                sel_dt = ''
                dmst_div = travle_kind
                print dmst_div
                prd_fee = t['SPrice']
                print prd_fee
                prd_status = t['SDetailState']['#text']
                print prd_status
                prd_url = ''
                
                """
                query = "insert into product_test values (product_seq.nextval, '" + tag_div + "','" + reg_div + "','" + prd_nm + "','" + st_city
                query += "',to_date('" + st_dt + "'),'" + tr_term + "','" + tr_div + "','" + dmst_div + "','" + sel_dt + "','" + st_time + "'," + prd_fee + ",'" + prd_url
                query += "',to_date('" + arr_day + "'),'" + arr_time + "','" + prd_status + "','" + air_cd + "')"
                
                
                query = savefilegethtml.getMasterMergeQuery('hanatour', productClass.pkg_mst_code, packageClass.pub_area_code, packageClass.pub_country, packageClass.pub_city, productClass.mst_name, mode, 'A', productClass.content, '')
                cursor = con.cursor()
                cursor.execute(query)
                con.commit()       
                
                query = savefilegethtml.getDetailMergeQuery('hanatour', productClass.pkg_mst_code, detailClass.pcode, detailClass.pname, detailClass.dday+detailClass.dtime, detailClass.aday+detailClass.atime, detailClass.tday, departCity, '', detailClass.acode, detailClass.lminute, detailClass.url, detailClass.amt, '0', '0', '0', '') 
                cursor = con.cursor()
                cursor.execute(query)
                con.commit()
                
                """
                #print >> exceptFile, query
                
                #print(query)
                #DB에 입력하는 쿼리..
                break
                #print(t['SName']['#text'])
                #print(t['SNight'])
                #print(t['SDay'])
                #print(t['SPrice'])
                #print(t['SAirCode'])
                #print(t['SAirName'])
                #print(t['SPriceDay']['#text'])
                #print(t['SArrivalDay']['#text'])
                #print(t['SPriceNum']['#text'])
                #print(t['SMeet'])
                #print(t['SstartAir'])
                #print(t['SstartTime'])
                #print(t['SArrivalTime'])
                #print(t['SDetailState']['#text'])
                
            normalCnt += 1
            cursor.close()
            con.close()
        
        break
        
    break

productListOpener.close()
subUrls.close()
exceptFile.close()

print("==========Product List==========")
print(productList)
print('Normal Process: ' + str(normalCnt) + ', Parcing Error: ' + str(parcingErr) + ', Parcing Error2 : ' + str(parcingErr2) + ', URL Error: ' + str(urlErr))
"""

#aa = requests.get("http://www.modetour.com/Package/List.aspx?startLocation=ICN&location=LOC4&location1=LOC4^LOC3&Theme=THE88&Theme1=THE88&MLoc=01")
#http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=06&Pcode=ATE101&Pd=&Type=01&term=201406060000%5E201506052359
#http://www.modetour.com/XML/Package/Get_ProductList.aspx?AN=4&Ct=&DateTerm=201406052346%5E201506042359&PL=1000&Pd=&Pn=1&S=201406&TN=THE88 ==> AN 값이 뭐지?? 전체보기.. PL 값을 최대로... Pn은 페이지 번호.. 1로 설정
#====> AN 값은... location 값을 쓰면 됨...(LOC 빼고..)

State 색별 상태..
red : 출발확정(최소 출발인원 이상 예약이 되어있는 상품으로서 예약과 동시에 출발이 가능합니다. 단, 예약자의 일부가 취소되어 최소 출발인원에 미치지 못할 경우, 행사가 진행되지 못할 수도 있습니다.)
blue : 예약가능(여유 좌석 내에서 예약이 가능하지만, 단체의 예약인원이 최소 출발인원에 미달하여 출발 여부는 미정인 상태입니다. 최소 출발인원 이상 예약될 경우 출발가능으로 변경됩니다.)
green : 대기예약(여유 죄석이 없거나 출발이 임박하여 예약가능 시간이 지나 담당자와의 확인이 필요한 상황입니다.)
기타색.. : 예약마감(판매가 종료된 상품입니다. 다른 상품이나 다른 날짜를 이용해 주시기 바랍니다)
"""


