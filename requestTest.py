# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

@author: KSC
"""

import requests

r = requests.get("http://www.modetour.com/").text

print(r)


