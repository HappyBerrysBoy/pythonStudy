# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 20:38:23 2014

@author: KSC
"""

import urllib2
import time, datetime
from time import localtime, strftime, sleep
from datetime import timedelta
import sys
import cx_Oracle

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



class clsCountryUrl:
    def __init__(self):
        self.country = ''
        self.url = ''

#저작권... ㄷㄷㄷ
#homepage html을 가져오고 파일로 저장..
homepageUrl = 'http://www.onlinetour.co.kr/web/home'
homepageHtml = urllib2.urlopen(homepageUrl).read()
homepageHtmlFile = open('onlinetourHomepageHtml.txt', 'w')
print >> homepageHtmlFile, homepageHtml
homepageHtmlFile.close()

### 패키지별, 지역별 URL 가져오기..
flag = False
urlClasses = list() # clsCountryUrl 들의 List
homepageHtml = open('onlinetourHomepageHtml.txt')
for each_line in homepageHtml:
    #print each_line
    if each_line.find('<li id="n_pack">') > -1:
        flag = True
    
    if flag:
        if each_line.find('<li>') > -1 and each_line.find('전체') < 0:
            countryCls = clsCountryUrl()
            countryCls.country = each_line.split('>')[2].split('<')[0]
            countryCls.url = each_line.split('"')[1]
            urlClasses.append(countryCls)
    
    if flag and each_line.find('<li id="n_travel">') > -1:
        break
homepageHtml.close()
### 패키지별, 지역별 URL 가져오기... 끝!
for urlCls in urlClasses:
    print 'name:' + urlCls.country + ', url:' + urlCls.url









