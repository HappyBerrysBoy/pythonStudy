# -*- coding: utf-8 -*-
"""
Created on Fri Jun 06 10:26:20 2014

@author: KSC
"""

import requests

r = requests.post('http://hnctech73.iptime.org:9000/berthJson?atb=&vvd_status=&atd=201406060600&cct=&etb=&etd=&in_vvd_opr=&opr=&out_vvd_opr=&route=&terminal_id=&vsl_name=&vvd=')
print(r.text)