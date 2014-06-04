# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 00:08:33 2014

@author: KSC
"""

import requests

mainpage = requests.get("http://www.modetour.com/").text

overseas = mainpage[mainpage.find('<div class="overseas">'):mainpage.find('<div class="domestic">')]
domestics = mainpage[mainpage.find('<div class="domestic">'):mainpage.find('<div class="total_categories">')]

overseasFile = open('overseas.txt', 'w')
domesticsFile = open('domestics.txt', 'w')

print >> overseasFile, overseas
print >> domesticsFile, domestics

overseasFile.close()
domesticsFile.close()
#print(overseas)
#print('=========================================================================================================================================')
#print(domestics)

openOverseas = open('overseas.txt')
openDomestics = open('domestics.txt')

#전체 List 말고 대표 메뉴만 가도 다 나오는듯...
overseasMainUrls = list()
overseasMainUrlsFile = open('mainUrls.txt', 'w')
for each_line in openOverseas:
    if each_line.strip()[:3] == '<li':
        if each_line.find('subMain') > -1 and each_line.find('span') > -1:
        #print(each_line.strip())
            submain = subMain()
            result = submain.getParam(each_line)
            #submain.printToString()
            #print(submain.makeURL())
            print >> overseasMainUrlsFile, submain.makeURL()
            overseasMainUrls.append(submain.makeURL())
        """elif each_line.find('List') > -1:
            sublist = subList()
            result = sublist.getParam(each_line)
            #sublist.printToString()
            #print(sublist.makeURL())
            print >> mainUrls, sublist.makeURL()
            overseasMainUrls.append(submain.makeURL())"""
overseasMainUrlsFile.close()

menuDistrict = overseasMainUrls.pop()
menuPremium = overseasMainUrls.pop()
menuCruise = overseasMainUrls.pop()
menuGolf = overseasMainUrls.pop()
menuHoney = overseasMainUrls.pop()
menuFree= overseasMainUrls.pop()
menuPackage = overseasMainUrls.pop()

packageResponse = requests.get(menuPackage).text
packageResponse = packageResponse[packageResponse.find('<div class="submain">'):packageResponse.find('<div class="total_categories">')]
menuPackageFile = open('packageUrls.txt', 'w')
print >> menuPackageFile, packageResponse
menuPackageFile.close()
#print(packageResponse)

subUrls = open('modePackageUrls.txt', 'w')
openPackageFile = open('packageurls.txt')
for each_line in openPackageFile:
    if each_line.strip()[:3] == '<dt' or each_line.strip()[:3] == '<dd':
        #print(each_line)
        sublist = subList()
        result = sublist.getParam(each_line)
        #print(sublist.makeURL())
        #print >> subUrls, each_line
        print >> subUrls, sublist.makeURL()

subUrls.close()

aa = requests.get("http://www.modetour.com/Xml/Package/Get_Pcode.aspx?Ct=&Month=06&Pcode=ASP502&Pd=&Type=01&term=201406052222%5E201506042359")
print(aa.text)


#classes..
class subMain():
    def __init__(self):
        self.thing = 0
    
    def getParam(self, line):
        #dicts = dict()
        self.startLocation = line[line.find('startLocation=') + len('startLocation='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        #print(line)
        self.id = line[line.find('id=') + len('id='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        #print(line)
        self.type = line[line.find('type=') + len('type='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        #print(line)
        self.MLoc = line[line.find('MLoc=') + len('MLoc='):line.find(' ') - 1]
        return self
    
    def printToString(self):
        print('SubMain ==> startlocation:' + self.startLocation + ', id:' + self.id + ', type:' + self.type + ', Mloc:' + self.MLoc)
        
    def makeURL(self):
        return 'http://www.modetour.com/Package/subMain2.aspx?startLocation=' + self.startLocation + '&id=' + self.id + '&type=' + self.type + '&MLoc=' + self.MLoc

class subList():
    def __init__(self):
        self.thing = 0
    
    def getParam(self, line):
        self.startLocation = line[line.find('startLocation=') + len('startLocation='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        self.location = line[line.find('location=') + len('location='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        self.location1 = line[line.find('location1=') + len('location1='):line.find('amp;') - 1]
        line = line[line.find('amp;') + len('amp;'):]
        if line.find('Theme=') > -1:
            self.Theme = line[line.find('Theme=') + len('Theme='):line.find('amp;') - 1]
            line = line[line.find('amp;') + len('amp;'):]
        else:
            self.Theme = ''

        if line.find('Theme1=') > -1:
            self.Theme1 = line[line.find('Theme1=') + len('Theme1='):line.find('amp;') - 1]
            line = line[line.find('amp;') + len('amp;'):]
        else:
            self.Theme1 = ''
        self.MLoc = line[line.find('MLoc=') + len('MLoc='):line.find(' ') - 1]
        return self
    
    def printToString(self):
        print('SubList ==> startlocation:' + self.startLocation + ', location:' + self.location + ', location1:' + self.location1 + ', Theme:' + self.Theme + ', Theme1:' + self.Theme1 + ', Mloc:' + self.MLoc)
        
    def makeURL(self):
        return 'http://www.modetour.com/Package/List.aspx?startLocation=' + self.startLocation + '&location=' + self.location + '&location1=' + self.location1 + '&Theme=' + self.Theme + '&Theme1=' + self.Theme1 + '&MLoc=' + self.MLoc

