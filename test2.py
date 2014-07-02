# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

@author: KSC
"""

import re
import codes
import sys

print sys.getdefaultencoding()

text = '[다국가여행]싱가폴/방콕/파타야/홍콩 상품'
print type(text)

text2 = '이시카키/미야코지마'
print type(text2)

cc = re.findall('[가-힣]+', text2)
print len(cc)

for c in cc:
    print unicode(c, 'utf-8')


#cp_str = "안녕하세요"
#uni_str = unicode(cp_str, 'cp949') # cp949 방식을 사용하는 "안녕하세요"라는 문자를 유니코드로 변경
#print uni_str.encode('utf8') # 유니코드 "안녕하세요"를 UTF-8로 변경



#text = u'가☆나★다◎라◈마┃바'
#text = 'abcd1234가나다라'
#text = '[동아시아정복1탄]대만/홍콩5일'
#result = re.split('[\ \]\[\)\(\/\+\-\&\!\@\#\$\%\^\*\~\"\}\{\|\>\<\0-9\a-Z]', text)
#result = re.findall(u'[\uac00-\ud7a3]+', text)

#for aa in result:
    #print aa
"""





ll = codes.getCityCode(text)
l1 = ll[0]
l2 = ll[1]
print '========================'

for l11 in l1:
    print l11
    
print '========================'

for l22 in l2:
    print l22
  
"""  
"""
successidx = 0
failidx = 0    
f = open('exp_test.txt')
ff = open('exp_test_result.txt', 'w')
for line in f:
    print >> ff, 'Line : ' + line
    ll = codes.getCityCode(line.encode('utf-8'))
    if len(ll[0]) == 0 and len(ll[1]) == 0:
        print >> ff, 'fail : ' + line
        failidx += 1
    else:
        cities = ''
        nations = ''
        for nation in ll[0]:
            nations += nation + ', '
        for city in ll[1]:
            cities += city + ', '
        
        print >> ff, 'succ : ' + nations + " // " + cities

ff.close()
f.close()
"""