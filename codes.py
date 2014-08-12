# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 13:02:51 2014

@author: KSC
"""

import re
import sys
import cx_Oracle
import tourQuery

def getCodes(cityCode, nationCode, continentCode, cityNationCode, nationCnttCode):
    con = cx_Oracle.connect("bigtour/bigtour@221.167.94.198:1521/ora11g")
    
    query = 'select * from tmp_site'
    cursor = con.cursor()
    cursor.execute(query)
    for row in cursor:
        #print type(row[2])
        siteCityCode[row[2]] = row[1]
        siteCode[row[3].decode('cp949')] = row[2]
        #nationCode[row[5].decode('cp949')] = row[0]
        #nationCode[row[0]] = row[0]
    
    query = 'select * from tmp_city'
    cursor = con.cursor()
    cursor.execute(query)
    for row in cursor:
        #print type(row[2])
        cityNationCode[row[1]] = row[0]
        cityCode[row[2].decode('cp949')] = row[1]
        cityCode[row[1]] = row[1]
        #nationCode[row[5].decode('cp949')] = row[0]
        #nationCode[row[0]] = row[0]
        
    query = 'select * from tmp_nt'
    cursor = con.cursor()
    cursor.execute(query)
    for row in cursor:
        #print type(row[2])
        #cityNationCode[row[1]] = row[0]
        #cityCode[row[2].decode('cp949')] = row[1]
        #cityCode[row[1]] = row[1]
        nationCode[row[1].decode('cp949')] = row[0]
        nationCode[row[0]] = row[0]
        nationCnttCode[row[0]] = row[8]
        
    query = 'select * from tmp_cntt'
    cursor = con.cursor()
    cursor.execute(query)
    for row in cursor:
        #print type(row[2])
        #cityNationCode[row[1]] = row[0]
        #cityCode[row[2].decode('cp949')] = row[1]
        #cityCode[row[1]] = row[1]
        continentCode[row[1].decode('cp949')] = row[0]
        continentCode[row[0]] = row[0]
    con.close()

siteCode = dict()
cityCode = dict()
nationCode = dict()
continentCode = dict()
siteCityCode = dict()
cityNationCode = dict()
nationCnttCode = dict()

"""
'산토우':'SWA',
'SWA':'SWA',
nationCode
'일본':'JP'
'JP':'JP'
cityNationCode
"""
getCodes(cityCode, nationCode, continentCode, cityNationCode, nationCnttCode)

#print cityCode
#print nationCode
#print cityNationCode
#print nationCnttCode
#print continentCode

def getStatusCode(status):
    if status == 'DF':        # 출발확정
        return 'DF'
    elif status == 'RS':      # 예약가능
        return 'RS'
    elif status == 'WR':      #대기예약
        return 'WR'
    elif status == 'RF':      # 예약마감
        return 'RF'
    elif status == 'NO':    # 상태값 없음
        return 'NONE'

def getStatus(tour, status):
    if tour == 'hanatour':
        if status == '0':
            return getStatusCode('RF')
        elif status == '1':
            return getStatusCode('RS')
        elif status == '2':
            return getStatusCode('DF')
        else:
            return getStatusCode('NO')
    elif tour == 'modetour':
        if status == 'gray':
            return getStatusCode('RF')
        elif status == 'blue':
            return getStatusCode('RS')
        elif status == 'red':
            return getStatusCode('DF')
        elif status == 'green':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == 'ybtour':
        if status == '예약마감':
            return getStatusCode('RF')
        elif status == '예약가능':
            return getStatusCode('RS')
        elif status == '출발확정':
            return getStatusCode('DF')
        elif status == '예약대기':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == 'naeiltour':
        if status == '05':
            return getStatusCode('RF')
        elif status == '':
            return getStatusCode('RS')
        elif status == '03':
            return getStatusCode('DF')
        elif status == 'green':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == 'tourbaksa':
        if status == '예약마감':
            return getStatusCode('RF')
        elif status == '예약접수':
            return getStatusCode('RS')
        elif status == '바로예약':
            return getStatusCode('DF')
        elif status == '대기예약':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == 'verygoodtour':
        if status == '예약마감':
            return getStatusCode('RF')
        elif status == '예약하기':
            return getStatusCode('RS')
        elif status == '출발확정':
            return getStatusCode('DF')
        elif status == '대기예약':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == 'tour2000':
        if status == '예약마감':
            return getStatusCode('RF')
        elif status == '예약가능':
            return getStatusCode('RS')
        elif status == '출발가능':
            return getStatusCode('DF')
        elif status == '대기예약':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == 'onlinetour':
        if status == 'Finish':
            return getStatusCode('RF')
        elif status == 'Avail':
            return getStatusCode('RS')
        elif status == 'Confirm':
            return getStatusCode('DF')
        elif status == '대기예약':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == 'lottetour':
        if status == '01':
            return getStatusCode('RS')
        elif status == '03':
            return getStatusCode('RF')
        elif status == '04':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
    elif tour == '...':
        if status == 'gray':
            return getStatusCode('RF')
        elif status == 'blue':
            return getStatusCode('RS')
        elif status == 'red':
            return getStatusCode('DF')
        elif status == 'green':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
            
            
def getTourKindCode(kind):
    if kind == 'Package':
        return 'P'
    elif kind == 'Free':
        return 'F'
    elif kind == 'Honeymoon':
        return 'W'
    elif kind == 'Golf':
        return 'G'
    elif kind == 'Cruise':
        return 'C'
    elif kind == 'Domestic':
        return 'D'
    else:
        return 'No'
            
            
def getTourKind(tour, status):
    if tour == 'hanatour':
        if status == 'P':
            return getTourKindCode('Package')
        elif status == 'W':
            return getTourKindCode('Honeymoon')
        elif status == 'G':
            return getTourKindCode('Golf')
        elif status == 'C':
            return getTourKindCode('Cruise')
        elif status == 'D':
            return getTourKindCode('Domestic')
        else:
            return getTourKindCode('None')
            
    elif tour == 'modetour':
        if status == '패키지':
            return getTourKindCode('Package')
        elif status == '자유':
            return getTourKindCode('Free')
        elif status == '허니문':
            return getTourKindCode('Honeymoon')
        elif status == '골프':
            return getTourKindCode('Golf')
        elif status == '크루즈':
            return getTourKindCode('Cruise')
        elif status == 'JM':
            return getTourKindCode('Package')
        elif status == '부산·지방출발':
            return getTourKindCode('Package')
        else:
            return getTourKindCode('NO')
            
    elif tour == 'ybtour':
        if status == 'P':
            return getTourKindCode('Package')
        elif status == 'F':
            return getTourKindCode('Free')
        elif status == 'W':
            return getTourKindCode('Honeymoon')
        elif status == 'G':
            return getTourKindCode('Golf')
        elif status == 'D':
            return getTourKindCode('Domestic')
        elif status == 'PUS':
            return getTourKindCode('Package')
        elif status == 'C':
            return getTourKindCode('Cruise')
        else:
            return getTourKindCode('NO')
            """            
    elif tour == 'naeiltour':
        if status == '05':
            return getStatusCode('RF')
        elif status == '':
            return getStatusCode('RS')
        elif status == '03':
            return getStatusCode('DF')
        elif status == 'green':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')
            """
    elif tour == 'tourbaksa':
        if status == '키즈투어':
            return getTourKindCode('Package')
        elif status == '국내여행':
            return getTourKindCode('Domestic')
        elif status == '골프':
            return getTourKindCode('Golf')
        elif status == '크루즈':
            return getTourKindCode('Cruise')
        elif status == '해외패키지':
            return getTourKindCode('Package')
        elif status == '레저/스포츠':
            return getTourKindCode('Package')
        elif status == '해외자유':
            return getTourKindCode('Free')
        elif status == '허니문':
            return getTourKindCode('Honeymoon')
        else:
            return getTourKindCode('NO')
            
    elif tour == 'verygoodtour':
        if status == 'P':
            return getTourKindCode('Package')
        elif status == 'F':
            return getTourKindCode('Free')
        elif status == 'D':
            return getTourKindCode('Domestic')
        elif status == 'PUS':
            return getTourKindCode('Package')
        elif status == 'W':
            return getTourKindCode('Honeymoon')
        elif status == 'G':
            return getTourKindCode('Golf')
        elif status == 'Luxury':
            return getTourKindCode('Package')
        elif status == 'Air':
            return getTourKindCode('Air')
        elif status == 'Hotel':
            return getTourKindCode('Hotel')
        elif status == 'Company':
            return getTourKindCode('Company')
        else:
            return getTourKindCode('No')
            
    elif tour == 'tour2000':
        if status == '해외여행':
            return getTourKindCode('Package')
        elif status == '자유여행':
            return getTourKindCode('Free')
        elif status == '국내여행':
            return getTourKindCode('Domestic')
        elif status == '허니문':
            return getTourKindCode('Honeymoon')
        elif status == '골프':
            return getTourKindCode('Golf')
        elif status == '실시간 항공':
            return getTourKindCode('Air')
        elif status == '호텔':
            return getTourKindCode('Hotel')
        else:
            return getTourKindCode('No')
            
    elif tour == 'onlinetour':
        if status == '해외패키지':
            return getTourKindCode('Package')
        elif status == '해외자유배낭':
            return getTourKindCode('Free')
        elif status == '국내여행':
            return getTourKindCode('Domestic')
        elif status == '허니문':
            return getTourKindCode('Honeymoon')
        elif status == '골프':
            return getTourKindCode('Golf')
        elif status == '부산출발':
            return getTourKindCode('Package')
        elif status == '제주여행':
            return getTourKindCode('Domestic')
        else:
            return getTourKindCode('No')
            
    elif tour == 'lottetour':
        if status == 'package':
            return getTourKindCode('Package')
        elif status == 'fit':
            return getTourKindCode('Free')
        elif status == 'honeymoon _open':
            return getTourKindCode('Honeymoon')
        elif status == 'golf':
            return getTourKindCode('Golf')
        elif status == 'cruise line':
            return getTourKindCode('Cruise')
        else:
            return getTourKindCode('No')
            
    elif tour == '...':
        if status == 'gray':
            return getStatusCode('RF')
        elif status == 'blue':
            return getStatusCode('RS')
        elif status == 'red':
            return getStatusCode('DF')
        elif status == 'green':
            return getStatusCode('WR')
        else:
            return getStatusCode('NO')

def setNTCityCode(keys, cities, nations, continents, sites):
    global siteCode
    global cityCode
    global nationCode
    global continentCode
    global siteCityCode
    global cityNationCode
    global nationCnttCode
            
    for key in keys:
        try:
            #print 'nationkey : ', key.encode('cp549')
            #print key
            #if a == 'a':
                #print key
        
            if siteCode.has_key(key):
                sCode = siteCode[key]
                ctCode = siteCityCode[sCode]
                ntCode = cityNationCode[ctCode]
                cntCode = nationCnttCode[ntCode]
                sites.add(sCode)
                cities.add(ctCode)
                nations.add(ntCode)
                continents.add(cntCode)
                continue
            elif cityCode.has_key(key):
                ctCode = cityCode[key]
                ntCode = cityNationCode[ctCode]
                cntCode = nationCnttCode[ntCode]
                cities.add(ctCode)
                nations.add(ntCode)
                continents.add(cntCode)
                continue
            elif nationCode.has_key(key):
                ntCode = nationCode[key]
                nations.add(ntCode)
                continents.add(nationCnttCode[ntCode])
                continue
            elif continentCode.has_key(key):
                continents.add(continentCode[key])
                continue
                
            encodedKey = key.encode('utf-8')
            if siteCode.has_key(encodedKey):
                sCode = siteCode[encodedKey]
                ctCode = siteCityCode[sCode]
                ntCode = cityNationCode[ctCode]
                cntCode = nationCnttCode[ntCode]
                sites.add(sCode)
                cities.add(ctCode)
                nations.add(ntCode)
                continents.add(cntCode)
                continue
            elif cityCode.has_key(encodedKey):
                ctCode = cityCode[encodedKey]
                ntCode = cityNationCode[ctCode]
                cntCode = nationCnttCode[ntCode]
                cities.add(ctCode)
                nations.add(ntCode)
                continents.add(cntCode)
                continue
            elif nationCode.has_key(encodedKey):
                ntCode = nationCode[encodedKey]
                nations.add(ntCode)
                continents.add(nationCnttCode[ntCode])
                continue
            elif continentCode.has_key(encodedKey):
                continents.add(continentCode[encodedKey])
                continue
            """
            cp949Encoded = key.encode('cp949')
            if cityCode.has_key(cp949Encoded):
                cCode = cityCode[cp949Encoded]
                cities.add(cCode)
                nations.add(cityNationCode[cCode])
                continents.add(nationCnttCode[cityNationCode[cCode]])
                continue
            elif nationCode.has_key(cp949Encoded):
                cCode = nationCode[cp949Encoded]
                nations.add(cCode)
                continents.add(nationCnttCode[cCode])
                continue
            elif continentCode.has_key(cp949Encoded):
                continents.add(continentCode[cp949Encoded])
                continue
            """
        except:
            print 'Key : ', key
            print 'Codes Error', sys.exc_info()[0]
            pass


def delOverlapRegion(cities, nations, continents, sites):
    global siteCityCode
    global cityNationCode
    global nationCnttCode
    
    for site in sites:
        try:
            ct = siteCityCode[site]
            cities.remove(ct)
        except:
            pass
    
    for site in sites:
        try:
            ct = siteCityCode[site]
            nt = cityNationCode[ct]
            nations.remove(nt)
        except:
            pass
    
    for site in sites:
        try:
            ct = siteCityCode[site]
            nt = cityNationCode[ct]
            cntt = nationCnttCode[nt]
            continents.remove(cntt)
        except:
            pass
    
    #print '==============='
    for city in cities:
        try:
            nt = cityNationCode[city]
            nations.remove(nt)
        except:
            pass
    #print '==============='    
    for city in cities:
        try:
            nt = cityNationCode[city]
            cntt = nationCnttCode[nt]
            continents.remove(cntt)
        except:
            pass
    #print '==============='    
    for nation in nations:
        try:
            continents.remove(nationCnttCode[nation])
        except:
            pass
        
def parceCode(content):
    keys = ''
    
    if type(content).__name__ == 'str':
        try:
            if len(content) == len(re.findall(u'[a-zA-Z0-9]', content.decode('cp949'))):
                keys = re.findall(u'[a-zA-Z0-9]+', content.decode('cp949'))
            else:
                keys = re.findall(u'[\uac00-\ud7a3]+', content.decode('cp949'))
        except:
            if len(content) == len(re.findall(u'[a-zA-Z0-9]', content.decode('utf-8'))):
                keys = re.findall(u'[a-zA-Z0-9]+', content.decode('utf-8'))
            else:
                keys = re.findall(u'[\uac00-\ud7a3]+', content.decode('utf-8'))
    else:
        keys = re.findall(u'[\uac00-\ud7a3]+', content)
        
    return keys

def getCityCode(productname, city='', comment='', nation=''):
    sites = set()
    cities = set()
    nations = set()
    continents = set()
    
    productnameKeys = parceCode(productname)
    cityKeys = parceCode(city)
    commentKeys = parceCode(comment)
    nationKeys = parceCode(nation)
    """
    if type(productname).__name__ == 'str':
        try:
            productnameKeys = re.findall(u'[\uac00-\ud7a3]+', productname.decode('cp949'))
        except:
            productnameKeys = re.findall(u'[\uac00-\ud7a3]+', productname.decode('utf-8'))
    else:
        productnameKeys = re.findall(u'[\uac00-\ud7a3]+', productname)
        
    if type(city).__name__ == 'str':
        try:
            if len(city) == len(re.findall(u'[a-zA-Z0-9]', city.decode('cp949'))):
                cityKeys = re.findall(u'[a-zA-Z0-9]+', city.decode('cp949'))
            else:
                cityKeys = re.findall(u'[\uac00-\ud7a3]+', city.decode('cp949'))
        except:
            if len(city) == len(re.findall(u'[a-zA-Z0-9]', city.decode('utf-8'))):
                cityKeys = re.findall(u'[a-zA-Z0-9]+', city.decode('utf-8'))
            else:
                cityKeys = re.findall(u'[\uac00-\ud7a3]+', city.decode('utf-8'))
    else:
        cityKeys = re.findall(u'[\uac00-\ud7a3]+', city)
       
    if type(comment).__name__ == 'str':
        try:
            commentKeys = re.findall(u'[\uac00-\ud7a3]+', comment.decode('cp949'))
        except:
            commentKeys = re.findall(u'[\uac00-\ud7a3]+', comment.decode('utf-8'))
    else:
        commentKeys = re.findall(u'[\uac00-\ud7a3]+', comment)
    
    if type(nation).__name__ == 'str':
        try:
            if len(nation) == len(re.findall(u'[a-zA-Z0-9]', nation.decode('cp949'))):
                nationKeys = re.findall(u'[a-zA-Z0-9]+', nation.decode('cp949'))
            else:
                nationKeys = re.findall(u'[\uac00-\ud7a3]+', nation.decode('cp949'))
        except:
            if len(nation) == len(re.findall(u'[a-zA-Z0-9]', nation.decode('utf-8'))):
                nationKeys = re.findall(u'[a-zA-Z0-9]+', nation.decode('utf-8'))
            else:
                nationKeys = re.findall(u'[\uac00-\ud7a3]+', nation.decode('utf-8'))
    else:
        nationKeys = re.findall(u'[\uac00-\ud7a3]+', nation)
        
    """    
    #print productnameKeys
    #print cityKeys
    #print commentKeys
    #print nationKeys
    
    setNTCityCode(productnameKeys, cities, nations, continents, sites)
    setNTCityCode(cityKeys, cities, nations, continents, sites)
    setNTCityCode(commentKeys, cities, nations, continents, sites)
    setNTCityCode(nationKeys, cities, nations, continents, sites)

    #print '==============='
    #print cities
    #print nations
    #print continents

    delOverlapRegion(cities, nations, continents, sites)
    
    #print '******************'
    #print cities
    #print nations
    #print continents

    #print cities
    #print nations
    #print continents
    
    nationCity = list()
    nationCity.append(cities)
    nationCity.append(nations)
    nationCity.append(continents)    
    nationCity.append(sites)
    return nationCity


def insertRegionData(agency, prd_no, cityList, nationList, continentList, siteList):
    global siteCode
    global cityCode
    global nationCode
    global continentCode
    global siteCityCode
    global cityNationCode
    global nationCnttCode
    
    con = tourQuery.getOracleConnection()
    query = tourQuery.delMasterRegionQuery(agency, prd_no)
    #print query
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    # Region Insert
    
    regionSeq = 0
    
    for site in siteList:
        try:
            ct = siteCityCode[site]
            nt = cityNationCode[ct]
            cntt = nationCnttCode[nt]
            query = tourQuery.crtMasterRegionQuery(agency, prd_no, str(regionSeq), cntt, nt, ct, site)
            #print query
            cursor = con.cursor()
            cursor.execute(query)
            regionSeq += 1
        except:
            pass
    
    for city in cityList:
        try:
            nt = cityNationCode[city]
            cntt = nationCnttCode[nt]
            query = tourQuery.crtMasterRegionQuery(agency, prd_no, str(regionSeq), cntt, nt, city, '')
            #print query
            cursor = con.cursor()
            cursor.execute(query)
            regionSeq += 1
        except:
            pass
        
    for nation in nationList:
        try:
            cntt = nationCnttCode[nation]
            query = tourQuery.crtMasterRegionQuery(agency, prd_no, str(regionSeq), cntt, nation, '', '')
            cursor = con.cursor()
            cursor.execute(query)
            regionSeq += 1
        except:
            pass
        
    for continent in continentList:
        try:
            query = tourQuery.crtMasterRegionQuery(agency, prd_no, str(regionSeq), continent, '', '', '')
            cursor = con.cursor()
            cursor.execute(query)
            regionSeq += 1
        except:
            pass
        
    con.commit()
    con.close()