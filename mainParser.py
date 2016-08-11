#!/usr/bin/python 
#filename: depParser
import manipulateCsv
import sys,getopt
import os
import subprocess
DB_NAME_FILE = "depends_graph.csv"
STATUS_FILE = "/var/lib/dpkg/status"
MNT_PATH_ISO = "/tmp/iso"
MNT_PATH_FS = "/tmp/squashfs"
def parseFile2Csv(status_file_name):
	"""
	id_num : auto_increment
	package_name : package 
	version : Version 
	depends : Depends
	pre-depends : Pre-depends
	description : Description
	=> rList : [id_num,package_name,version,depends,pre-depends,description]
	"""
	fd = open(status_file_name)
	all_status_info = fd.read().split('\n')
	id_num = 0
	data = ['','','','','','']	
	for elem in all_status_info: 
		if elem == '':	
			if '' == data[1]:
				continue
			id_num = id_num + 1 
			data[0] = str(id_num)
			if 0 != manipulateCsv.insert2Db(DB_NAME_FILE,data):
				return -1
			data = ['','','','','','']
		if elem.find("Package: ") == 0:
			data[1] = elem.split(' ')[1]
			continue
		if elem.find("Version: ") == 0:
			data[2] = elem.split(' ')[1]
			continue
		if elem.find("Depends: ") == 0:
			data[3] = elem.split("Depends:")[1]
			continue
		if elem.find("Pre-Depends: ") == 0:
			data[4] = elem.split("Pre-Depends: ")[1]
			continue
		if elem.find("Description: ") == 0:
               		data[5] = elem.split("Description: ")[1].replace("\""," ")
			continue
	return 0

def  checkValidPath(path_file):
	if os.path.exists(path_file):
	#the file is there 
		return 0
	elif os.access(os.path.dirname(path_file), os.W_OK):
	#the file does not exists but write priviledge are given
		return 1
	else:
	#can not write there
		return -1

def deconstruct():
	"""
	rcode: -1 represents executing command failed ; 
		0 represents executing command ok .
	"""
	try:
        	subprocess.check_output(['umount', MNT_PATH_FS])  
		subprocess.check_output(['umount', MNT_PATH_ISO])
	except:
		return -1 
	return 0
	return 0

def parseIso2Csv(iso_name):
	"""
	rcode: 0 represent ok 
	       -11 represent failed 
	"""	
	if not os.geteuid() == 0:
		sys.exit("\nOnly root can run this script\n")
	#create directory
	if not os.path.exists(MNT_PATH_ISO):
    		os.makedirs(MNT_PATH_ISO)
	if not os.path.exists(MNT_PATH_FS):
		os.makedirs(MNT_PATH_FS)	
	try:
        	subprocess.check_output(['mount', '-o', 'loop', iso_name, MNT_PATH_ISO])
        	subprocess.check_output(['mount', MNT_PATH_ISO + '/casper/' + 'filesystem.squashfs', MNT_PATH_FS])
	except:
		return -1
	if -1 != parseFile2Csv(MNT_PATH_FS + STATUS_FILE):
		return 0
	else:
		return -1
	
if __name__ == "__main__":
	manipulateCsv.createDb(DB_NAME_FILE)
	#parseFile2Csv(STATUS_FILE)
	if len(sys.argv) == 1: 
		FILE_NAME = "/var/lib/dpkg/status"
		parseFile2Csv(FILE_NAME)
	elif len(sys.argv) == 2:
		ISO_NAME = sys.argv[1]
		if -1 == checkValidPath(sys.argv[1]) or 1 == checkValidPath(sys.argv[1]):
			print "file is not exist or the path do not have write priviledge . Please check ..."
			sys.exit(1)
		if -1 != parseIso2Csv(ISO_NAME):
			deconstruct()
	else:
		print "usage: python mainParser/py [optional:iso]"
		sys.exit(1)
	sys.exit(1)
