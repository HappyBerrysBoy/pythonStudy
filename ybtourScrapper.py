# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 23:48:18 2014

@author: KSC
"""

import xmltodict
import urllib2
import re
import time, datetime
import sys
import savefilegethtml
import codes
import tourUtil
import tourQuery
import cx_Oracle
        
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
        self.detailcode = ''
#print('Product URL : ' + productUrl)
        #productListOpener = urllib2.urlopen(productUrl)
        #productListGet = productListOpener.read()

class classCalc():
    def __init__(self):
        self.day = ''
        self.status = ''
        self.url = ''

defaultUrl = 'http://www.ybtour.co.kr/GoodSearch/Area_Menu_XML.asp?'

tourAgency = 'ybtour'
#targetYear = '2014'
#targetMonth = '07'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

departCity = ''
dmst_div = ''

exceptFile = open('ybtourException' + scrappingStartTime + '.txt', 'w')
print >> exceptFile, "Start : %s" % time.ctime()
ml1List = list()
ml2List = list()
ml3List = list()
productClassList = list()
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
try:
    print '===========================================MainUrl==========================================='
    mainUrl = defaultUrl + 'ML=1&MCD='
    print 'Main URL : ' + mainUrl
    print >> exceptFile, mainUrl
    packageListXml = urllib2.urlopen(mainUrl).read()
    packageListDict = xmltodict.parse(packageListXml)
    
    urlMap = dict()
    urlMap['A01'] = 'overseas'  # overseas
    urlMap['A03'] = 'airtel'    # airtel
    urlMap['A06'] = 'Honeymoon' # Honeymoon
    urlMap['A09'] = 'Overseas'  # Golf
    urlMap['A12'] = 'Overseas'  # 국내 여행... but.. 주소는 Overseas를 사용하네..
    urlMap['A15'] = 'Overseas'  # 지역 출발... but 주소는 Overseas를 사용
    urlMap['A18'] = 'Overseas'    # Cruise but 주소는 Overseas
    
    packageMap = dict()
    packageMap['A01'] = codes.getTourKind('ybtour', 'P')
    packageMap['A03'] = codes.getTourKind('ybtour', 'F')
    packageMap['A06'] = codes.getTourKind('ybtour', 'W')
    packageMap['A09'] = codes.getTourKind('ybtour', 'G')
    packageMap['A12'] = codes.getTourKind('ybtour', 'D')
    packageMap['A15'] = codes.getTourKind('ybtour', 'PUS')
    packageMap['A18'] = codes.getTourKind('ybtour', 'C')
    
    for pack in packageListDict['ROOT']['List']:
        try:
            package = classPackage()
            package.menuCode = pack['MenuCD']
            package.menuName = pack['MenuNM']
            package.goodTypeCode = pack['GoodTypeCD']
            package.sbar = pack['SBAR']
            ml1List.append(package)
            #print 'MenuCD:' + pack['MenuCD'] + ', MenuNM:' + pack['MenuNM'] + ', GoodTypeCD:' + pack['GoodTypeCD'] + ', SBAR:' + pack['SBAR']
            
            if package.menuCode == 'A03':
                continue
            
            print '===========================================Sub1 URL==========================================='
            subUrl = defaultUrl + 'ML=2&MCD=' + package.menuCode
            print 'Sub URL : ' + subUrl
            
            print >> exceptFile, 'Sub URL : ', subUrl
            packageSub1ListXml = urllib2.urlopen(subUrl).read()
            packageSub1ListDict = xmltodict.parse(packageSub1ListXml)
            
            for packSub1 in packageSub1ListDict['ROOT']['List']:
                try:
                    subpackage = classPackage()
                    subpackage.menuCode = packSub1['MenuCD']
                    subpackage.menuName = packSub1['MenuNM']
                    subpackage.goodTypeCode = packSub1['GoodTypeCD']
                    subpackage.sbar = packSub1['SBAR']
                    ml2List.append(subpackage)
                    #print 'MenuCD:' + subpackage.menuCode + ', MenuNM:' + subpackage.menuName + ', GoodTypeCD:' + subpackage.goodTypeCode + ', SBAR:' + str(subpackage.sbar)
                    
                    print '===========================================Sub2 URL==========================================='
                    sub2Url = defaultUrl + 'ML=3&MCD=' + subpackage.menuCode
                    
                    #if sub2Url == 'http://www.ybtour.co.kr/GoodSearch/Area_Menu_XML.asp?ML=3&MCD=A12_03':
                        #print ''
                    
                    print 'Sub2 URL : ' + sub2Url
                    print >> exceptFile, 'Sub2 URL : ', sub2Url
                    packageSub2ListXml = urllib2.urlopen(sub2Url).read()
                    packageSub2ListDict = xmltodict.parse(packageSub2ListXml)
                    
                    #con = tourQuery.getOracleConnection()
                    for packSub2 in packageSub2ListDict['ROOT']['List']:
                        try:
                            sub2package = classPackage()
                            sub2package.menuCode = packSub2['MenuCD']
                            sub2package.menuName = packSub2['MenuNM']
                            sub2package.goodTypeCode = packSub2['GoodTypeCD']
                            sub2package.sbar = packSub2['SBAR']
                            ml3List.append(sub2package)
                            #print 'MenuCD:' + sub2package.menuCode + ', MenuNM:' + sub2package.menuName + ', GoodTypeCD:' + sub2package.goodTypeCode + ', SBAR:' + str(sub2package.sbar)
                            
                            print '===========================================productList URL==========================================='
                            #출발지 구분
                            if package.menuCode == 'A15':
                                departCity = 'PUS'
                            else:
                                departCity = 'ICN'
                            
                            #해외 국내 구분
                            if package.menuCode == 'A12':
                                dmst_div = 'D'
                            else:
                                dmst_div = 'A'
                                
                            #if not (str(sub2package.sbar) == '1511' or sub2package.sbar == 1511):
                                #continue
                            
                            #con = tourQuery.getOracleConnection()

                            defaultproductListUrl = 'http://www.ybtour.co.kr/Goods/' + urlMap[package.menuCode] + '/list.asp?sub_area_cd=' + str(sub2package.sbar)
                            print 'List URL : ' + defaultproductListUrl
                            
                            print >> exceptFile, 'List URL : ', defaultproductListUrl
                            productList = urllib2.urlopen(defaultproductListUrl).read()
                            codeList = re.findall(r"goodFocus\w*", productList)
                            
                            productNameList = list()
                            productCommentList = list()
                            productNameHtml = productList[productList.find('travel_top_section'):productList.find('frmGD')]
                            productNameHtml = savefilegethtml.htmlToList(productNameHtml, 'xxx.txt')
                            for pdName in productNameHtml:
                                if pdName.find('height="110" alt="') > 0:
                                    productNameList.append(pdName.split('alt="')[1].split('"')[0].replace("'", "").strip().decode('utf-8'))
                                # description을.. 다른놈으로 가져가야 할듯.. route로..
                                #if pdName.find('<p class="desc">') > 0:
                                    #productCommentList.append(pdName.split('desc">')[1].split('<')[0].replace("'", "").strip().decode('utf-8'))
                                if pdName.find('<p class="route">') > 0:
                                    productCommentList.append(tourUtil.getRemovedHtmlTag(pdName).strip().replace("'", "").decode('utf-8'))
                                    
                            #today = today.replace(month = today.month + 1)
                            codeIdx = 0
    
                            for pcode in codeList:
                                detailProduct = pcode.split('s')[1]
                                
                                detailProductUrl = ''
                                if not (package.menuCode == 'A03' or package.menuCode == 'A06'):       # 출발일정 눌렀을때 List가 펼쳐지는 경우랑, 페이지가 이동하는 경우 나눔..
                                    detailProductUrl = ''
                                    #if package.menuCode == 'A01':
                                    detailProductUrl = 'http://www.ybtour.co.kr/Goods/' + urlMap[package.menuCode] + '/inc_evList_ajax.asp?goodCD=' + detailProduct + '&startDT=' + targetYear + targetMonth
                                        
                                    #if detailProductUrl == 'http://www.ybtour.co.kr/Goods/Overseas/inc_evList_ajax.asp?goodCD=JAA2013113&startDT=201407':
                                        #print ''
                                    
                                    print 'Detail Product URL : ' + detailProductUrl
                                    print >> exceptFile, 'Detail Product URL : ', detailProductUrl
                                    detailProductList = savefilegethtml.getHtml(detailProductUrl, '', '', 'ybtourTempFile.txt')
                                    
                                    try:
                                        # 2014. 06. 29. 여행상품명에서 국가, 도시코드 가져오는 부분으로 적용..
                                        codeLists = codes.getCityCode(productNameList[codeIdx], sub2package.menuName, productCommentList[codeIdx], subpackage.menuName)
                                        cityList = codeLists[0]
                                        nationList = codeLists[1]
                                        continentList = codeLists[2]
                                        
                                        #print cityList
                                        #print nationList
                                        #print continentList
                                        
                                        query = tourQuery.getMasterMergeQuery(tourAgency, detailProduct, productNameList[codeIdx], packageMap[package.menuCode], dmst_div, productCommentList[codeIdx], '')
                                    
                                        #print query
                                        
                                        codeIdx += 1
                                        cursor = con.cursor()
                                        cursor.execute(query)
                                        con.commit()
                                        codes.insertRegionData(tourAgency, detailProduct, cityList, nationList, continentList)
                                        
                                        flag = False
                                        clsProduct = classProduct()
                                        for parcer in detailProductList:
                                            try:
                                                if parcer.strip()[:len('<td><input type="checkbox"')] == '<td><input type="checkbox"':
                                                    flag = True
                                                    clsProduct = classProduct()
                                                
                                                if flag:
                                                    if parcer.find('<td><span class="blue">') > -1:
                                                        spliter = parcer.strip().split(' ')
                                                        clsProduct.departDay = spliter[1].split('>')[1].replace('/', '').strip()
                                                        clsProduct.departTime = spliter[3].split('<')[0].replace(':', '').strip()
                                                        clsProduct.arriveDay = spliter[4].split('>')[2].replace('/', '').strip()
                                                        clsProduct.arriveTime = spliter[6].split('<')[0].replace(':', '').strip()
                                                        #print >> ybtourproductfile, 'departday:' + str(clsProduct.departDay) + ', departtime:'  + str(clsProduct.departTime) + ', arrDay:' + str(clsProduct.arriveDay) + ', arrTime:' + str(clsProduct.arriveTime)
                                                    elif parcer.find('absmiddle') > -1 and parcer.find('air') > -1:
                                                        #clsProduct.airCode = parcer.replace('"', '').replace("'", "").split("alt=")[1].split(" ")[0].decode('utf-8')        # 한글코드말고 영문코드로 변경
                                                        clsProduct.airCode = parcer[parcer.find('.gif') - 4:parcer.find('.gif') - 2]
                                                        #print >> ybtourproductfile, 'airCode:' + clsProduct.airCode
                                                    elif parcer.find('<td class="lt"><a href="') > -1:
                                                        clsProduct.detailcode = parcer.split('ev_seq=')[1].split('&')[0]
                                                        spliter = parcer.strip().split(' ')
                                                        clsProduct.url = 'http://www.ybtour.co.kr' + spliter[2].split('"')[1]
                                                        spliter = parcer.strip().split('>')
                                                        clsProduct.productName = spliter[2].split('<')[0].replace("'", '').decode('utf-8')
                                                        #print >> ybtourproductfile, 'URL:' + clsProduct.url + ', Name:' + clsProduct.productName
                                                    elif parcer.find('박') > -1 and len(parcer) < 9:
                                                        clsProduct.period = parcer.strip()[:1]
                                                        #print >> ybtourproductfile, 'Period:' + clsProduct.period
                                                    elif parcer.find('<td class="blue">') > -1 and parcer.find('원') > -1:
                                                        spliter = parcer.strip().split('>')
                                                        clsProduct.price = spliter[1].split('원')[0].replace(',', '')
                                                        #print >> ybtourproductfile, 'Price:' + clsProduct.price
                                                    elif parcer.find('출발확정') > -1 or parcer.find('예약마감') > -1 or parcer.find('예약가능') > -1:
                                                        spliter = parcer.strip().split('>')
                                                        #print codes.getStatus('ybtour', spliter[1].split('<')[0])
                                                        clsProduct.status = codes.getStatus('ybtour', spliter[1].split('<')[0])
                                                        #print >> ybtourproductfile, 'Status:' + clsProduct.status
                                                    elif parcer.strip() == '</tr>':
                                                        flag = False
                                                        # 2014. 06. 29. 여행상품명에서 국가, 도시코드 가져오는 부분으로 적용..
                                                        
                                                        query = tourQuery.getDetailMergeQuery(tourAgency, detailProduct, clsProduct.detailcode, clsProduct.productName, targetYear+clsProduct.departDay+clsProduct.departTime, targetYear+clsProduct.arriveDay+clsProduct.arriveTime, clsProduct.period, departCity, '', clsProduct.airCode, clsProduct.status, clsProduct.url, clsProduct.price, '0', '0', '0', '') 
                                                        #query = savefilegethtml.getDetailMergeQuery('ybtour', detailProduct, clsProduct.detailcode, clsProduct.productName, targetYear+clsProduct.departDay+clsProduct.departTime, targetYear+clsProduct.arriveDay+clsProduct.arriveTime, clsProduct.period, departCity, '', clsProduct.airCode, clsProduct.status, clsProduct.url, clsProduct.price, '0', '0', '0', '') 
                                                        #print query
                                                        con.commit()
                                                        cursor = con.cursor()
                                                        cursor.execute(query)
                                                        con.commit()
                                                        #break
                                            except:
                                                print "ML5 Parcing Error:", sys.exc_info()[0]
                                                print >> exceptFile, "ML5 Parcing Error:", sys.exc_info()[0]
                                                pass
                                            
                                        #break
                                    except UnicodeEncodeError as err1:
                                        print >> exceptFile, err1
                                        pass
                                    except:
                                        print "ML4 Parcing Error:", sys.exc_info()[0]
                                        print >> exceptFile, "ML4 Parcing Error:", sys.exc_info()[0]
                                        pass
                                    
                                elif package.menuCode == 'A03' or package.menuCode == 'A06':                            # 출발일정 눌렀을때 페이지가 이동하는 경우
                                    # 달력에서 일정 뽑고, 세부 List에서 가격 기타 정보 뽑고
                                    #detailProductUrl = 'http://www.ybtour.co.kr/Goods/' + urlMap[package.menuCode] + '/inc_evList_ajax.asp?goodCD=' + detailProduct + '&startDT=' + targetYear + targetMonth
                                    if len(detailProduct) < 8:
                                        continue
                                    
                                    #달력..
                                    calUrl = 'http://www.ybtour.co.kr/Goods/overseas/inc_view_cal_dev.asp?good_type_cd='+detailProduct[:1]+'&area_cd='+detailProduct[1:3]+'&good_yy='+detailProduct[3:7]+'&good_seq='+detailProduct[7:]
                                    dayList = savefilegethtml.getHtml(calUrl, 'td', 'cal_desc', 'ybtourCalc.txt')
                                    
                                    availDay = False
                                    clsCalc = classCalc()
                                    calList = list()
                                    for day in dayList:
                                        try:
                                            if day.find('<td width') > -1:
                                                if day.find('#') > -1:
                                                    clsCalc = classCalc()
                                                    if day.upper().find('#F5DEDE') > -1:
                                                        clsCalc.status = codes.getStatus('ybtour', '예약가능')
                                                    elif day.upper().find('#EDC6C6') > -1:
                                                        clsCalc.status = codes.getStatus('ybtour', '예약대기')
                                                    elif day.upper().find('#ECECEC') > -1:
                                                        clsCalc.status = codes.getStatus('ybtour', '예약마감')
                                                    availDay = True
                                                else:
                                                    availDay = False
                                            elif availDay and day.find('a href=') > -1:
                                                clsCalc.url = 'http://www.ybtour.co.kr/goods/' + urlMap[package.menuCode] + '/view.asp?ev_ym=' + targetYear + targetMonth + '&ev_seq=' + day.split('ev_seq=')[1].split('"')[0]
                                            elif availDay and day.find('<font color') > -1:
                                                clsCalc.day = tourUtil.getRemovedHtmlTag(day)
                                                calList.append(clsCalc)
                                        except:
                                            print >> exceptFile, "Calculation Parcing Error:", sys.exc_info()[0]
                                            pass
                                            
                                            
                                    #con = tourQuery.getOracleConnection()
                                    
                                    codeLists = codes.getCityCode(productNameList[codeIdx], sub2package.menuName, productCommentList[codeIdx], subpackage.menuName)
                                    cityList = codeLists[0]
                                    nationList = codeLists[1]
                                    continentList = codeLists[2]
                                    #print cityList
                                    #print nationList
                                    #print continentList
                                        
                                    query = tourQuery.getMasterMergeQuery(tourAgency, detailProduct, productNameList[codeIdx], packageMap[package.menuCode], dmst_div, productCommentList[codeIdx], '')

                                    #print query
                                    cursor = con.cursor()
                                    cursor.execute(query)
                                    con.commit()
                                    codes.insertRegionData(tourAgency, detailProduct, cityList, nationList, continentList)
                                    
                                    
                                    # 저장된 날짜들을 기준으로 세부 페이지 호출.... ㄷㄷㄷ
                                    for cal in calList:
                                        try:
                                            print 'Calc Detail URL :', cal.url
                                            print >> exceptFile, 'Calc Detail URL :', cal.url
                                            detailInfos = savefilegethtml.getHtml(cal.url, '<table class="table1">', '<div class="aside_wrap">', 'ybtourDetailInfoHtml.txt')
    
                                            chkDepartInfo = False
                                            chkArriveInfo = False
                                            chkAirlineInfo = False
                                            period = 0
                                            dDay = ''
                                            dTime = ''
                                            aDay = ''
                                            url = ''
                                            airCode = ''
                                            price = ''
                                            productSeq = ''
                                            
                                            for detailInfo in detailInfos:
                                                try:
                                                    if detailInfo.find('detail01.gif') > -1:
                                                        chkDepartInfo = True
                                                        chkAirlineInfo = False
                                                    elif chkDepartInfo and detailInfo.find('<br>') > -1:
                                                        dDay = detailInfo.split('월')[1].split('일')[0].strip()
                                                        chkDepartInfo = False
                                                    elif detailInfo.find('detail02.gif') > -1:
                                                        chkArriveInfo = True
                                                    elif chkArriveInfo and detailInfo.find('년') > -1 and detailInfo.find('<br>') < 0:
                                                        aDay = detailInfo.split('월')[1].split('일')[0].strip()
                                                        chkArriveInfo = False
                                                    elif detailInfo.find('class="lt"') > -1:
                                                        if detailInfo.find('goGoodsViewAirtel') > -1:
                                                            productSeq = detailInfo.split('goGoodsViewAirtel')[1].split(',')[1].split(')')[0].strip()
                                                        elif detailInfo.find('goGoodsViewHoneyMoon') > -1:
                                                            productSeq = detailInfo.split('goGoodsViewHoneyMoon')[1].split(',')[1].split(')')[0].strip()
                                                        url = 'http://www.ybtour.co.kr/goods/' + urlMap[package.menuCode] + '/view.asp?ev_ym=' + targetYear + targetMonth + '&ev_seq=' + productSeq
                                                        if detailInfo.find('absmiddle') > -1:
                                                            airCode = detailInfo[detailInfo.find('.gif') - 4:detailInfo.find('.gif') - 2]
                                                        chkAirlineInfo = True
                                                    elif chkAirlineInfo and detailInfo.find('absmiddle') > -1:
                                                        airCode = detailInfo[detailInfo.find('.gif') - 4:detailInfo.find('.gif') - 2]
                                                    elif chkAirlineInfo and detailInfo.find('<strong>') > -1:
                                                        numArray = tourUtil.getNumArray(tourUtil.getRemovedHtmlTag(detailInfo))
                                                        for tmp in numArray:
                                                            period += int(tmp)
                                                    elif chkAirlineInfo and detailInfo.find('<em>') > -1:
                                                        price = re.sub('[^0-9]', '', tourUtil.getRemovedHtmlTag(detailInfo))
                                                        
                                                        query = tourQuery.getDetailMergeQuery(tourAgency, detailProduct, productSeq, productNameList[codeIdx], targetYear+targetMonth+dDay, targetYear+targetMonth+aDay, str(period), departCity, '', airCode, cal.status, url, price, '0', '0', '0', '') 
                                                        #print query
                                                        cursor = con.cursor()
                                                        cursor.execute(query)
                                                        con.commit()
                                                        #break
                                                except:
                                                    print >> exceptFile, "Free2 Parcing Error:", sys.exc_info()[0]
                                                    pass
                                            #break
                                        except:
                                            print >> exceptFile, "Free Parcing Error:", sys.exc_info()[0]
                                            pass
                                        
                                    codeIdx += 1
                                    """
                                    예약 불가능한 날짜
                                    <td width="27" height="21" align="center" class="font_num" style="background-color:;">
    								
    							<font color="#ec1515">6</font>
                                    
                                    얘약가능한 날짜
                                    <td width="27" height="21" align="center" class="font_num" style="background-color:#f5dede;">
    								
    								<a href="view.asp?ev_ym=201407&ev_seq=35620">
    								
    							<font color="#ec1515"><strong>7</font>	
                                    
                                    대기 가능 날짜
                                    <td width="27" height="21" align="center" class="font_num" style="border: 2px solid #F15F5F; background-color:#EDC6C6;">
    								
    								<a href="view.asp?ev_ym=201407&ev_seq=23484">
    																	
    							<font color="white"><strong>11</font></div>
    
                                    
                                    예약 마감된 날짜
                                    <td width="27" height="21" align="center" class="font_num" style="background-color:#ececec;">
    								
    								<a href="view.asp?ev_ym=201407&ev_seq=35639">
    								
    							<font color="#666666"><strong>26</font>
                                    """
                            #break
                        except ValueError as err:
                            print 'ML3-2 Parcing Error : ' + err.message
                            pass
                        except:
                            print "ML3 Parcing Error:", sys.exc_info()[0]
                            print >> exceptFile, "ML3 Parcing Error:", sys.exc_info()[0]
                            pass
                        
                    #break
                except:
                    print "ML2 Parcing error:", sys.exc_info()[0]
                    print >> exceptFile, "ML2 Parcing Error:", sys.exc_info()[0]
                    pass
            #break
        except:
            print "ML1 Parcing error:", sys.exc_info()[0]
            print >> exceptFile, "ML1 Parcing Error:", sys.exc_info()[0]
            pass
except:
    print "urllib2 Error(Main) error:", sys.exc_info()[0]
    print >> exceptFile, "urllib2 Error(Main) error:", sys.exc_info()[0]
    pass
finally:
    con.commit()
    con.close()    

print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()





