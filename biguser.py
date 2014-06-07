# -*- coding: utf-8 -*-
"""
Created on Fri Jun 06 10:26:20 2014

@author: KSC
"""

import requests
import xmltodict


detailUrl = requests.get('http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=06&Pcode=ATA202&Pd=&Type=01&term=201406071238%5E201506070000').text
tree = xmltodict.parse(detailUrl)
for t in tree['ModeSangPum']['SangList']:
    print(t['SName']['#text'])
    print(t['SAirCode'])
    print(t['SPriceDay']['#text'])
    print(t['SArrivalDay']['#text'])
    print(t['SDay'])
    print(t['SPrice'])
    print(t['SDetailState']['#text'])