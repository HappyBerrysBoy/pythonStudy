# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 02:29:14 2014

@author: KSC
"""

import urllib2
import savefilegethtml
import requests
import xmltodict
import datetime

"""
aa = 'http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=07&Pcode=EAP361&Pd=&Type=01'
detailUrl = requests.get(aa).text
tree = xmltodict.parse(detailUrl)
print tree['ModeSangPum']['STitle']
"""

toDate = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

exceptFileName = 'hanatourException' + toDate + '.txt'
print exceptFileName