# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 12:54:12 2014

@author: KSC
"""
import requests 

requests.Timeout(2)
mainpage = requests.get('http://www.modetour.com/').text