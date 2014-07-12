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
import sys
import savefilegethtml
import time, datetime
import codes
import tourQuery

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
        self.tourType = getTourType(line.split('<span>')[1].split('<')[0])
    
    def printToString(self):
        print('SubMain ==> startlocation:' + self.startLocation + ', id:' + self.id + ', type:' + self.type + ', Mloc:' + self.MLoc)
        
    def makeURL(self):
        return 'http://www.modetour.com/Package/subMain2.aspx?startLocation=' + self.startLocation + '&id=' + self.id + '&type=' + self.type + '&MLoc=' + self.MLoc

def getTourType(name):
    if name == '패키지':
        return 'P'
    elif name == '자유':
        return 'F'
    elif name == '허니문':
        return 'W'
    elif name == '골프':
        return 'G'
    elif name == '크루즈':
        return 'C'
    elif name == 'JM':
        return 'L'
    elif name == '부산·지방출발':
        return 'B'

class subList():
    def __init__(self):
        self.thing = 0
    
    def getParam(self, line):
        #print 'Line Info : ' + line
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
        self.name = ''
        if len(line.split('">')) > 1 and  len(line.split('">')[1].split('<')[0]) > 0:
            self.name = line.split('">')[1].split('<')[0].decode('utf-8')
        else:
            self.name = ''
    
    def printToString(self):
        print('SubList ==> startlocation:' + self.startLocation + ', location:' + self.location + ', location1:' + self.location1 + ', Theme:' + self.Theme + ', Theme1:' + self.Theme1 + ', Mloc:' + self.MLoc)
        
    def makeURL(self):
        return 'http://www.modetour.com/Package/List.aspx?startLocation=' + self.startLocation + '&location=' + self.location + '&location1=' + self.location1 + '&Theme=' + self.Theme + '&Theme1=' + self.Theme1 + '&MLoc=' + self.MLoc


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
# 일단 해외여행만... 국내여행을 별도로...
# 시간 변수들..
tourAgency = 'modutour'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
#targetYear = '2014'
#targetMonth = '07'
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

idx = 0
normalCnt = 0
parcingErr = 0
parcingErr2 = 0
urlErr = 0
productList = list()
productList.append('START')
exceptFile = open('modeTourException' + scrappingStartTime + '.txt', 'w')
print >> exceptFile, "Start : %s" % time.ctime()

departCity = ''
tourtype = ''

#overseasMainUrls = list()
#overseasMainUrlsFile = open('mainUrls.txt', 'w')

for each_line in openOverseas:
    if each_line.strip()[:3] == '<li':
        if each_line.find('subMain') > -1 and each_line.find('span') > -1:
            submain = subMain()
            submain.getParam(each_line)
            tourtype = submain.tourType
            departCity = submain.startLocation
            #print >> overseasMainUrlsFile, submain.makeURL()
            #overseasMainUrls.append(submain.makeURL())
            
            try:
                packageResponse = requests.get(submain.makeURL()).text
                packageResponse = packageResponse[packageResponse.find('<div class="submain">'):packageResponse.find('<div class="total_categories">')]
                menuPackageFile = open('packageUrls.txt', 'w')
                print >> menuPackageFile, packageResponse.encode('utf-8')
                menuPackageFile.close()
            
                openPackageFile = open('packageurls.txt')
                con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
                
                for each_line in openPackageFile:
                    if each_line.strip()[:3] == '<dt' or each_line.strip()[:3] == '<dd':
                        #print(each_line)
                        sublist = subList()
                        sublist.getParam(each_line)
                        #print(sublist.makeURL())
                        #print >> subUrls, each_line
                        #print >> subUrls, sublist.makeURL()
                        listUrls = sublist.makeURL()
                        anCode = listUrls[listUrls.find('location=') + len('location=LOC'):listUrls.find('&location1=')]
                        themeCode = listUrls[listUrls.find('Theme=') + len('Theme='):listUrls.find('&Theme1=')]
                        productUrl = 'http://www.modetour.com/XML/Package/Get_ProductList.aspx?AN=' + anCode + '&Ct=&PL=1000&Pd=&Pn=1&TN=' + themeCode
                        
                        try:
                            print('Product URL : ' + productUrl)
                            print >> exceptFile, productUrl
                            productListGet = urllib2.urlopen(productUrl).read()
                            
                            try:
                                pcodeList = re.findall(r'\bPcode="[\w]*', productListGet)
                                
                                for pcode in pcodeList:
                                    detailProduct = pcode.split('"')[1]
                                    
                                    if productList.count(detailProduct) == 0:
                                        productList.append(detailProduct)
                                        #print('productList : ' + productList)
                                        
                                        tmpUrl = 'http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=' + targetMonth + '&Pcode=' + detailProduct + '&Pd=&Type=01'
                                        print('Detail Product URL : ' + tmpUrl)
                                        print >> exceptFile, tmpUrl
                
                                        try:                
                                            detailUrl = requests.get(tmpUrl).text
                                            tree = xmltodict.parse(detailUrl)
                                            productCode = tree['ModeSangPum']['SCode']
                                            productName = tree['ModeSangPum']['STitle'].replace("'", "")
                                            productComment = tree['ModeSangPum']['SCont'].replace("'", "")
                                            
                                            #print productName
                                            codeList = codes.getCityCode(sublist.name, productName, productComment)
                                            cityList = codeList[0]
                                            nationList = codeList[1]
                                            continentList = codeList[2]
                                            
                                            # Master 상품 입력
                                            query = tourQuery.getMasterMergeQuery(tourAgency, productCode, productName, tourtype, 'A', productComment, '')
                                            #print query
                                            cursor = con.cursor()
                                            cursor.execute(query)
                                            # Region Data 삭제
                                            codes.insertRegionData(tourAgency, productCode, cityList, nationList, continentList)
                                            con.commit()
                                            
                                            #query = savefilegethtml.getMasterMergeQueryTest1('modutour', productCode, '', '', sublist.name, productName, tourtype, 'A', productComment, '', nationList, cityList)  # A : 해외(Abroad)
                                            #query = savefilegethtml.getMasterMergeQuery('modutour', productCode, '', '', sublist.name, productName, tourtype, 'A', productComment, '')  # A : 해외(Abroad)
                                            #print query
                                            #cursor = con.cursor()
                                            #cursor.execute(query)
                                            #con.commit()
                                            
                                            if not tree['ModeSangPum'].has_key('SangList'):
                                                continue
                                            
                                            for t in tree['ModeSangPum']['SangList']:
                                                tag_div = ''
                                                reg_div = anCode
                                                prd_nm = t['SName']['#text'].replace("'", "")
                                                air_cd = t['SAirCode'][:2]
                                                st_city = ''
                                                st_dt = t['SPriceDay']['#text']
                                                st_time = t['SstartTime'].replace(':', '')
                                                #st_time = ''
                                                arr_day = t['SArrivalDay']['#text']
                                                arr_time = t['SArrivalTime'].replace(':', '')
                                                arr_time = ''
                                                tr_term = t['SDay']
                                                tr_div = themeCode
                                                sel_dt = ''
                                                prd_fee = t['SPrice']['#text']
                                                prd_status = codes.getStatus('modetour', t['SDetailState']['#text'])
                                                prd_code = t['SPriceNum']['#text']
                                                flynum = t['SstartAir']
                                                #period = t['SNight']  #기간이 아니라... 잠자는 횟수임.. 1박2일이면.. 1
                                                airline = t['SAirName']
                                                prd_url = 'http://www.modetour.com/Package/Itinerary.aspx?startLocation='+sublist.startLocation+'&location='+sublist.location+'&location1='+sublist.location1+'&theme='+sublist.Theme+'&theme1='+sublist.Theme1+'&MLoc='+sublist.MLoc+'&Pnum='+prd_code
                                                #print 'product url:' + prd_url
                                                query = tourQuery.getDetailMergeQuery(tourAgency, productCode, prd_code, prd_nm, st_dt+st_time, arr_day+arr_time, tr_term, sublist.startLocation, '', air_cd, prd_status, prd_url, prd_fee, '0', '0', '0', '') 
                                                #print >> exceptFile, query
                                                #print query
                                                cursor = con.cursor()
                                                cursor.execute(query)
                                                con.commit()
                                                normalCnt += 1
                                                #break
                                            
                                                #print(t['SMeet'])
                                        except TypeError as typeerr:
                                            urlErr += 1
                                            reg_div = anCode
                                            prd_nm = tree['ModeSangPum']['SangList']['SName']['#text'].replace("'", "")
                                            air_cd = tree['ModeSangPum']['SangList']['SAirCode']
                                            st_dt = tree['ModeSangPum']['SangList']['SPriceDay']['#text']
                                            st_time = tree['ModeSangPum']['SangList']['SstartTime'].replace(':', '')
                                            arr_day = tree['ModeSangPum']['SangList']['SArrivalDay']['#text']
                                            arr_time = tree['ModeSangPum']['SangList']['SArrivalTime'].replace(':', '')
                                            tr_term = tree['ModeSangPum']['SangList']['SDay']
                                            tr_div = themeCode
                                            prd_fee = tree['ModeSangPum']['SangList']['SPrice']
                                            prd_status = tree['ModeSangPum']['SangList']['SDetailState']['#text']
                                            prd_code = tree['ModeSangPum']['SangList']['SPriceNum']['#text']
                                            flynum = tree['ModeSangPum']['SangList']['SstartAir']
                                            airline = tree['ModeSangPum']['SangList']['SAirName']
                                            prd_url = 'http://www.modetour.com/Package/Itinerary.aspx?startLocation='+sublist.startLocation+'&location='+sublist.location+'&location1='+sublist.location1+'&theme='+sublist.Theme+'&theme1='+sublist.Theme1+'&MLoc='+sublist.MLoc+'&Pnum='+prd_code
                                            query = savefilegethtml.getDetailMergeQuery('modetour', productCode, prd_code, prd_nm, st_dt+st_time, arr_day+arr_time, tr_term, sublist.startLocation, '', air_cd, prd_status, prd_url, prd_fee, '0', '0', '0', '') 
                                            #print query
                                            cursor = con.cursor()
                                            cursor.execute(query)
                                            con.commit()
                                            #print >> exceptFile, query
                                            print >> exceptFile, "Depth 33 : type Error:", sys.exc_info()[0]
                                            pass
                                        except:
                                            urlErr += 1
                                            print >> exceptFile, sys.exc_info()[0]
                                            pass
                                    #break
                            except:
                                urlErr += 1
                                print >> exceptFile, "Depth 2 : Parcing or Query Error:", sys.exc_info()[0]
                                pass
                            
                        except urllib2.URLError as err:
                            urlErr += 1
                            print >> exceptFile, "Depth 1 : Parcing or Query Error:", sys.exc_info()[0]
                            pass
                        
                        #break
            except:
                urlErr += 1
                print >> exceptFile, "Depth 0 :  Error:", sys.exc_info()[0]
                pass
            finally:
                openPackageFile.close()
                con.commit()
                con.close()
            
            #break
        """elif each_line.find('List') > -1:
            sublist = subList()
            result = sublist.getParam(each_line)
            #sublist.printToString()
            #print(sublist.makeURL())
            print >> mainUrls, sublist.makeURL()
            overseasMainUrls.append(submain.makeURL())"""
#overseasMainUrlsFile.close()
openOverseas.close()
openDomestics.close()
print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()

#menuDistrict = overseasMainUrls.pop()
#menuPremium = overseasMainUrls.pop()
#menuCruise = overseasMainUrls.pop()
#menuGolf = overseasMainUrls.pop()
#menuHoney = overseasMainUrls.pop()
#menuFree= overseasMainUrls.pop()
#menuPackage = overseasMainUrls.pop()

"""
try:
    packageResponse = requests.get(menuPackage).text
    packageResponse = packageResponse[packageResponse.find('<div class="submain">'):packageResponse.find('<div class="total_categories">')]
    menuPackageFile = open('packageUrls.txt', 'w')
    print >> menuPackageFile, packageResponse.encode('utf-8')
    menuPackageFile.close()
except:
    print('Error Second Page Loading...')
"""
#print(packageResponse)
"""
openPackageFile = open('packageurls.txt')
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")

for each_line in openPackageFile:
    if each_line.strip()[:3] == '<dt' or each_line.strip()[:3] == '<dd':
        #print(each_line)
        sublist = subList()
        sublist.getParam(each_line)
        #print(sublist.makeURL())
        #print >> subUrls, each_line
        #print >> subUrls, sublist.makeURL()
        listUrls = sublist.makeURL()
        anCode = listUrls[listUrls.find('location=') + len('location=LOC'):listUrls.find('&location1=')]
        themeCode = listUrls[listUrls.find('Theme=') + len('Theme='):listUrls.find('&Theme1=')]
        productUrl = 'http://www.modetour.com/XML/Package/Get_ProductList.aspx?AN=' + anCode + '&Ct=&PL=1000&Pd=&Pn=1&TN=' + themeCode
        
        try:
            print('Product URL : ' + productUrl)
            print >> exceptFile, productUrl
            productListGet = urllib2.urlopen(productUrl).read()
            try:
                pcodeList = re.findall(r'\bPcode="[\w]*', productListGet)
                
                for pcode in pcodeList:
                    detailProduct = pcode.split('"')[1]
                    
                    if productList.count(detailProduct) == 0:
                        productList.append(detailProduct)
                        #print('productList : ' + productList)
                        
                        tmpUrl = 'http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=' + targetMonth + '&Pcode=' + detailProduct + '&Pd=&Type=01'
                        print('Detail Product URL : ' + tmpUrl)
                        print >> exceptFile, tmpUrl

                        try:                
                            detailUrl = requests.get(tmpUrl).text
                            tree = xmltodict.parse(detailUrl)
                            productCode = tree['ModeSangPum']['SCode']
                            productName = tree['ModeSangPum']['STitle']
                            productComment = tree['ModeSangPum']['SCont']
                            query = savefilegethtml.getMasterMergeQuery('modetour', productCode, '', '', sublist.name, productName, 'P', 'A', productComment, '')
                            #print query
                            cursor = con.cursor()
                            cursor.execute(query)
                            con.commit()                            
                            
                            for t in tree['ModeSangPum']['SangList']:
                                tag_div = ''
                                reg_div = anCode
                                prd_nm = t['SName']['#text']
                                air_cd = t['SAirCode']
                                st_city = ''
                                st_dt = t['SPriceDay']['#text']
                                st_time = t['SstartTime'].replace(':', '')
                                #st_time = ''
                                arr_day = t['SArrivalDay']['#text']
                                arr_time = t['SArrivalTime'].replace(':', '')
                                arr_time = ''
                                tr_term = t['SDay']
                                tr_div = themeCode
                                sel_dt = ''
                                prd_fee = t['SPrice']
                                prd_status = t['SDetailState']['#text']
                                prd_code = t['SPriceNum']['#text']
                                flynum = t['SstartAir']
                                #period = t['SNight']  #기간이 아니라... 잠자는 횟수임.. 1박2일이면.. 1
                                airline = t['SAirName']
                                prd_url = 'http://www.modetour.com/Package/Itinerary.aspx?startLocation='+sublist.startLocation+'&location='+sublist.location+'&location1='+sublist.location1+'&theme='+sublist.Theme+'&theme1='+sublist.Theme1+'&MLoc='+sublist.MLoc+'&Pnum='+prd_code
                                #print 'product url:' + prd_url
                                #print >> exceptFile, query
                                query = savefilegethtml.getDetailMergeQuery('modetour', productCode, prd_code, prd_nm, st_dt+st_time, arr_day+arr_time, tr_term, sublist.startLocation, '', air_cd, prd_status, prd_url, prd_fee, '0', '0', '0', '') 
                                #print query
                                cursor = con.cursor()
                                cursor.execute(query)
                                con.commit()
                                break
                                #print(t['SMeet'])
                        except KeyError as keyerr:
                            pass
                        except TypeError as typeerr:
                            reg_div = anCode
                            prd_nm = tree['ModeSangPum']['SangList']['SName']['#text']
                            air_cd = tree['ModeSangPum']['SangList']['SAirCode']
                            st_dt = tree['ModeSangPum']['SangList']['SPriceDay']['#text']
                            st_time = tree['ModeSangPum']['SangList']['SstartTime'].replace(':', '')
                            arr_day = tree['ModeSangPum']['SangList']['SArrivalDay']['#text']
                            arr_time = tree['ModeSangPum']['SangList']['SArrivalTime'].replace(':', '')
                            tr_term = tree['ModeSangPum']['SangList']['SDay']
                            tr_div = themeCode
                            prd_fee = tree['ModeSangPum']['SangList']['SPrice']
                            prd_status = tree['ModeSangPum']['SangList']['SDetailState']['#text']
                            prd_code = tree['ModeSangPum']['SangList']['SPriceNum']['#text']
                            flynum = tree['ModeSangPum']['SangList']['SstartAir']
                            airline = tree['ModeSangPum']['SangList']['SAirName']
                            prd_url = 'http://www.modetour.com/Package/Itinerary.aspx?startLocation='+sublist.startLocation+'&location='+sublist.location+'&location1='+sublist.location1+'&theme='+sublist.Theme+'&theme1='+sublist.Theme1+'&MLoc='+sublist.MLoc+'&Pnum='+prd_code
                            query = savefilegethtml.getDetailMergeQuery('modetour', productCode, prd_code, prd_nm, st_dt+st_time, arr_day+arr_time, tr_term, sublist.startLocation, '', air_cd, prd_status, prd_url, prd_fee, '0', '0', '0', '') 
                            #print query
                            cursor = con.cursor()
                            cursor.execute(query)
                            con.commit()
                            print >> exceptFile, query
                            print >> exceptFile, "Depth 33 : type Error:", sys.exc_info()[0]
                            pass
                        except:
                            parcingErr2 += 1
                            print >> exceptFile, "Depth 3 : Parcing or Query Error:", sys.exc_info()[0]
                            pass
                        normalCnt += 1
                    break
            except:
                print >> exceptFile, "Depth 2 : Parcing or Query Error:", sys.exc_info()[0]
                pass
            
        except urllib2.URLError as err:
            print >> exceptFile, "Depth 1 : Parcing or Query Error:", sys.exc_info()[0]
            pass
        
        break
openPackageFile.close()
con.close()
exceptFile.close()
"""

#Daum 쇼핑하우는 통신판매중개자로서 상품주문, 배송 및 환불의 의무와 책임은 각 판매업체에 있습니다. 위 내용에 대한 저작권 및 법적 책임은 자료제공사 또는 글쓴이에 있으며 Daum의 입장과 다를 수 있습니다.

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
