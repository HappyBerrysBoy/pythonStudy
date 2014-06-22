# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 21:16:18 2014

@author: KSC
"""

import os
import sys

def getTourScrapFile(name):
    if name == 'hanatour':
        return 'hanatourScrapper.py'
    elif name == 'modetour':
        return 'modetourScrapper.py'
    elif name == 'naeiltour':
        return 'naeiltourScrapper.py'
    elif name == 'onlinetour':
        return 'onlinetourScrapper.py'
    elif name == 'tour2000':
        return 'tour2000Scrapper.py'
    elif name == 'tourbaksa':
        return 'tourbaksaScrapper.py'
    elif name == 'verygoodtour':
        return 'verygoodtourScrapper.py'
    elif name == 'wemakeprice':
        return 'wemakepriceScrapper.py'
    elif name == 'ybtour':
        return 'ybtourScrapper.py'

tourCompany = sys.argv[1]
scrapYear = sys.argv[2]
scrapMonth = sys.argv[3]

e = os.system('python ' + getTourScrapFile(tourCompany) + ' ' + scrapYear + ' ' + scrapMonth)

if not e == 0:
  print >>sys.stderr, '실행 중 에러가 났습니다. 에러 코드:', e