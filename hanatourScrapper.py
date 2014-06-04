# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

@author: KSC
"""

import requests
import xmltodict
import time, datetime
from time import localtime, strftime
from datetime import timedelta
import urllib2

mainpage = requests.get('http://www.modetour.com/').text

overseas = mainpage[mainpage.find('<div class="overseas">'):mainpage.find('<div class="domestic">')]
domestics = mainpage[mainpage.find('<div class="domestic">'):mainpage.find('<div class="total_categories">')]

overseasFile = open('overseas.txt', 'w')
domesticsFile = open('domestics.txt', 'w')

print >> overseasFile, overseas
print >> domesticsFile, domestics

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

packageResponse = requests.get(menuPackage).text
packageResponse = packageResponse[packageResponse.find('<div class="submain">'):packageResponse.find('<div class="total_categories">')]
menuPackageFile = open('packageUrls.txt', 'w')
print >> menuPackageFile, packageResponse
menuPackageFile.close()
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

today = datetime.date.today()
nextYear = today + timedelta(days=365)
nextTime = nextYear.timetuple()
time = time.localtime()
subUrls = open('modePackageUrls.txt')
productListFile = open('modeProductList.txt', 'w')
for each_line in subUrls:
    anCode = each_line[each_line.find('location=') + len('location=LOC'):each_line.find('&location1=')]
    themeCode = each_line[each_line.find('Theme=') + len('Theme='):each_line.find('&Theme1=')]
    fromDate = strftime("%Y", time) + strftime("%m", time) + strftime("%d", time) + strftime("%H", time) + strftime("%M", time)
    toDate = strftime("%Y", nextTime) + strftime("%m", nextTime) + strftime("%d", nextTime) + strftime("%H", nextTime) + strftime("%M", nextTime)
    thisMonth = strftime("%Y", time) + strftime("%m", time)#str(time.tm_year) + str(time.tm_mon)
    #print('LOC : ' + anCode + ', Theme : ' + themeCode + ', Fromdate : ' + fromDate + ', ToDate : ' + toDate + ', thisMonth : ' + thisMonth)
    productUrl = 'http://www.modetour.com/XML/Package/Get_ProductList.aspx?AN=' + anCode + '&Ct=&DateTerm=' + fromDate + '%5E' + toDate + '&PL=1000&Pd=&Pn=1&S=' + thisMonth + '&TN=' + themeCode
    #print(productUrl)
    print >> productListFile, productUrl
subUrls.close()
productListFile.close()
#aa = requests.get("http://www.modetour.com/Package/List.aspx?startLocation=ICN&location=LOC4&location1=LOC4^LOC3&Theme=THE88&Theme1=THE88&MLoc=01")
#http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=06&Pcode=ATE101&Pd=&Type=01&term=201406060000%5E201506052359
#http://www.modetour.com/XML/Package/Get_ProductList.aspx?AN=4&Ct=&DateTerm=201406052346%5E201506042359&PL=1000&Pd=&Pn=1&S=201406&TN=THE88 ==> AN 값이 뭐지?? 전체보기.. PL 값을 최대로... Pn은 페이지 번호.. 1로 설정
#====> AN 값은... location 값을 쓰면 됨...(LOC 빼고..)


productSet = set()
productListFile = open('modeProductList.txt')
for each_line in productListFile:
    productListGet = urllib2.urlopen(each_line).read()#requests.get(each_line).text
    productListXml = xmltodict.parse(productListGet)
    tmpFile = open('ProductCode' + each_line[each_line.find('AN=') + len('AN='):each_line.find('&Ct=')] + '.txt', 'w')
    print >> tmpFile, productListXml
    tmpFile.close()
    #print(type(productListXml))
    for tmpXml in productListXml['ModeTour']['Product']:
        productSet.add(tmpXml['@Pcode'])
    #print(productListXml['ModeTour']['Product'][0]['@Pcode'])
    print(len(productSet))
    break
productListFile.close()

""" xmltodict 사용법..
>>> doc = xmltodict.parse(
<mydocument has="an attribute">
...   <and>
...     <many>elements</many>
...     <many>more elements</many>
...   </and>
...   <plus a="complex">
...     element as well
...   </plus>
... </mydocument>
... )
>>>
>>> doc['mydocument']['@has']
u'an attribute'
>>> doc['mydocument']['and']['many']
[u'elements', u'more elements']
>>> doc['mydocument']['plus']['@a']
u'complex'
>>> doc['mydocument']['plus']['#text']
u'element as well'
"""

""" State 색별 상태..
<xsl:when test="SDetailState = 'red'">
                <img src="http://img.modetour.co.kr/mode2010/modetour/search/btn_posssible.gif" alt="출발확정" title="최소 출발인원 이상 예약이 되어있는 상품으로서 예약과 동시에 출발이 가능합니다. 단, 예약자의 일부가 취소되어 최소 출발인원에 미치지 못할 경우, 행사가 진행되지 못할 수도 있습니다." />
              </xsl:when>
              <xsl:when test="SDetailState = 'blue'">
                <img src="http://img.modetour.co.kr/mode2010/modetour/search/btn_reservepossible.gif" alt="예약가능" title="여유 좌석 내에서 예약이 가능하지만, 단체의 예약인원이 최소 출발인원에 미달하여 출발 여부는 미정인 상태입니다. 최소 출발인원 이상 예약될 경우 출발가능으로 변경됩니다."/>
              </xsl:when>
              <xsl:when test="SDetailState = 'green'">
                <img src="http://img.modetour.co.kr/mode2010/modetour/search/btn_reservewait.gif" alt="대기예약" title="여유 죄석이 없거나 출발이 임박하여 예약가능 시간이 지나 담당자와의 확인이 필요한 상황입니다." />
              </xsl:when>
              <xsl:otherwise>
                <img src="http://img.modetour.co.kr/mode2010/modetour/search/btn_endreserve.gif" alt="예약마감" title="판매가 종료된 상품입니다. 다른 상품이나 다른 날짜를 이용해 주시기 바랍니다." />
              </xsl:otherwise>
            </xsl:choose>"""

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

