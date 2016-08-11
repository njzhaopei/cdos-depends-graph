#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb as db
HOST = "localhost"
def initPackageDb(user,passwd,db_name):
	con = db.connect(HOST,user,passwd) 	
	cursor = con.cursor()
	sql = 'CREATE DATABASE IF NOT EXISTS ' + db_name
	cursor.execute(sql)
	con.close()

def createTb(user,passwd,db_name):
	con = db.connect(HOST,user,passwd,db_name)
	cursor = con.cursor()
	create_tb_sql = "CREATE TABLE IF NOT EXISTS system_package_info (\
			id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,\
			package_name VARCHAR(256) NOT NULL,\
			version VARCHAR(128) NOT NULL,\
			depends TEXT(2048),\
			predepends Text(2048) ,\
			description Text\
	)"	
	cursor.execute(create_tb_sql)
	con.close()

def insert2Db(user,passwd,db_name,data):
	#package_id = data[0]，package_name = data[1], version = data[2],depends = data[3] , predepends = data[4]
	con = db.connect(HOST,user,passwd,db_name)
	with con:
		cursor = con.cursor()
		if data[1] != "":
			print "insert info to db ..."
			try:
				insert_db_sql = "INSERT INTO system_package_info(id,package_name,version,depends,predepends,description) VALUES(" + "\"" + data[0] + "\"," + "\"" + data[1] + "\"," + "\"" +  data[2] + "\"," + "\"" + data[3] + "\"," + "\"" + data[4] + "\"," + "\"" + data[5] + "\")" 
				print insert_db_sql
				cursor.execute(insert_db_sql)
			except ValueError:
                		print "VAlUE ERROR:" + key

def selectRows(user,passwd,db_name,package_name,filter_value):
	
	rdict = {}
	select_sql = "select package_name,depends,predepends from system_package_info"
	con = db.connect(HOST,user,passwd,db_name)
	with con:
		cur = con.cursor()
		if filter_value == True:
			cur.execute(select_sql + " where package_name=\""  + package_name + "\"")
		else:
			cur.execute(select_sql)
		rows = cur.fetchall()
		for rows in rows:
			rdict[rows[0]] = [rows[1],rows[2]] 
				
		print "======================"
	return rdict

def selectPackageColumn(user,passwd,db_name):
	rList = []
        select_sql = "select package_name from system_package_info"
        con = db.connect(HOST,user,passwd,db_name)
        with con:
                cur = con.cursor()
                cur.execute(select_sql)
                rows = cur.fetchall()
                for rows in rows:
                        rList.append(rows[0])
        return rList


"""
if __name__ == '__main__':
	print "initPackageDb..."
	#initPackageDb("root","mint","package_info")
	print "createTb..."
	#createTb("root","mint","package_info")
	#test_data1 、 test_data2 [id,package_name,version,depends,predepends,description]
	print "insert data to table ..."
	#data = [1,"xserver-xorg-input-vmmouse","1:13.0.0-1build1","libc6 (>= 2.7), xorg-input-abi-20, xserver-xorg-core (>= 2:1.14.99.902), xserver-xorg-input-mouse, udev","multiarch-support","Support library to use the MBIM protocol\
 libmbim is a glib-based library for talking to WWAN modems and devices\
 which speak the Mobile Interface Broadband Model (MBIM) protocol."]
	insert2Db("root","mint","package_info", data)
"""
