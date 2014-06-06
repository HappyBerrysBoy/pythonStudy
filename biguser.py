# -*- coding: utf-8 -*-
"""
Created on Fri Jun 06 10:26:20 2014

@author: KSC
"""

import requests
from xml import parsers
import xml.etree.ElementTree as ET
import xmltodict

tmpUrl = 'http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=07&Pcode=ACP201&Pd=&Type=01&term=201406061800%5E201506060000'
tree = xmltodict.parse(requests.get(tmpUrl).text)
print(len(tree['ModeSangPum']['SangList']))
for t in tree['ModeSangPum']['SangList']:
    print(t['SName']['#text'])
    print(t['SNight'])
    print(t['SDay'])
    print(t['SPrice'])
    print(t['SAirCode'])
    print(t['SAirName'])
    print(t['SPriceDay']['#text'])
    print(t['SArrivalDay']['#text'])
    print(t['SPriceNum']['#text'])
    print(t['SMeet'])
    print(t['SstartAir'])
    print(t['SstartTime'])
    print(t['SDetailState']['#text'])
    print('=======================================================')
    