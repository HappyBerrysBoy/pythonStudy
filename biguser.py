# -*- coding: utf-8 -*-
"""
Created on Fri Jun 06 10:26:20 2014

@author: KSC
"""

import requests
import xmltodict

class clsRegionUrlGroup():
    def __init__(self):
        self.region = ''
        self.url = ''

class clsTourKindGroup():
    def __init__(self):
        self.tourkind = ''
        self.regionUrlGroup = list()        
        
class clsTotalGroup():
    def __init__(self):
        self.departCity = ''
        self.tourkindgroup = list()
        
aa = clsTotalGroup()
bb = clsTourKindGroup()
cc = clsRegionUrlGroup()
dd = clsRegionUrlGroup()

bb.regionUrlGroup.append(dd)
bb.regionUrlGroup.append(cc)
print bb.regionUrlGroup.count(cc)