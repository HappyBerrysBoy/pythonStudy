# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 16:00:07 2014

@author: user
"""

import urllib2

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
    
#Master 여행상품 조회 쿼리 Return
def getMasterTourInfo(tagn_id, prd_no, cntt_div, nt_cd, arr_city, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md):
    query = "insert into t_prd values ('" + tagn_id + "','" + prd_no + "','" + cntt_div + "','" + nt_cd + "','" + arr_city + "','" + prd_nm
    query += "','" + tr_div + "','" + dmst_div + "','" + prd_desc + "','" + prd_desc_md + "')"
    return query
    
#Detail 여행상품 조회 쿼리 Return
def getDetailTourInfo(tagn_id, prd_no, prd_seq, prd_dtl_nm, dep_dt, arr_dt, tr_term, dep_arpt, arr_arpt, arln_id, prd_st, prd_url, prd_fee_ad, prd_fee_ch, prd_fee_bb, cmps_seat, exg_div):
    query = "insert into t_prd_dtl values ('" + tagn_id + "','" + prd_no + "','" + prd_seq + "','" + prd_dtl_nm + "',to_date('" + dep_dt + "', 'yyyymmddhh24mi'),to_date('" + arr_dt + "', 'yyyymmddhh24mi'),'"
    query += tr_term + "','" + dep_arpt + "','" + arr_arpt + "','" + arln_id + "','" + prd_st + "','" + prd_url + "'," + prd_fee_ad + "," + prd_fee_ch + "," + prd_fee_bb + "," + cmps_seat + ",'" + exg_div + "',sysdate)"
    return query
    
    
    