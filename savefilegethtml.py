# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 16:00:07 2014

@author: user
"""

import urllib2
import os

#urlopen에서 부터 list로 return까지 모두다 처리하는 함수
def getHtml(url, startParcer, endParcer, filename, replaceFirst='', replaceSecond=''):
    returnHtml = urllib2.urlopen(url).read()
    
    if startParcer != '' and endParcer != '':
        returnHtml = returnHtml[returnHtml.find(startParcer):returnHtml.find(endParcer)]
    elif startParcer != '' and endParcer == '':
        returnHtml = returnHtml[returnHtml.find(startParcer):]
    elif startParcer == '' and endParcer != '':
        returnHtml = returnHtml[:returnHtml.find(endParcer)]
        
    if replaceFirst != '' and replaceSecond != '':
        returnHtml.replace(replaceFirst, replaceSecond)

    return htmlToList(returnHtml, filename)
    
#html 최초 내용을 그대로 받아서 list형태로 return 하는 함수
def getHtmlList(html, startParcer, endParcer, filename, replaceFirst='', replaceSecond=''):
    if startParcer != '' and endParcer != '':
        html = html[html.find(startParcer):html.find(endParcer)]
    if replaceFirst != '' and replaceSecond != '':
        html.replace(replaceFirst, replaceSecond)

    return htmlToList(html, filename)

#urlopen으로 가져온 데이터로 부터 list로 return하는 함수
def htmlToList(html, filename):
    saveFile(filename, html)
    return openFile(filename)

#파일로 저장하는 함수
def saveFile(filename, content):
    fileopen = open(filename, 'w')
    print >> fileopen, content
    fileopen.close()

#저장된 파일을 가져오고 list로 반환하는 함수
def openFile(filename):
    returnList = list()
    content = open(filename)
    for each_line in content:
        returnList.append(each_line)
        
    content.close()
    #os.remove(filename)
    return returnList
    
def chkExistFile(filename):
    if os.path.isfile(filename):
        return filename + 'tmp'
    else:
        return filename
    
