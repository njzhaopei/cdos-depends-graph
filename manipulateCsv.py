#!/usr/bin/python
import csv
import sys
from collections import defaultdict
# -*- coding: UTF-8 -*-
FIELD_NAMES = ['id','package_name','version','depends','predepends','description']
def createDb(db_name):
	"""
	rcode: 0 means create successfully;
	      -1 means create unsuccessfully.
	"""
	with open(db_name, 'wb') as csvfile:
    		filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    		filewriter.writerow(FIELD_NAMES)
		csvfile.close()
	return 0
	
def insert2Db(db_name,data):
	"""
	rcode: 0 means create successfully;
	       -1 means create unsuccessfully.
	"""
	with open(db_name, 'ab+') as csvfile:
    		filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    		filewriter.writerow(data)
		csvfile.close()
	return 0
	
def selectAllRows(db_name):
	"""
        rdict: {package_name:[version,depends,pre-depends,description]}
        if select rows error , raise exception .
        """
	rdict = {}
	with open(db_name,"rb") as f:
		reader = csv.reader(f)
		num = 0
                for line in reader:
                        if num != 0:
                                rdict[line[1]] = [line[2],line[3],line[4],line[5]]
                        else:
                                num = num + 1
        f.close()
        return rdict
	

def selectRows(db_name):
	"""
	rdict: {package_name:[depends,pre-depends]}
	if select rows error , raise exception .
	"""
	rdict = {}
	with open(db_name,"rb") as f:
		reader = csv.reader(f)		
		num = 0
		for line in reader:
			if num != 0:	
				rdict[line[1]] = [line[3],line[4]] 
			else:
				num = num + 1
	f.close()
	return rdict		

def selectPackageColumn(db_name,column_name):
	"""
	rlist: [,package_name...]
	if select package column error , raise exception . 
	"""
	columns = defaultdict(list)
	with open(db_name,"rb") as f:
                reader = csv.DictReader(f)
		for row in reader: #read a row as {column1: value1 , column2: value2 ...}
			for (k,v) in row.items():
				columns[k].append(v)
	return columns['package_name']

def selectAllDepends(db_name):
	"""
	rlist: [,depends,rdepends...]
	when encountering a error , it will raise a exception .
	"""
	columns = defaultdict(list)
	with open(db_name,"rb") as f:
		reader = csv.DictReader(f)
		for row in reader:
			for(k,v) in row.items():
				columns[k].append(v)
	return columns['depends'] + columns['predepends']
"""
test api
if __name__ == '__main__':
	DB_NAME = "depends_graph.csv"
	#test createDb()
	rcode = createDb(DB_NAME)
	if rcode == -1:
		pass
	else:
		print "create db successfully"
	#test insert2Db()
	data = ['1','xserver-xorg-input-vmmouse','1:13.0.0-1build1','libc6 (>= 2.7), xorg-input-abi-20, xserver-xorg-core (>= 2:1.14.99.902), xserver-xorg-input-mouse, udev',' ','X.Org X server -- VMMouse input driver to use with VMWare']
	#data = ['0','a','0.01','b','des']
	rcode = insert2Db(DB_NAME,data)
	if rcode == -1:
		pass
	else:
		print "insert2Db successfully"
	#test selectRows()
	rDict = selectRows(DB_NAME,)
	print rDict
	#test selectPackageColumn()
	rList = selectPackageColumn(DB_NAME,'package_name')
	print rList
	print selectAllDepends('depends_graph1.csv')
"""
