#!/usr/bin/python 
import subprocess
def insertInfo2Def(deb_path , deb_name):
	"""
	insert deb info and its depends info into def 
	example:
	A {'depends:'[depends] , 'predepends':[pre_depends]}
	=> insert depends info to def
	"""
	
def parseDebInfo(deb_path,deb_name):
	"""
	use external command `dpkg -I *.deb` to output the deb infomation ;
	rList = [depends,...] + [pr_depends,...] 
	rcode: 0 parses deb info correctly ; 1 parses deb info uncorrectly .  
	"""
	output = subprocess.check_output(['dpkg','-I',deb_path + '/' + deb_name])	
	"""
	handle output string to rlist
	"""
	return rlist
	
	
def addDeb2Def(deb_path , deb_name):
	if 0 == parseDebInfo(deb_path , deb_name):	
		insertInfo2Def(deb_path , deb_name)
	else -1 == parseDebInfo(deb_path , deb_name):
		print "parse Deb Info uncorrectly" 
		pass
		
def delDeb2Def(deb_name , deb_version):
	"""
	rcode: 0 represents del deb corrctly , -1 represents del deb uncorrectly 
	"""
	
#test 
if __name__ == '__main__':
	print "version definiton test ..."
	"""
	addDeb2Def(deb_path , deb_name)
	"""
	deb_path = "/home/zippo"
	deb_name = ['XX.deb','.deb','.txt']
	if 1 == addDeb2Def(deb_path , deb_name):
		print "test case1: pass"
	if 0 == addDeb2Def(deb_path , deb_name):
		print "test case2: pass"
	if -1 == addDeb2Def(deb_path , deb_name):
		print "test case3: pass"
	
	print "delDeb2Def(deb_path ,deb_name)"
	if 0 == delDeb2Def(deb_name , deb_version)
		print "test case4: pass"
	if -1 == delDeb2Def(deb_name , deb_version)
		print "test case5: pass"
