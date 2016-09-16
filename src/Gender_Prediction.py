
# Import Libraries

import os
import re
import urllib2
from zipfile import ZipFile
import csv
import cPickle as pickle

def downloadNames():
    u = urllib2.urlopen('https://www.ssa.gov/oact/babynames/names.zip')
    localFile = open('names.zip', 'w')
    localFile.write(u.read())
    localFile.close()

def getNameList():
    if not os.path.exists('names.pickle'):
        print 'names.pickle does not exist, generating'
        
        # https://www.ssa.gov/oact/babynames/names.zip
        
        if not os.path.exists('names.zip'):
            print 'names.zip does not exist, downloading from github'
            downloadNames()
        else:
            print 'names.zip exists, not downloading'
        
        print 'Extracting names from names.zip'  
        
        namesDict=extractNamesDict()
        
        maleNames=list()
        femaleNames=list()
        
        print 'Sorting Names'
        
        for name in namesDict:
            counts=namesDict[name]
            tuple=(name,counts[0],counts[1])
            if counts[0]>counts[1]:
                maleNames.append(tuple)
            elif counts[1]>counts[0]:
                femaleNames.append(tuple)
        
        names=(maleNames,femaleNames)
        
        print 'Saving names.pickle'
        fw=open('names.pickle','wb')
        pickle.dump(names,fw,-1)
        fw.close()
        print 'Saved names.pickle'
    else:
        print 'names.pickle exists, loading data'
        f=open('names.pickle','rb')
        names=pickle.load(f)
        print 'names.pickle loaded'
        
    print '%d male names loaded, %d female names loaded'%(len(names[0]),len(names[1]))
    
    return names[0],names[1]

def extractNamesDict():
    zf=ZipFile('names.zip', 'r')
    filenames=zf.namelist()
    
    names=dict()
    genderMap={'M':0,'F':1}
    
    for filename in filenames:
        fp = zf.open(filename,'rU')
        rows=csv.reader(fp, delimiter=',', dialect=csv.excel_tab)
        try:
            for row in rows:
            #print name,row[1]
                try:
                    name=row[0].upper()
                    gender=genderMap[row[1]]
                    count=int(row[2])

                    if not names.has_key(name):
                        names[name]=[0,0]

                    names[name][gender]=names[name][gender]+count
                except:
                    pass
        except:
            pass
            
        fp.close()
        
        print '\tImported %s'%filename
    return names


def find_gender_from_first_name(name):
    if name.upper() in new_male_list:
        return "Male"
    elif name.upper() in new_female_list:
        return "Female"
    else:
        return "Unknown"    

if __name__ == '__main__':
    
	male_names, female_names = getNameList()
	new_male_list = []
	new_female_list = []

	for index,name in enumerate(male_names):
		try:
		    if (name[1]/name[2])>=4:
		        new_male_list.append(name[0])
		except:
		    new_male_list.append(name[0])
		    
	#print "Total number of Male Names after is %d." %len(new_male_list)	
	
	
	for index,name in enumerate(female_names):
		try:
		    if (name[2]/name[1])>=4:
		        new_female_list.append(name[0])
		except:
		    new_female_list.append(name[0])
		    
	#print "Total number of Female Names after is %d." %len(new_female_list)
	
	#find_gender_from_first_name('Harsh')
	
