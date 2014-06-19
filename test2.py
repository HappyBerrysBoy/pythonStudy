# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 00:48:02 2014

@author: KSC
"""




class clsMenuUrls():
    def __init__(self, p_mode, p_url):
        self.url = p_url
        self.mode = p_mode
        
cls = clsMenuUrls('a', 'b')
print cls.url
print cls.mode