# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 16:00:07 2014

@author: user
"""

import os
import urllib2

def getHtml(url, startParcer, endParcer, filename):
    returnHtml = urllib2.urlopen(url).read()
    if startParcer != '' and endParcer != '':
        returnHtml = returnHtml[returnHtml.find(startParcer):returnHtml.find(endParcer)]
    returnHtmlFile = open(filename, 'w')
    print >> returnHtmlFile, returnHtml
    returnHtmlFile.close()

    returnValue = list()
    returnHtml = open(filename)
    for each_line in returnHtml:
        returnValue.append(each_line)
        
    returnHtml.close()
    
    os.remove(filename)
    return returnValue
