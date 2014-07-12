# -*- coding: utf-8 -*-
"""
Created on Sun Jul 06 00:24:08 2014

@author: KSC
"""

import re
import tourQuery

def getRemovedHtmlTag(html):
    return re.sub('<(/)?([a-zA-Z0-9]*)(\\s[a-zA-Z0-9]*=[^>]*)?(\\s)*(/)?>', ' ', html)

def getNumArray(html):
    return re.findall('[\^0-9]+', html)
    
def getNumArrayUnicode(html):
    return re.findall(u'[\^0-9]+', html)
    
    
"""
aa = '<td class="pro_date">07/28 (월) 09:10<br/><span>08/17 (<span style="color:red;margin-bottom:0;">일</span>) 05:50</span></td>'
aa = '<td class="pro_date">07/07 (월) <br/><span></span></td>'
aa = '<td class="pro_date">07/07 (월) 16:15<br/><span>07/09 (수) 21:05</span></td>'
print aa
bb = getRemovedHtmlTag(aa)
print bb
cc = re.findall('[\^0-9]+', bb)
print cc
"""