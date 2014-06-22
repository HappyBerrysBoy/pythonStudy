# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 16:00:07 2014

@author: user
"""

import urllib2
import os

masterTable = 't_prd'
detailTable = 't_prd_dtl'

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
    
#Master 여행상품 조회 쿼리 Return
def getMasterInsertQuery(tagn_id, prd_no, cntt_div, nt_cd, arr_city, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md):
    query = "insert into " +  masterTable + " values ('" + tagn_id + "','" + prd_no + "','" + cntt_div + "','" + nt_cd + "','" + arr_city + "','" + prd_nm
    query += "','" + tr_div + "','" + dmst_div + "','" + prd_desc + "','" + prd_desc_md + "')"
    return query
    
#Detail 여행상품 조회 쿼리 Return
def getDetailInsertQuery(tagn_id, prd_no, prd_seq, prd_dtl_nm, dep_dt, arr_dt, tr_term, dep_arpt, arr_arpt, arln_id, prd_st, prd_url, prd_fee_ad, prd_fee_ch, prd_fee_bb, cmps_seat, exg_div):
    query = "insert into " +  detailTable + " values ('" + tagn_id + "','" + prd_no + "','" + prd_seq + "','" + prd_dtl_nm + "',to_date('" + dep_dt + "', 'yyyymmddhh24mi'),to_date('" + arr_dt + "', 'yyyymmddhh24mi'),'"
    query += tr_term + "','" + dep_arpt + "','" + arr_arpt + "','" + arln_id + "','" + prd_st + "','" + prd_url + "'," + prd_fee_ad + "," + prd_fee_ch + "," + prd_fee_bb + "," + cmps_seat + ",'" + exg_div + "',sysdate)"
    return query
    
   #Master 여행상품 조회 쿼리 Return
def getMasterMergeQuery(tagn_id, prd_no, cntt_div, nt_cd, arr_city, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md):
    query = "merge into " +  masterTable + " a using ("
    query += "select '" + tagn_id + "' tagn_id,'" + prd_no + "' prd_no,'" + cntt_div + "' cntt_div,'" + nt_cd + "' nt_cd,'" + arr_city + "' arr_city,'" + prd_nm + "' prd_nm,'"
    query += tr_div + "' tr_div,'" + dmst_div + "' dmst_div,'" + prd_desc + "' prd_desc,'" + prd_desc_md + "' prd_desc_md from dual) b on (a.tagn_id = b.tagn_id and a.prd_no = b.prd_no) "
    query += "when matched then update set a.cntt_div= b.cntt_div, a.nt_cd= b.nt_cd, a.arr_city= b.arr_city, a.prd_nm= b.prd_nm, a.tr_div= b.tr_div, "
    query += "a.dmst_div= b.dmst_div, a.prd_desc= b.prd_desc, a.prd_desc_md= b.prd_desc_md "
    query += "when not matched then insert (tagn_id, prd_no, cntt_div, nt_cd, arr_city, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md) "
    query += "values ( b.tagn_id, b.prd_no, b.cntt_div, b.nt_cd, b.arr_city, b.prd_nm, b.tr_div, b.dmst_div, b.prd_desc, b.prd_desc_md)"
    return query
    
#Detail 여행상품 조회 쿼리 Return
def getDetailMergeQuery(tagn_id, prd_no, prd_seq, prd_dtl_nm, dep_dt, arr_dt, tr_term, dep_arpt, arr_arpt, arln_id, prd_st, prd_url, prd_fee_ad, prd_fee_ch, prd_fee_bb, cmps_seat, exg_div):
    query = "merge into " +  detailTable + " a using ("
    query += "select '" + tagn_id + "' tagn_id, '" + prd_no + "' prd_no,'" + prd_seq + "' prd_seq,'" + prd_dtl_nm + "' prd_dtl_nm,'" + dep_dt + "' dep_dt,'" + arr_dt + "' arr_dt,'"
    query += tr_term + "' tr_term,'" + dep_arpt + "' dep_arpt,'" + arr_arpt + "' arr_arpt,'" + arln_id + "' arln_id,'" + prd_st + "' prd_st,'" + prd_url + "' prd_url," 
    query += prd_fee_ad + " prd_fee_ad," + prd_fee_ch + " prd_fee_ch," + prd_fee_bb + " prd_fee_bb," + cmps_seat + " cmps_seat,'" + exg_div + "' exg_div from dual)" 
    query += " b on (a.tagn_id = b.tagn_id and a.prd_no = b.prd_no and a.prd_seq = b.prd_seq) "
    query += "when matched then update set a.PRD_DTL_NM =b.PRD_DTL_NM, a.DEP_DT = to_date(b.DEP_DT, 'yyyymmddhh24mi'), a.ARR_DT = to_date(b.ARR_DT, 'yyyymmddhh24mi'), "
    query += "a.TR_TERM =b.TR_TERM, a.DEP_ARPT =b.DEP_ARPT, a.ARR_ARPT =b.ARR_ARPT, a.ARLN_ID =b.ARLN_ID, a.PRD_ST =b.PRD_ST, a.PRD_URL =b.PRD_URL, a.PRD_FEE_AD =b.PRD_FEE_AD, "
    query += "a.PRD_FEE_CH =b.PRD_FEE_CH, a.PRD_FEE_BB =b.PRD_FEE_BB, a.CMPS_SEAT =b.CMPS_SEAT, a.EXG_DIV =b.EXG_DIV, a.SEL_DT =sysdate "
    query += "when not matched then insert (TAGN_ID, PRD_NO, PRD_SEQ, PRD_DTL_NM, DEP_DT, ARR_DT, TR_TERM, DEP_ARPT, ARR_ARPT, ARLN_ID, PRD_ST, PRD_URL, PRD_FEE_AD, PRD_FEE_CH, PRD_FEE_BB, CMPS_SEAT, EXG_DIV, SEL_DT) "
    query += "values ( b.tagn_id , b.prd_no , b.PRD_SEQ , b.PRD_DTL_NM , to_date(b.DEP_DT, 'yyyymmddhh24mi') , to_date(b.ARR_DT, 'yyyymmddhh24mi') , b.TR_TERM , b.DEP_ARPT , b.ARR_ARPT , b.ARLN_ID ,"
    query += "b.PRD_ST , b.PRD_URL , b.PRD_FEE_AD , b.PRD_FEE_CH , b.PRD_FEE_BB , b.CMPS_SEAT , b.EXG_DIV , sysdate )"
    return query
