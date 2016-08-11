#!/usr/bin/python
# -*- coding: UTF-8 -*-
#this file was created for test
import manipulateCsv
DB_NAME = "depends_graph.csv"
OUTPUT_DB_NAME = "未被依赖列表_0728.csv"
def removeDupList(depends_list):
	"""
	rlist : [,depends,predepends...]
	handle like this [,'a','b','c']  => ['a',...]
	"""
	rlist = []
	#package_name_list = ['a','b','c','d','e']
	package_name_list = manipulateCsv.selectPackageColumn(DB_NAME,"package_name")
	for elem in depends_list:
		if elem not in rlist and elem in package_name_list:
			rlist.append(elem)
	return rlist	
	
def wipeUnNecInfo(depends_list):
	"""
	rlist : [,depends,predepends]
	handle like this [,'a(>1.0)','b(2.0)','c | d(>0.1)'] => [,'a','b','c']
	"""
	rlist = []
	for elem in depends_list:
		tmp_list = []
		if elem.find('|') != -1:
			tmp_list = elem.split('|')
			for elem_child in tmp_list:
				rlist.append(elem_child.split('(')[0].strip())
		else:
			rlist.append(elem.split('(')[0].strip())
	return rlist
			
def parseDep2List(depends_list):
	"""
	rlist : [,depends,predepends,] 
	handle like this ['','a(>1.0),b(2.0)','c | d(>0.1)'] => ['a(>1.0)','b(2.0)','c | d(>0.1)']
	"""	
	rlist = []
	for elem in depends_list:
		if elem == '':
			continue
		elif elem.find(',') != -1:
			rlist.extend(elem.split(','))
		else:
			rlist.append(elem)
	return rlist

def writeList2File(package_list,file_name):
	"""
	if rcode : 0  write ok 
		      write failed
	"""
	with open(file_name,'wb') as f:
		for elem in package_list:
			f.write(elem + '\n')
	return 0 
			
def findNorDepPackages(package_list):
	"""
	rlist : [,depends,rdepends,] with 
	"""
	rlist = []
	depends_list = manipulateCsv.selectAllDepends(DB_NAME)
	final_depends_list = removeDupList(wipeUnNecInfo(parseDep2List(depends_list)))
	for elem in package_list:
		if elem == '':
			continue
		elif elem.strip() not in final_depends_list:
			rlist.append(elem)	
	return rlist 

def getNorDepPackages():
	"""
	rcode : 0  get depends correctly .
	"""
	all_package_list = manipulateCsv.selectPackageColumn(DB_NAME,"package_name")
	final_package_list = findNorDepPackages(all_package_list)
	all_package_info =  manipulateCsv.selectAllRows(DB_NAME)
	manipulateCsv.createDb(OUTPUT_DB_NAME)
	index = 0
	for elem,extra_info in all_package_info.items():
		package_version = extra_info[0]
		package_depends = extra_info[1]
		package_predepends = extra_info[2]
		package_description = extra_info[3]
		if elem == '':
			continue
		elif elem in final_package_list:
			index = index + 1
			data = [index,elem.strip(),package_version,package_depends,package_predepends,package_description]
			if manipulateCsv.insert2Db(OUTPUT_DB_NAME,data) == -1:
				pass #handle exception
	return 0
					

if __name__ == "__main__":
	print getNorDepPackages()	
