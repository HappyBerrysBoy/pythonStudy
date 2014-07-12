# -*- coding: utf-8 -*-
"""
Created on Wed Jul 09 01:53:58 2014

@author: KSC
"""

import cx_Oracle

masterTable = 't_prd'
detailTable = 't_prd_dtl'
masterTableTest = 't_prd_test2'
detailTableTest = 't_prd_dtl_test2'

def getOracleConnection():
    return cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")

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
def getMasterMergeQuery(tagn_id, prd_no, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md):
    query = "merge into " +  masterTable + " a using ("
    query += "select '" + tagn_id + "' tagn_id,'" + prd_no + "' prd_no,'" + prd_nm + "' prd_nm,'"
    query += tr_div + "' tr_div,'" + dmst_div + "' dmst_div,'" + prd_desc + "' prd_desc,'" + prd_desc_md + "' prd_desc_md from dual) b on (a.tagn_id = b.tagn_id and a.prd_no = b.prd_no) "
    query += "when matched then update set a.prd_nm= b.prd_nm, a.tr_div= b.tr_div, "
    query += "a.dmst_div= b.dmst_div, a.prd_desc= b.prd_desc, a.prd_desc_md= b.prd_desc_md, a.sel_dt = sysdate "
    query += "when not matched then insert (tagn_id, prd_no, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md, sel_dt) "
    query += "values ( b.tagn_id, b.prd_no, b.prd_nm, b.tr_div, b.dmst_div, b.prd_desc, b.prd_desc_md, sysdate)"
    return query
    
def delMasterRegionQuery(tagn_id, prd_no):
    query = "delete from ttr_tr_area where tagn_id ='" + tagn_id + "' and prd_no = '" + prd_no + "'"
    return query

   #Master 여행상품 조회 쿼리 Return
def crtMasterRegionQuery(tagn_id, prd_no, tr_area_seq, tr_cntt, tr_nt_cd, tr_city_cd):
    query = "insert into ttr_tr_area (tagn_id, prd_no, tr_area_seq, tr_cntt, tr_nt_cd, tr_city_cd) values ("
    query += "'" + tagn_id + "','" + prd_no + "','" + tr_area_seq + "','" + tr_cntt + "','" + tr_nt_cd + "','" + tr_city_cd + "')"
    return query
    
#Detail 여행상품 조회 쿼리 Return
def getDetailMergeQuery(tagn_id, prd_no, prd_seq, prd_dtl_nm, dep_dt, arr_dt, tr_term, dep_arpt, arr_arpt, arln_id, prd_st, prd_url, prd_fee_ad, prd_fee_ch, prd_fee_bb, cmps_seat, exg_div, term_bak=''):
    query = "merge into " +  detailTable + " a using ("
    query += "select '" + tagn_id + "' tagn_id, '" + prd_no + "' prd_no,'" + prd_seq + "' prd_seq,'" + prd_dtl_nm + "' prd_dtl_nm,'" + dep_dt + "' dep_dt,'" + arr_dt + "' arr_dt,'"
    query += tr_term + "' tr_term,'" + dep_arpt + "' dep_arpt,'" + arr_arpt + "' arr_arpt,'" + arln_id + "' arln_id,'" + prd_st + "' prd_st,'" + prd_url + "' prd_url," 
    query += prd_fee_ad + " prd_fee_ad," + prd_fee_ch + " prd_fee_ch," + prd_fee_bb + " prd_fee_bb," + cmps_seat + " cmps_seat,'" + exg_div + "' exg_div, nvl('" + term_bak + "', 0) TR_TERM_BAK from dual)" 
    query += " b on (a.tagn_id = b.tagn_id and a.prd_no = b.prd_no and a.prd_seq = b.prd_seq) "
    query += "when matched then update set a.PRD_DTL_NM =b.PRD_DTL_NM, a.DEP_DT = to_date(b.DEP_DT, 'yyyymmddhh24mi'), a.ARR_DT = to_date(b.ARR_DT, 'yyyymmddhh24mi'), "
    query += "a.TR_TERM =b.TR_TERM, a.DEP_ARPT =b.DEP_ARPT, a.ARR_ARPT =b.ARR_ARPT, a.ARLN_ID =b.ARLN_ID, a.PRD_ST =b.PRD_ST, a.PRD_URL =b.PRD_URL, a.PRD_FEE_AD =b.PRD_FEE_AD, "
    query += "a.PRD_FEE_CH =b.PRD_FEE_CH, a.PRD_FEE_BB =b.PRD_FEE_BB, a.CMPS_SEAT =b.CMPS_SEAT, a.EXG_DIV =b.EXG_DIV, a.SEL_DT =sysdate, a.TR_TERM_BAK = b.TR_TERM_BAK "
    query += "when not matched then insert (TAGN_ID, PRD_NO, PRD_SEQ, PRD_DTL_NM, DEP_DT, ARR_DT, TR_TERM, DEP_ARPT, ARR_ARPT, ARLN_ID, PRD_ST, PRD_URL, PRD_FEE_AD, PRD_FEE_CH, PRD_FEE_BB, CMPS_SEAT, EXG_DIV, SEL_DT, TR_TERM_BAK) "
    query += "values ( b.tagn_id , b.prd_no , b.PRD_SEQ , b.PRD_DTL_NM , to_date(b.DEP_DT, 'yyyymmddhh24mi') , to_date(b.ARR_DT, 'yyyymmddhh24mi') , b.TR_TERM , b.DEP_ARPT , b.ARR_ARPT , b.ARLN_ID ,"
    query += "b.PRD_ST , b.PRD_URL , b.PRD_FEE_AD , b.PRD_FEE_CH , b.PRD_FEE_BB , b.CMPS_SEAT , b.EXG_DIV , sysdate, b.TR_TERM_BAK )"
    return query

def getCode(codes):
    if len(codes) > 0:
        return codes.pop()
    else:
        return ''

   #Master 여행상품 조회 쿼리 Return
def getMasterMergeQueryTest1(tagn_id, prd_no, cntt_div, nt_cd, arr_city, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md, nations, cities):
    query = "merge into " +  masterTableTest + " a using ("
    query += "select '" + tagn_id + "' tagn_id,'" + prd_no + "' prd_no,'" + cntt_div + "' cntt_div,'" + nt_cd + "' nt_cd,'" + arr_city + "' arr_city,'" + prd_nm + "' prd_nm,'"
    query += tr_div + "' tr_div,'" + dmst_div + "' dmst_div,'" + prd_desc + "' prd_desc,'" + prd_desc_md + "' prd_desc_md,'"
    query += getCode(nations) + "' nt_cd1,'" + getCode(nations) + "' nt_cd2,'" + getCode(nations) + "' nt_cd3,'" + getCode(nations) + "' nt_cd4,'" + getCode(nations) + "' nt_cd5,'" + getCode(nations) + "' nt_cd6,'" + getCode(nations) + "' nt_cd7,'" + getCode(nations) + "' nt_cd8,'" + getCode(nations) + "' nt_cd9,'" + getCode(nations) + "' nt_cd10,'"
    query += getCode(cities) + "' arr_city1,'" + getCode(cities) + "' arr_city2,'" + getCode(cities) + "' arr_city3,'" + getCode(cities) + "' arr_city4,'" + getCode(cities) + "' arr_city5,'"
    query += getCode(cities) + "' arr_city6,'" + getCode(cities) + "' arr_city7,'" + getCode(cities) + "' arr_city8,'" + getCode(cities) + "' arr_city9,'" + getCode(cities) + "' arr_city10 "
    query += " from dual) b on (a.tagn_id = b.tagn_id and a.prd_no = b.prd_no) "
    query += "when matched then update set a.cntt_div= b.cntt_div, a.nt_cd= b.nt_cd, a.arr_city= b.arr_city, a.prd_nm= b.prd_nm, a.tr_div= b.tr_div, "
    query += "a.dmst_div= b.dmst_div, a.prd_desc= b.prd_desc, a.prd_desc_md= b.prd_desc_md, "
    query += "a.nt_cd1 = b.nt_cd1, a.nt_cd2 = b.nt_cd2, a.nt_cd3 = b.nt_cd3, a.nt_cd4 = b.nt_cd4, a.nt_cd5 = b.nt_cd5, "
    query += "a.nt_cd6 = b.nt_cd6, a.nt_cd7 = b.nt_cd7, a.nt_cd8 = b.nt_cd8, a.nt_cd9 = b.nt_cd9, a.nt_cd10 = b.nt_cd10, "
    query += "a.arr_city1 = b.arr_city1, a.arr_city2 = b.arr_city2, a.arr_city3 = b.arr_city3, a.arr_city4 = b.arr_city4, a.arr_city5 = b.arr_city5, "
    query += "a.arr_city6 = b.arr_city6, a.arr_city7 = b.arr_city7, a.arr_city8 = b.arr_city8, a.arr_city9 = b.arr_city9, a.arr_city10 = b.arr_city10, a.sel_dt = sysdate "
    query += "when not matched then insert (tagn_id, prd_no, cntt_div, nt_cd, arr_city, prd_nm, tr_div, dmst_div, prd_desc, prd_desc_md, "
    query += "nt_cd1, nt_cd2, nt_cd3, nt_cd4, nt_cd5, nt_cd6, nt_cd7, nt_cd8, nt_cd9, nt_cd10, "
    query += "arr_city1, arr_city2, arr_city3, arr_city4, arr_city5, arr_city6, arr_city7, arr_city8, arr_city9, arr_city10, sel_dt) "
    query += "values ( b.tagn_id, b.prd_no, b.cntt_div, b.nt_cd, b.arr_city, b.prd_nm, b.tr_div, b.dmst_div, b.prd_desc, b.prd_desc_md, "
    query += "b.nt_cd1, b.nt_cd2, b.nt_cd3, b.nt_cd4, b.nt_cd5, b.nt_cd6, b.nt_cd7, b.nt_cd8, b.nt_cd9, b.nt_cd10, "
    query += "b.arr_city1, b.arr_city2, b.arr_city3, b.arr_city4, b.arr_city5, b.arr_city6, b.arr_city7, b.arr_city8, b.arr_city9, b.arr_city10, sysdate)"
    return query
    
#Detail 여행상품 조회 쿼리 Return
def getDetailMergeQueryTest1(tagn_id, prd_no, prd_seq, prd_dtl_nm, dep_dt, arr_dt, tr_term, dep_arpt, arr_arpt, arln_id, prd_st, prd_url, prd_fee_ad, prd_fee_ch, prd_fee_bb, cmps_seat, exg_div, term_bak=''):
    query = "merge into " +  detailTableTest + " a using ("
    query += "select '" + tagn_id + "' tagn_id, '" + prd_no + "' prd_no,'" + prd_seq + "' prd_seq,'" + prd_dtl_nm + "' prd_dtl_nm,'" + dep_dt + "' dep_dt,'" + arr_dt + "' arr_dt,'"
    query += tr_term + "' tr_term,'" + dep_arpt + "' dep_arpt,'" + arr_arpt + "' arr_arpt,'" + arln_id + "' arln_id,'" + prd_st + "' prd_st,'" + prd_url + "' prd_url," 
    query += prd_fee_ad + " prd_fee_ad," + prd_fee_ch + " prd_fee_ch," + prd_fee_bb + " prd_fee_bb," + cmps_seat + " cmps_seat,'" + exg_div + "' exg_div, nvl('" + term_bak + "', 0) TR_TERM_BAK from dual)" 
    query += " b on (a.tagn_id = b.tagn_id and a.prd_no = b.prd_no and a.prd_seq = b.prd_seq) "
    query += "when matched then update set a.PRD_DTL_NM =b.PRD_DTL_NM, a.DEP_DT = to_date(b.DEP_DT, 'yyyymmddhh24mi'), a.ARR_DT = to_date(b.ARR_DT, 'yyyymmddhh24mi'), "
    query += "a.TR_TERM =b.TR_TERM, a.DEP_ARPT =b.DEP_ARPT, a.ARR_ARPT =b.ARR_ARPT, a.ARLN_ID =b.ARLN_ID, a.PRD_ST =b.PRD_ST, a.PRD_URL =b.PRD_URL, a.PRD_FEE_AD =b.PRD_FEE_AD, "
    query += "a.PRD_FEE_CH =b.PRD_FEE_CH, a.PRD_FEE_BB =b.PRD_FEE_BB, a.CMPS_SEAT =b.CMPS_SEAT, a.EXG_DIV =b.EXG_DIV, a.SEL_DT =sysdate, a.TR_TERM_BAK = b.TR_TERM_BAK "
    query += "when not matched then insert (TAGN_ID, PRD_NO, PRD_SEQ, PRD_DTL_NM, DEP_DT, ARR_DT, TR_TERM, DEP_ARPT, ARR_ARPT, ARLN_ID, PRD_ST, PRD_URL, PRD_FEE_AD, PRD_FEE_CH, PRD_FEE_BB, CMPS_SEAT, EXG_DIV, SEL_DT, TR_TERM_BAK) "
    query += "values ( b.tagn_id , b.prd_no , b.PRD_SEQ , b.PRD_DTL_NM , to_date(b.DEP_DT, 'yyyymmddhh24mi') , to_date(b.ARR_DT, 'yyyymmddhh24mi') , b.TR_TERM , b.DEP_ARPT , b.ARR_ARPT , b.ARLN_ID ,"
    query += "b.PRD_ST , b.PRD_URL , b.PRD_FEE_AD , b.PRD_FEE_CH , b.PRD_FEE_BB , b.CMPS_SEAT , b.EXG_DIV , sysdate, b.TR_TERM_BAK )"
    return query
