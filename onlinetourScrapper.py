# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 20:38:23 2014

@author: KSC
"""

import sys
import time, datetime
import codes
import tourQuery
import cx_Oracle
import savefilegethtml
import tourUtil

# 여행종류 및 국가정보(대륙)는 상품번호 앞 3자리로 구분
# 첫번째 자리 : 해외패키지 ==> 1:해외패키지, 2:허니문, 3:골프, 7:해외자유배낭, D:부산출발, 국내여행은.. 별도로 빼야 할듯!!
# 두번째~세번째 자리 : 국가(대륙), 허니문은... 또 예외인듯... 음... 그럴거면 차라리 3자리 통으로 따서.. 패키지, 지역 정보 가져오는게 나을듯.. => 그렇게하자!!
region = dict()
region['110'] = '해외패키지,동남아'
region['120'] = '해외패키지,일본'
region['130'] = '해외패키지,중국'
region['140'] = '해외패키지,괌/사이판'
region['150'] = '해외패키지,남태평양'
region['160'] = '해외패키지,유럽'
region['170'] = '해외패키지,미주/특수'

region['710'] = '해외자유배낭,동남아'
region['720'] = '해외자유배낭,일본'
region['730'] = '해외자유배낭,중국'
region['760'] = '해외자유배낭,유럽'
region['770'] = '해외자유배낭,미주/특수'
region['750'] = '해외자유배낭,남태평양'
region['740'] = '해외자유배낭,괌/사이판'
region['7TR'] = '해외자유배낭,트레킹'

region['330'] = '골프,중국'
region['320'] = '골프,일본'
region['310'] = '골프,동남아'
region['340'] = '골프,괌/사이판'

region['230'] = '허니문,미주'
region['240'] = '허니문,몰디브'
region['210'] = '허니문,태국'
region['220'] = '허니문,발리'
region['215'] = '허니문,필리핀'
region['245'] = '허니문,유럽'
region['246'] = '허니문,호주/피지'
region['225'] = '허니문,괌/사이판'
region['247'] = '허니문,칸쿤/기타'

region['D'] = '부산출발,해외패키지'
region['8'] = '부산출발,해외자유여행'
region['BE1BE17'] = '부산출발,국내제주여행'

class clsDetailRegionUrls():
    def __init__(self):
        self.name = ''
        self.url = ''

class clsSubMenuUrls():
    def __init__(self):
        self.name = ''
        self.url = ''
        self.detailRegionList = list()

class clsMenuUrls():
    def __init__(self):
        self.name = ''
        self.url = ''
        self.tourType = ''
        self.dmst_div = ''
        self.departCity = ''
        self.subMenuList = list()
        
class clsProduct():
    def __init__(self):
        self.productCode = ''
        self.productName = ''
        self.description = ''
        self.night = ''
        self.period = ''
        self.detailUrl = ''
        
class clsDetailProduct():
    def __init__(self):
        self.status = ''
        self.price = ''
        self.url = ''
        self.productName = ''
        self.dDay = ''
        self.dTime = ''
        self.aDay = ''
        self.aTime = ''
        self.airCode = ''
        self.proc_cd = ''

def pusanUrl(name, url):
    subMenuUrls = clsSubMenuUrls()
    subMenuUrls.name = name
    subMenuUrls.url = url
    
    print subMenuUrls.name.decode('utf-8') + ' : ' + subMenuUrls.url
    #print >> exceptFile, subMenuUrls + ' : ' + subMenuUrls.url
    
    detailProductPusanHtml = savefilegethtml.getHtml(subMenuUrls.url, 'class="container', '<!-- end .ot_tab_style1 -->', 'onlinetourSubPagePusan.txt')
    
    for subMenu in detailProductPusanHtml:
        #if subMenu.find('<li class="">') > -1 and subMenu.find('전체') < 0:
        if subMenu.find('<li') > -1 and subMenu.find('<a') > -1 and (subMenu.find('전체') < 0 or subMenuUrls.url.find('D50') > -1  or subMenuUrls.url.find('D60') > -1  or subMenuUrls.url.find('D70') > -1):
            detailRegionUrls = clsDetailRegionUrls()
            detailRegionUrls.name = tourUtil.getRemovedHtmlTag(subMenu).strip()
            detailRegionUrls.url = mainUrl + tourUtil.getTagAttr(subMenu, 'a', 'href')
            subMenuUrls.detailRegionList.append(detailRegionUrls)
            
            print detailRegionUrls.name.decode('utf-8') + ' : ' + detailRegionUrls.url
            #print >> exceptFile, detailRegionUrls.name + ' : ' + detailRegionUrls.url
            
    return subMenuUrls



# 시간 변수들..
tourAgency = 'onlinetour'
mainUrl = 'http://www.onlinetour.co.kr/web/tour'
mainUrl2 = 'http://www.onlinetour.co.kr'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
#targetYear = '2014'
#targetMonth = '07'
scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

exceptFileName = 'onlinetourException' + scrappingStartTime + '.txt'
exceptFile = open(exceptFileName, 'w')
print >> exceptFile, "Start : %s" % time.ctime()

mainpageHtml = savefilegethtml.getHtml('http://www.onlinetour.co.kr/web/home', '<li id="n_pack">', '<!--}} ot_navi-->', 'onlinetourMainPage.txt')

# URL 쑤셔넣는 부분...
mainMenuList = list()
mainMenuUrls = clsMenuUrls()
subMenuUrls = clsSubMenuUrls()
detailRegionUrls = clsDetailRegionUrls()
chkFree = False
chkDomestic = False
for menuList in mainpageHtml:
    try:
        #print menuList
        if menuList.find('<a href=') > -1 and menuList.find('<li>') < 0:
            mainMenuUrls = clsMenuUrls()
            mainMenuUrls.name = tourUtil.getRemovedHtmlTag(menuList).strip()
            mainMenuUrls.url = tourUtil.getTagAttr(menuList, 'a', 'href')
            mainMenuUrls.dmst_div = 'A'
            if menuList.find('부산출발') > -1:
                mainMenuUrls.departCity = 'PUS'
                # 부산의 경우.. 세부 지역 URL이 바로 노출되어 있지 않아.. 강제로 쭈셔 넣어 준다..
                mainMenuUrls.subMenuList.append(pusanUrl('동남아', 'http://www.onlinetour.co.kr/web/tour?region_cd=D10'))
                mainMenuUrls.subMenuList.append(pusanUrl('일본', 'http://www.onlinetour.co.kr/web/tour?region_cd=D20'))
                mainMenuUrls.subMenuList.append(pusanUrl('중국', 'http://www.onlinetour.co.kr/web/tour?region_cd=D30'))
                mainMenuUrls.subMenuList.append(pusanUrl('괌/사이판', 'http://www.onlinetour.co.kr/web/tour?region_cd=D40'))
                mainMenuUrls.subMenuList.append(pusanUrl('남태평양', 'http://www.onlinetour.co.kr/web/tour?region_cd=D50'))
                mainMenuUrls.subMenuList.append(pusanUrl('유럽/특수', 'http://www.onlinetour.co.kr/web/tour?region_cd=D60'))
                mainMenuUrls.subMenuList.append(pusanUrl('미주/특수', 'http://www.onlinetour.co.kr/web/tour?region_cd=D70'))
            else:
                mainMenuUrls.departCity = 'ICN'
            
            mainMenuUrls.tourType = codes.getTourKind(tourAgency, mainMenuUrls.name)
            
            print mainMenuUrls.name.decode('utf-8') + ' : ' + mainMenuUrls.url + ' : ' + mainMenuUrls.tourType
            #print >> exceptFile, mainMenuUrls.name + ' : ' + mainMenuUrls.url + ' : ' + mainMenuUrls.tourType
            
            if menuList.find('국내여행') > -1:
                chkDomestic = True
        elif not chkDomestic and menuList.find('<li><a href=') > -1 and menuList.find('region_cd=') > -1 and menuList.find('전체') < 0:
            subMenuUrls = clsSubMenuUrls()
            subMenuUrls.name = tourUtil.getRemovedHtmlTag(menuList).strip()
            subMenuUrls.url = tourUtil.getTagAttr(menuList, 'a', 'href')
            
            print subMenuUrls.name.decode('utf-8') + ' : ' + subMenuUrls.url
            #print >> exceptFile, 'subMenuUrls : ' + subMenuUrls.url
            
            detailProductHtml = savefilegethtml.getHtml(subMenuUrls.url, 'class="container', '<!-- end .ot_tab_style1 -->', 'onlinetourSubPage.txt')
            #print >> exceptFile, 'subMenuUrls !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            
            for subMenu in detailProductHtml:
                #if subMenu.find('<li class="">') > -1 and subMenu.find('전체') < 0:
                if subMenu.find('<li') > -1 and subMenu.find('<a') > -1 and subMenu.find('전체') < 0:
                    detailRegionUrls = clsDetailRegionUrls()
                    detailRegionUrls.name = tourUtil.getRemovedHtmlTag(subMenu).strip()
                    detailRegionUrls.url = mainUrl + tourUtil.getTagAttr(subMenu, 'a', 'href')
                    subMenuUrls.detailRegionList.append(detailRegionUrls)
                    
                    print detailRegionUrls.name.decode('utf-8') + ' : ' + detailRegionUrls.url
                    #print >> exceptFile, detailRegionUrls.name + ' : ' + detailRegionUrls.url
                    
            mainMenuUrls.subMenuList.append(subMenuUrls)
            
        elif chkDomestic:
            if menuList.find('제주여행') > -1:
                subMenuUrls = clsSubMenuUrls()
                subMenuUrls.name = '제주'
                subMenuUrls.url = tourUtil.getTagAttr(menuList, 'a', 'href')
                
                print subMenuUrls.name.decode('utf-8') + ' : ' + subMenuUrls.url
                #print >> exceptFile, subMenuUrls.name + ' : ' + subMenuUrls.url
                
                detailProductHtml = savefilegethtml.getHtml(subMenuUrls.url, 'class="container"', '<!-- end .ot_tab_style1 -->', 'onlinetourSubPage.txt')
            
                # 제주는 일반 위에 패키지랑 동일하게 되는지 확인이 필요..
                for subMenu in detailProductHtml:
                    if subMenu.find('<li class="">') > -1 and subMenu.find('전체') < 0:
                        detailRegionUrls = clsDetailRegionUrls()
                        detailRegionUrls.name = tourUtil.getRemovedHtmlTag(subMenu).strip()
                        detailRegionUrls.url = mainUrl + tourUtil.getTagAttr(subMenu, 'a', 'href')
                        subMenuUrls.detailRegionList.append(detailRegionUrls)
                        
                        print detailRegionUrls.name.decode('utf-8') + ' : ' + detailRegionUrls.url
                        #print >> exceptFile, detailRegionUrls.name + ' : ' + detailRegionUrls.url
                
                mainMenuUrls.subMenuList.append(subMenuUrls)
                
        elif menuList.find('</li>') > -1 and menuList.find('<a href=') < 0:
            mainMenuList.append(mainMenuUrls)
            
    except:
        print >> exceptFile, "Main URL Error :", sys.exc_info()[0]
        print >> exceptFile, "menuList : ", menuList
        pass


# URL에서 세부 상품 내역 조회...
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
for mainMenu in mainMenuList:
    print 'Main Url : ' + mainMenu.name.decode('utf-8') + ' : ' + mainMenu.url
    print >> exceptFile, 'Main Url : ' + mainMenu.name + ' : ' + mainMenu.url
    for subMenu in mainMenu.subMenuList:
        print 'Main Sub : ' + subMenu.name.decode('utf-8') + ' : ' + subMenu.url
        print >> exceptFile, 'Main Sub : ' + subMenu.name + ' : ' + subMenu.url
        for detail in subMenu.detailRegionList:
            try:
                print 'Detail Item : ' + detail.name.decode('utf-8') + ' : ' + detail.url
                print >> exceptFile, 'Detail Item : ' + detail.name + ' : ' + detail.url
                
                #if detail.url != 'http://www.onlinetour.co.kr/web/tour?region_cd=1707006':
                    #continue
                
                regionCode = detail.url[detail.url.find('region_cd=') + len('region_cd='):]
                productsHtml = savefilegethtml.getHtml(detail.url, 'class="travel_body"', 'class="ot_pager"', 'onlinetourProductHtml.txt')
                #detailHtml = savefilegethtml.getHtml(detail.url, 'class="list"', '', 'onlinetourDetailHtml.txt')
                
                productCls = clsProduct()
                chkDesc = False
                for detailProduct in productsHtml:
                    try:
                        if detailProduct.find('id="goods') > -1:
                            productCls = clsProduct()
                            productCls.productCode = detailProduct.split('id="goods_')[1].split('"')[0]
                        elif detailProduct.find('<a href=') > -1 and detailProduct.find('<img src') < 0:
                            productCls.productName = tourUtil.getRemovedHtmlTag(detailProduct).strip().replace("'", "")
                        elif detailProduct.find('class="description"') > -1:
                            chkDesc = True
                        elif chkDesc:
                            chkDesc = False
                            productCls.description = detailProduct.strip()
                        elif detailProduct.find('class="period"') > -1:
                            tmpPeriod = tourUtil.getNumArray(tourUtil.getRemovedHtmlTag(detailProduct).strip())
                            if len(tmpPeriod) > 1:
                                productCls.night = tmpPeriod[1]
                                productCls.period = tmpPeriod[0]
                            elif len(tmpPeriod) > 0:
                                productCls.period = tmpPeriod[0]
                                
                            productCls.detailUrl = mainUrl + '/' + productCls.productCode + '/events?start_month=' + targetYear + targetMonth + '&region_cd=' + regionCode
                            print 'productCls.detailUrl : ', productCls.detailUrl
                            print >> exceptFile, 'productCls.detailUrl : ', productCls.detailUrl
                            
                            #print productCls.productName
                            #print detail.name
                            #print productCls.description
                            # 2014. 7. 23. 카테고리의 국가는 넣지 않기로 함...
                            #codeList = codes.getCityCode(productCls.productName, detail.name, productCls.description)
                            codeList = codes.getCityCode(productCls.productName, productCls.description)
                            cityList = codeList[0]
                            nationList = codeList[1]
                            continentList = codeList[2]
                            siteList = codeList[3]              # 2014. 8. 3. site 추가
                            
                            if len(cityList) == 0 and len(nationList) == 0 and len(continentList) == 0 and len(siteList) == 0:
                                codeList = codes.getCityCode(detail.name)
                                cityList = codeList[0]
                                nationList = codeList[1]
                                continentList = codeList[2]
                                siteList = codeList[3]          # 2014. 8. 3. site 추가
                            
                            # Master 상품 입력
                            query = tourQuery.getMasterMergeQuery(tourAgency, productCls.productCode, productCls.productName.decode('utf-8'), mainMenu.tourType, mainMenu.dmst_div, productCls.description.decode('utf-8'), '')
                            #print query
                            cursor = con.cursor()
                            cursor.execute(query)
                            con.commit()
                            # Region Data 삭제
                            codes.insertRegionData(tourAgency, productCls.productCode, cityList, nationList, continentList, siteList)   # 2014. 8. 3. site 추가
                            
                            detailProductHtml = savefilegethtml.getHtml(productCls.detailUrl, 'class="list"', '', 'onlinetourDetailProductHtml.txt')
                            
                            detailProductCls = clsDetailProduct()
                            chkPrice = False
                            for detailInfo in detailProductHtml:
                                try:
                                    if detailInfo.find('airline_cd') > -1:
                                        detailProductCls = clsDetailProduct()
                                        if detailInfo.find('비') > -1 or detailInfo.find('티') > -1:
                                            detailProductCls.airCode = ''
                                        else:
                                            detailProductCls.airCode = tourUtil.getTagAttr(detailInfo, 'tr', 'airline_cd')
                                        #print 'airCode : ', detailProductCls.airCode
                                    elif detailInfo.find('class="start"') > -1:
                                        numArray = tourUtil.getNumArray(tourUtil.getRemovedHtmlTag(detailInfo).strip())
                                        if len(numArray) > 3:
                                            detailProductCls.dTime = numArray[2] + numArray[3]
                                        if len(numArray) > 1:
                                            detailProductCls.dDay = targetYear + numArray[0] + numArray[1]
                                        if len(numArray) < 1:
                                            detailProductCls.dDay = ''
                                            detailProductCls.dTime = ''
                                        #print 'depart time : ', detailProductCls.dDay + detailProductCls.dTime
                                    elif detailInfo.find('class="end"') > -1:
                                        numArray = tourUtil.getNumArray(tourUtil.getRemovedHtmlTag(detailInfo).strip())
                                        if len(numArray) > 3:
                                            detailProductCls.aTime = numArray[2] + numArray[3]
                                        if len(numArray) > 1:
                                            detailProductCls.aDay = targetYear + numArray[0] + numArray[1]
                                        if len(numArray) < 1:
                                            detailProductCls.aDay = ''
                                            detailProductCls.aTime = ''
                                        #print 'arrive time : ', detailProductCls.aDay + detailProductCls.aTime
                                    elif detailInfo.find('class="product_name"') > -1:
                                        detailProductCls.productName = tourUtil.getRemovedHtmlTag(detailInfo).strip().replace("'", "")
                                        detailProductCls.url = mainUrl2 + tourUtil.getTagAttr(detailInfo, 'a', 'href')
                                        detailProductCls.proc_cd = detailInfo.split('/web/tour/')[1].split('?')[0]
                                        #print 'productname : ', detailProductCls.productName.decode('utf-8')
                                        #print 'url : ', detailProductCls.url
                                        #print 'proc_cd : ', detailProductCls.proc_cd
                                    elif detailInfo.find('class="wons"') > -1:
                                        chkPrice = True
                                    elif chkPrice:
                                        chkPrice = False
                                        numArray = tourUtil.getNumArray(detailInfo)
                                        detailProductCls.price = ''
                                        for num in numArray:
                                            detailProductCls.price += num
                                        #print 'Price : ', detailProductCls.price
                                    elif detailInfo.find('class="reservation"') > -1:
                                        if detailInfo.find('예약마감') > -1:
                                            detailProductCls.status = codes.getStatus('onlinetour', 'Finish')
                                        elif detailInfo.find('예약가능') > -1:
                                            detailProductCls.status = codes.getStatus('onlinetour', 'Avail')
                                        elif detailInfo.find('출발가능') > -1:
                                            detailProductCls.status = codes.getStatus('onlinetour', 'Confirm')
                                        else:
                                            detailProductCls.status = 'Etc'
                                            
                                        #print 'status : ', detailProductCls.status
                                        #print >> exceptFile, 'status : ', detailProductCls.status
            
                                        query = tourQuery.getDetailMergeQuery(tourAgency, productCls.productCode, detailProductCls.proc_cd, detailProductCls.productName.decode('utf-8'), detailProductCls.dDay + detailProductCls.dTime, detailProductCls.aDay+detailProductCls.aTime, productCls.period, mainMenu.departCity, '', detailProductCls.airCode, detailProductCls.status, detailProductCls.url, detailProductCls.price, '0', '0', '0', '', productCls.night) 
                                        #print query
                                        cursor = con.cursor()
                                        cursor.execute(query)
                                        con.commit()
                                        #break
                                except:
                                   print >> exceptFile, "Level3 Error :", sys.exc_info()[0]
                                   pass 
                            #break
                            
                    except:
                        print >> exceptFile, "Level2 Error :", sys.exc_info()[0]
                        pass
                #break
            except:
                print >> exceptFile, "Level1 Error :", sys.exc_info()[0]
                pass
        #break
    #break

query = tourQuery.updDepArrYMD(tourAgency, targetYear, targetMonth)
cursor = con.cursor()
cursor.execute(query)

con.close()
print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()