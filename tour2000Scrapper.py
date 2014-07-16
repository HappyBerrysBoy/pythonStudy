# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 00:49:14 2014

@author: KSC
"""

import cx_Oracle
import savefilegethtml
import sys
import time, datetime
import codes
import tourQuery
import tourUtil

#투어2000 상태코드, 날짜 선택하는 부분에서.. class 값이 tx_re01 : 예약마감, tx_re02 : 예약가능, tx_re03 : 출발확정, tx_re04 : 대기예약

class clsDetailMenu():
    def __init__(self):
        self.name = ''
        self.url = ''

class clsSubMenu():
    def __init__(self):
        self.name = ''
        self.url = ''
        self.detailMenuList = list()

class clsMenuUrls():
    def __init__(self):
        self.kind = ''
        self.name = ''
        self.subMenuList = list()

class clsProduct():
    def __init__(self):
        self.code = ''
        self.name = ''
        self.detailCode = ''
        self.night = ''
        self.period = ''
        self.url = ''
        self.detailInfoUrl = ''
        self.subcode = ''
    
    def toString(self):
        return 'code:'+self.code+',name:'+self.name+',detailcode:'+self.detailCode+',night:'+self.night+',period:'+self.period+',url:'+self.url

class clsProductDetail():
    def __init__(self):
        self.dDay = ''
        self.dTime = ''
        self.aDay = ''
        self.aTime = ''
        self.airCode = ''
        self.price = ''
        self.remainSeat = ''
        self.status = ''
        self.productName = ''
        self.url = ''
        self.productSeq = ''

def insertData(productCls, detailUrl, regionUrl, tourAgency, kind, dmst_div):
    print 'Product Url : ', productCls.url
    print >> exceptFile, 'Product Url : ', productCls.url
    detailProductHtml = savefilegethtml.getHtml(productCls.url, '', '', 'tour2000DetailHtml'+targetMonth+'.txt')
    
    codeList = codes.getCityCode(productCls.name.decode('utf-8'), detailUrl.name.decode('utf-8'), regionUrl.name.decode('utf-8'))
    cityList = codeList[0]
    nationList = codeList[1]
    continentList = codeList[2]
    
    # Master 상품 입력
    query = tourQuery.getMasterMergeQuery(tourAgency, productCls.code, productCls.name.decode('utf-8'), menu.kind, dmst_div, '', '')
    #print query
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    # Region Data 삭제
    codes.insertRegionData(tourAgency, productCls.code, cityList, nationList, continentList)
    
    pl10Idx = 0
    for detailProduct in detailProductHtml:
        try:
            if detailProduct.find('<span class="text_pink">') > -1 and detailProduct.find('<a href=') < 0:
                detailCls = clsProductDetail()
                numArray = tourUtil.getNumArray(detailProduct)
                if len(numArray) > 7:
                    detailCls.dDay = targetYear + numArray[0] + numArray[1]
                    detailCls.dTime = numArray[2] + numArray[3]
                    detailCls.aDay = targetYear + numArray[4] + numArray[5]
                    detailCls.aTime = numArray[6] + numArray[7]
                elif len(numArray) == 4:
                    detailCls.dDay = targetYear + numArray[0] + numArray[1]
                    detailCls.dTime = ''
                    detailCls.aDay = targetYear + numArray[2] + numArray[3]
                    detailCls.aTime = ''
            elif detailProduct.find('onError') > -1:
                detailCls.airCode = detailProduct[detailProduct.find('.gif') - 4:detailProduct.find('.gif') - 2]
            elif detailProduct.find('text_redB') > -1:
                numArray = tourUtil.getNumArray(tourUtil.getRemovedHtmlTag(detailProduct))
                for num in numArray:
                    detailCls.price += num
            elif detailProduct.find('</a></td>') > -1:
                if detailProduct.find('text_pink') > -1:
                    detailCls.status = codes.getStatus('tour2000', '예약가능')
                elif detailProduct.find('text_blau') > -1:
                    detailCls.status = codes.getStatus('tour2000', '출발가능')
                elif detailProduct.find('text_green') > -1:
                    detailCls.status = codes.getStatus('tour2000', '대기예약')
                elif detailProduct.find('text_grayLightSmall') > -1:
                    detailCls.status = codes.getStatus('tour2000', '예약마감')
                    
                detailCls.remainSeat = tourUtil.getRemovedHtmlTag(detailProduct).replace("'", "").strip()
            elif detailProduct.find('<p class="pl10">') > -1:
                if pl10Idx == 0:
                    pl10Idx = 1
                    detailCls.productName = tourUtil.getRemovedHtmlTag(detailProduct).replace("'", "").strip()
                    detailCls.url = mainUrl + tourUtil.getTagAttr(detailProduct, 'a', 'href')
                    detailCls.productSeq = detailProduct.split('ev_ym=')[1].split('&')[0] + detailProduct.split('ev_seq=')[1].split('&')[0]
                else:
                    pl10Idx = 0
                
                if detailCls.productName.find('부산출발') > -1:
                    departCity = 'PUS'
                else:
                    departCity = 'ICN'
                
                query = tourQuery.getDetailMergeQuery(tourAgency, productCls.code, detailCls.productSeq, detailCls.productName.decode('utf-8'), detailCls.dDay+detailCls.dTime, detailCls.aDay+detailCls.aTime, productCls.period, departCity, '', detailCls.airCode, detailCls.status, detailCls.url, detailCls.price, '0', '0', '0', '', productCls.night)
                #print >> exceptFile, query
                #print query
                cursor = con.cursor()
                cursor.execute(query)
                con.commit()
                #break
        except:
            print >> exceptFile, 'detail parcing Error : ', sys.exc_info()[0]
            pass


# 시간 변수들..
tourAgency = 'tour2000'
targetYear = sys.argv[1]
targetMonth = sys.argv[2]
#targetYear = '2014'
#targetMonth = '07'

scrappingStartTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

exceptFileName = 'tour2000Exception' + scrappingStartTime + '.txt'
exceptFile = open(exceptFileName, 'w')
print >> exceptFile, "Start : %s" % time.ctime()

mainUrl = 'http://www.tour2000.co.kr'

mainHtml = savefilegethtml.getHtml('http://www.tour2000.co.kr/index.asp', '<div class="navi_wholeMenu_box">', '<!-- navi_wholeMenu_wrapper// -->', 'tour2000mainHtml.txt')

startMainUrl = False
menuList = list()
MenuUrlCls = clsMenuUrls()
for each_line in mainHtml:
    if each_line.find('text_pinkB14') > -1:
        MenuUrlCls = clsMenuUrls()
        MenuUrlCls.kind = codes.getTourKind(tourAgency, tourUtil.getRemovedHtmlTag(each_line).strip())
        startMainUrl = True
    
    # 해외여행(패키지), 허니문, 골프, 국내(제주) 제외하고는 일단 패스
    if MenuUrlCls.kind == 'A' or MenuUrlCls.kind == 'F' or MenuUrlCls.kind == 'H' or MenuUrlCls.kind == 'No':
        continue    
    
    if startMainUrl and each_line.find('<li>') > -1:
        SubMenuCls = clsSubMenu()
        SubMenuCls.name = tourUtil.getRemovedHtmlTag(each_line).strip()
        SubMenuCls.url = mainUrl + tourUtil.getTagAttr(each_line, 'a', 'href')
        MenuUrlCls.subMenuList.append(SubMenuCls)
        
    if startMainUrl and each_line.find('</div>') > -1:
        startMainUrl = False
        menuList.append(MenuUrlCls)

# Url 수집..
for menu in menuList:
    try:
        # menu는 clsMenuUrls() 이다..
        print '@@@@@@@@@@@@@ (' + menu.kind + ') @@@@@@@@@@@@@@'
        for regionUrl in menu.subMenuList:
            # regionUrl clsSubMenu() 이다..
            print 'RegionUrl : ', regionUrl.name.strip().decode('utf-8') + ' => ' + regionUrl.url
            regionHtml = ''
            
            if regionUrl.url == 'http://www.tour2000.co.kr/domestic/domestic_Jeju.asp?cpCode=golfpkg':      # 국내 골프는 국내여행 메뉴에서 추가하자..
                continue
            
            if menu.kind ==  'D' and regionUrl.url != 'http://www.tour2000.co.kr/domestic/domestic_Jeju.asp?cpCode=real':         # 국내 여행은 요거 하나 URL로 모두 처리하자..
                continue
            
            if menu.kind == 'P':
                regionHtml = savefilegethtml.getHtml(regionUrl.url, 'class="con_left_pack">', '<div class="con_right">', 'tour2000regionhtml.txt')
            else:
                regionHtml = savefilegethtml.getHtml(regionUrl.url, 'class="con_left">', '</div><!-- con_left// -->', 'tour2000regionhtml.txt')
            
            menuOn = False
            menuOff = False
            chkJeju = False
            chkDomestic = False
            
            if menu.kind != 'D':
                for detailUrl in regionHtml:
                    if detailUrl.find('<li class="on">') > -1:
                        menuOn = True
                        menuOff = False
                        continue
                    elif detailUrl.find('<li class="off">') > -1:
                        menuOn = False
                        menuOff = True
                        continue
                    elif menuOn and detailUrl.find('<a href=') > -1 and detailUrl.find('class="sub_title"') < 0:
                        detailMenuCls = clsDetailMenu()
                        detailMenuCls.name = tourUtil.getRemovedHtmlTag(detailUrl).strip()
                        detailMenuCls.url = mainUrl + tourUtil.getTagAttr(detailUrl, 'a', 'href')
                        regionUrl.detailMenuList.append(detailMenuCls)
                        print 'Detail Url : ', detailMenuCls.url
            elif menu.kind == 'D':
                for detailUrl in regionHtml:
                    if detailUrl.find('제주여행') > -1:
                        chkJeju = True
                        chkDomestic = False
                        continue
                    elif detailUrl.find('내륙/테마여행') > -1:
                        chkJeju = False
                        chkDomestic = True
                        continue
                    elif (chkJeju or chkDomestic) and detailUrl.find('<a href=') > -1 and detailUrl.find('Goods_List.asp') > -1:
                        detailMenuCls = clsDetailMenu()
                        if chkJeju:
                            detailMenuCls.name = '제주'
                        elif chkDomestic:
                            detailMenuCls.name = '내륙'
                        detailMenuCls.url = mainUrl + tourUtil.getTagAttr(detailUrl, 'a', 'href')
                        regionUrl.detailMenuList.append(detailMenuCls)
                        #print 'Detail Url : ', detailMenuCls.url
            """
            <h3>에서 class 값을 이렇게 변경하면 됨
            해외  class="con_left_pack"
            자유  class="con_left_free"
            골프  class="con_left_golf"
            국내  class="con_left_domestic"            
            """
    except:
        #print 'URL Error : ', sys.exc_info()[0]
        print >> exceptFile, 'URL Error : ', sys.exc_info()[0]
        pass
# Url 수집완료
con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")        
dmst_div = ''
departCity = 'ICN'      # 부산출발... 등 출발 정보가 없다!!!!!!!
for menu in menuList:
    try:
        # menu는 clsMenuUrls() 이다..
        print '@@@@@@@@@@@@@ (' + menu.kind + ') @@@@@@@@@@@@@@'
        print >> exceptFile, '@@@@@@@@@@@@@@@@@@ (' + menu.kind + ') @@@@@@@@@@@@@@@@@@@'
        
        #if menu.kind != 'W':
            #continue
        if menu.kind == 'D':
            dmst_div = 'D'
        else:
            dmst_div = 'A'
        
        for regionUrl in menu.subMenuList:
            for detailUrl in regionUrl.detailMenuList:
                print detailUrl.name.decode('utf-8') + ' : ' + detailUrl.url
                print >> exceptFile, detailUrl.url
                try:
                    detailHtml = savefilegethtml.getHtml(detailUrl.url, 'overseas_list_menu', '<!-- con_right// -->', 'tour2000regionhtml.txt')
                    
                    if menu.kind == 'P':    
                        productCls = clsProduct()
                        codeChk = False
                        periodChk = False
                        for product in detailHtml:
                            try:
                                if product.find('class="overseas_list_box"') > -1:
                                    productCls = clsProduct()
                                    productCls.code = product.split('GOODS_')[1].split('"')[0]
                                elif product.find('<h4>') > -1:
                                    productCls.subcode = product.split('SUB_AREA_CD=')[1].split('"')[0]
                                    productCls.url = mainUrl + '/Overseas_Common/Ajax_AI_StartDayList.asp?sub_area_cd=' + productCls.subcode + '&goods_cd=' + productCls.code + '&get_month=' + targetYear + targetMonth
                                    productCls.name = tourUtil.getRemovedHtmlTag(product).replace("'", "").strip()
                                elif product.find('상품코드') > -1:
                                    codeChk = True
                                    periodChk = False
                                elif product.find('여행기간') > -1:
                                    codeChk = False
                                    periodChk = True
                                elif product.find('출발요일') > -1:
                                    codeChk = False
                                    periodChk = False
                                elif product.find('<dd>') > -1:
                                    if codeChk:
                                        productCls.detailCode = tourUtil.getRemovedHtmlTag(product).strip()
                                    elif periodChk:
                                        periodArray = tourUtil.getNumArray(product)
                                        
                                        if len(periodArray) > 0:
                                            productCls.night = periodArray[0]
                                        if len(periodArray) > 1:
                                            productCls.period = periodArray[1]
                                        
                                        #print >> exceptFile, "detail url : ", productCls.url
                                        insertData(productCls, detailUrl, regionUrl, tourAgency, menu.kind, dmst_div)
                                        
                                        #break   
                            except:
                               print >> exceptFile, 'detail parcing Error : ', sys.exc_info()[0]
                               pass 
                                
                    else:       # Package가 아닌경우
                        productCls = clsProduct()
                        for product in detailHtml:
                            if product.find('class="overseas_list_big"') > -1:
                                #print product
                                productCls = clsProduct()
                            elif product.find('<h5>') > -1:
                                #http://www.tour2000.co.kr/Overseas_common/overseas_goods.asp?goods_cd=24020141&SUB_AREA_CD=7001
                                #http://www.tour2000.co.kr/Overseas_Common/Ajax_AI_StartDayList.asp?goods_cd=24020141&get_month=201408
                                productCls.code = product.split('goods_cd=')[1].split('&')[0]
                                productCls.detailInfoUrl = mainUrl + tourUtil.getTagAttr(product, 'a', 'href')
                                productCls.url = mainUrl + '/Overseas_Common/Ajax_AI_StartDayList.asp?goods_cd=' + productCls.code + '&get_month=' + targetYear + targetMonth
                                productCls.name = tourUtil.getRemovedHtmlTag(product).replace("'", "").strip()
                            elif product.find('class="overseas_list_big_right"') > -1:
                                nightPeriodHtml = savefilegethtml.getHtml(productCls.detailInfoUrl, 'class="overseas_list_content"', '<!-- overseas_list_content// -->', 'tour2000nightPeriodHtml'+targetMonth+'.txt')
                                chkPeriod = False
                                for nightPeriod in nightPeriodHtml:
                                    if nightPeriod.find('여행기간') > -1:
                                        chkPeriod = True
                                    elif chkPeriod and nightPeriod.find('<dd>') > -1:
                                        periodArray = tourUtil.getNumArray(nightPeriod)
                                        if len(periodArray) > 0:
                                            productCls.night = periodArray[0]
                                        if len(periodArray) > 1:
                                            productCls.period = periodArray[1]
                                    
                                        #print >> exceptFile, productCls.toString()
                                        
                                        #print >> exceptFile, "detail url : ", productCls.url
                                        
                                insertData(productCls, detailUrl, regionUrl, tourAgency, menu.kind, dmst_div)
                                        
                                        #break        
                                
                except:
                    print >> exceptFile, 'detail url Error : ', sys.exc_info()[0]
                    pass
                
                #break
            #break
        #break
    except:
        print >> exceptFile, 'product url Error : ', sys.exc_info()[0]
        pass

con.close()
print >> exceptFile, "End : %s" % time.ctime()
exceptFile.close()