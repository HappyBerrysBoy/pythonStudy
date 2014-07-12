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
    con = cx_Oracle.connect("bigtour/bigtour@hnctech73.iptime.org:1521/ora11g")
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

cityCode = dict()
nationCode = dict()
continentCode = dict()
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

def setNTCityCode(keys, cities, nations, continents):
    for key in keys:
        try:
            #print 'nationkey : ', key.encode('cp549')
            #print key
            #if a == 'a':
                #print key
            encodedKey = key.encode('utf-8')
            if cityCode.has_key(key):
                cCode = cityCode[key]
                cities.add(cCode)
                nations.add(cityNationCode[cCode])
                continents.add(nationCnttCode[cityNationCode[cCode]])
            elif nationCode.has_key(key):
                cCode = nationCode[key]
                nations.add(cCode)
                continents.add(nationCnttCode[cCode])
            elif continentCode.has_key(key):
                cCode = continentCode[key]
                continents.add(cCode)
            elif cityCode.has_key(encodedKey):
                cCode = cityCode[encodedKey]
                cities.add(cCode)
                nations.add(cityNationCode[cCode])
                continents.add(nationCnttCode[cityNationCode[cCode]])
            elif nationCode.has_key(encodedKey):
                cCode = nationCode[encodedKey]
                nations.add(cCode)
                continents.add(nationCnttCode[cCode])
            elif continentCode.has_key(encodedKey):
                continents.add(continentCode[encodedKey])
        except:
            print 'Key : ', key
            print 'Codes Error', sys.exc_info()[0]
            pass


def delOverlapRegion(cities, nations, continents):
    
    #print '==============='
    for city in cities:
        try:
            nt = cityNationCode[city]
            #print city + ':' + nt
            nations.remove(nt)
            #print cities
            #print nations
            #print continents
        except:
            pass
    #print '==============='    
    for city in cities:
        try:
            nt = cityNationCode[city]
            cntt = nationCnttCode[nt]
            #print city + ':' + nt
            #print nt + ':' + cntt
            continents.remove(cntt)
            #print cities
            #print nations
            #print continents
        except:
            pass
    #print '==============='    
    for nation in nations:
        try:
            #print nation + ':' + nationCnttCode[nation]
            continents.remove(nationCnttCode[nation])
            #print cities
            #print nations
            #print continents
        except:
            pass

def getCityCode(productname, city='', comment='', nation=''):
    cities = set()
    nations = set()
    continents = set()
    
    productnameKeys = ''
    cityKeys = ''
    commentKeys = ''
    nationKeys = ''
    
    if type(productname).__name__ == 'str':
        productnameKeys = re.findall(u'[\uac00-\ud7a3]+', productname.decode('cp949'))
    else:
        productnameKeys = re.findall(u'[\uac00-\ud7a3]+', productname)
        
    if type(city).__name__ == 'str':
        if len(city) == len(re.findall(u'[a-zA-Z0-9]', city.decode('cp949'))):
            cityKeys = re.findall(u'[a-zA-Z0-9]+', city.decode('cp949'))
        else:
            cityKeys = re.findall(u'[\uac00-\ud7a3]+', city.decode('cp949'))
    else:
        cityKeys = re.findall(u'[\uac00-\ud7a3]+', city)
       
    if type(comment).__name__ == 'str':
        commentKeys = re.findall(u'[\uac00-\ud7a3]+', comment.decode('cp949'))
    else:
        commentKeys = re.findall(u'[\uac00-\ud7a3]+', comment)
    
    if type(nation).__name__ == 'str':
        if len(nation) == len(re.findall(u'[a-zA-Z0-9]', nation.decode('cp949'))):
            nationKeys = re.findall(u'[a-zA-Z0-9]+', nation.decode('cp949'))
        else:
            nationKeys = re.findall(u'[\uac00-\ud7a3]+', nation.decode('cp949'))
    else:
        nationKeys = re.findall(u'[\uac00-\ud7a3]+', nation)
        
    setNTCityCode(productnameKeys, cities, nations, continents)
    setNTCityCode(cityKeys, cities, nations, continents)
    setNTCityCode(commentKeys, cities, nations, continents)
    setNTCityCode(nationKeys, cities, nations, continents)

    #print '==============='
    #print cities
    #print nations
    #print continents

    delOverlapRegion(cities, nations, continents)
    
    #print cities
    #print nations
    #print continents
    #print '******************'

    #print cities
    #print nations
    #print continents
    
    nationCity = list()
    nationCity.append(cities)
    nationCity.append(nations)
    nationCity.append(continents)    
    return nationCity


def insertRegionData(agency, prd_no, cityList, nationList, continentList):
    con = tourQuery.getOracleConnection()
    query = tourQuery.delMasterRegionQuery(agency, prd_no)
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    # Region Insert
    
    regionSeq = 0
    for city in cityList:
        try:
            nt = cityNationCode[city]
            cntt = nationCnttCode[nt]
            query = tourQuery.crtMasterRegionQuery(agency, prd_no, str(regionSeq), cntt, nt, city)
            cursor = con.cursor()
            cursor.execute(query)
            regionSeq += 1
        except:
            pass
        
    for nation in nationList:
        try:
            cntt = nationCnttCode[nation]
            query = tourQuery.crtMasterRegionQuery(agency, prd_no, str(regionSeq), cntt, nation, '')
            cursor = con.cursor()
            cursor.execute(query)
            regionSeq += 1
        except:
            pass
        
    for continent in continentList:
        try:
            query = tourQuery.crtMasterRegionQuery(agency, prd_no, str(regionSeq), continent, '', '')
            cursor = con.cursor()
            cursor.execute(query)
            regionSeq += 1
        except:
            pass
        
    con.commit()
    con.close()