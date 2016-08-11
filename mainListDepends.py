#!/usr/bin/python
# -*- coding: UTF-8 -*-
import graphviz as gv
import functools
import sys,getopt
import manipulateCsv
import graphCreate
import graphStore
DB_NAME = "depends_graph.csv"

def get_all_nodes(node_list):
	"""
	node_list : ['a','e'] =>
	rdict : {'a':['b','c','d'],'e':{'f','g','h'}}
	"""
	node_dict = {}
	for elem in node_list:
		all_depends_dict = manipulateCsv.selectRows(DB_NAME)
		# concatenate string 'depends' and string 'pre-depends'
		all_depends = all_depends_dict[elem.strip()][0] + ',' +  all_depends_dict[elem.strip()][1]
		node_dict[elem] = [x.strip() for x in all_depends.split(',')]
	return node_dict

def get_all_rnodes(node_list):
	"""
        node_list: ['a']  => 
        rlist: [...{a:[b,c,d]}]
        """
	node_dict = {}
	rdependsDict = manipulateCsv.selectRows(DB_NAME)
	for elem in node_list:
		rlist = []
        	for key,value in rdependsDict.items():
                	rpkg_list = []
                	pkg_list = value[0] + ',' + value[1]
                	for x in pkg_list.split(','):
                        	if x.find('(') != -1:
                                	rpkg_list.append(x.split('(')[0].strip())
                        	elif x == "":
                                	continue
                        	else:
                                	rpkg_list.append(x.strip())
                	if elem in rpkg_list:
                        	rlist.append(key)
		node_dict[elem] = rlist
	return node_dict
	
def handleDepends(depends_list):
	"""
	depends_list[['a(>0.1)','b(>0.2)'],['c(>2.0.0)']] 
	rlist : ['a','b']
	handle like this : [['a(>0.1)','b(>0.2)'],['c(>2.0.0)']]  => ['a','b','c']
	"""
	rlist = []
	all_depends_list = []
	for i in range(len(depends_list)):
		all_depends_list.extend(depends_list[i])
	for elem in all_depends_list:
		if '' == elem:
			continue
		elif elem.find('(') != -1:
			rlist.append(elem.split('(')[0])
		else:
			rlist.append(elem)
	return rlist

def isEmptyNodeList(node_list):
	"""
	node_list : ['a','b']
	rcode : -1 represents node _list is not empty , 0 represents node_list is empty . 
	"""
	handled_node_list = handleDepends(node_list)
	for elem in handled_node_list:
		if elem != '':
			return -1
	return 0	
	
def getDependsNodes(depends_list):
	#print "getDependsNode"
	rlist = []
	mixture_list = []
	for elem in depends_list:
		print elem
		mixture_list.extend(elem)	
	print mixture_list
	for elem in mixture_list:
		if elem not in rlist:
			rlist.append(elem)
	#print "rlist",rlist
	return rlist	
		

def getDependsEdges(depends_list):
	#print "getDependsedge"	
	rdict = {}
	rlist = []
	mixture_list = []
	for elem in depends_list:
	#	rdict =  dict(tmp_dict,**elem)
		rdict = dict(rdict.items() + elem.items())
	for key,values in rdict.items():
		if key == '':
			continue
		else:
			for elem in values:	
				if elem == '':
					continue
				elif elem.find('(') != -1:
					rlist.append((key,elem.split('(')[0]))
				else:
					rlist.append((key,elem))
	return rlist

def getRdependsEdges(depends_list):
        #print "getRdependsedge"
        rdict = {}
        rlist = []
        mixture_list = []
        for elem in depends_list:
        #       rdict =  dict(tmp_dict,**elem)
                rdict = dict(rdict.items() + elem.items())
        for key,values in rdict.items():
                if key == '':
                        continue
                else:
                        for elem in values:
                                if elem == '':
                                        continue
                                elif elem.find('(') != -1:
                                        rlist.append((elem.split('(')[0],key))
                                else:
                                        rlist.append((elem,key))
        return rlist

def getDepends(package_name,depth):
	"""
	#rlist : [...[...]] eg. ['a',['b',['e','f','g']],['c','x','y','z']]
	rlist : [[a:{'b','c','d'}],['b':{'e'},'c':{'e'}]...]
	"""
	rlist = []
	#print "getDepends :"
	package_name_list = manipulateCsv.selectPackageColumn(DB_NAME,"package_name")
	if depth < 1:
		print "depth is too "
	elif depth > len(package_name_list):
		print "the num of depth is larger than the num of node"
	#depends_matrix = graphStore.genDependsMatrix()	
	#index = package_name_list.index(package_name)
	n = 1
	node_list = []
	print package_name + "正向依赖关系:"
	while n <= depth: 
		node_dict = []
		if n == 1:
			node_list.append(package_name)
			node_dict = get_all_nodes(node_list)
			node_list = node_dict.values()
			print "层次:" , n
			print node_dict
			rlist.append(node_dict)
		
		else:	
			ite_node_list = handleDepends(node_list)
			node_dict = get_all_nodes(ite_node_list)
			node_list = node_dict.values()
			print "层次:" , n
			print node_dict
			rlist.append(node_dict)
		if isEmptyNodeList(node_list) != -1:
			break
		else:
			n = n + 1
	#print depends_matrix[index]
	#print "=======test log========"
	#print getDependsNodes(rlist)
	#print "=======test log1========"
	#print getDependsEdges(rlist)
	return rlist
					
		
	
def getRdepends(package_name,depth):
	"""
	rList : [...[...]] eg. ['a',['b',['e','f','g']],['c','x','y','z']]
	"""
	print package_name + "被依赖关系:"
        package_name_list = manipulateCsv.selectPackageColumn(DB_NAME,"package_name")
        if depth < 1:
                print "depth is too low"
        elif depth > len(package_name_list):
                print "the num of depth is larger than the num of node"
	n = 1
	rlist = []
        node_list = []
        while n <= depth:
                node_dict = []
                if n == 1:
                        node_list.append(package_name)
                        node_dict = get_all_rnodes(node_list)
                        node_list = node_dict.values()
                        print "层次:" , n
                        print node_dict
                        rlist.append(node_dict)

                else:
                        ite_node_list = handleDepends(node_list)
                        node_dict = get_all_rnodes(ite_node_list)
                        node_list = node_dict.values()
                        print "层次:" , n
                        print node_dict
                        rlist.append(node_dict)
                if isEmptyNodeList(node_list) != -1:
                        break
                else:
                        n = n + 1
	return rlist
#	dependsDict = manipulateCsv.selectRows(DB_NAME)
#	for key,value in dependsDict.items():
	

def checkValidPackage(package_name):
	if package_name in manipulateCsv.selectPackageColumn(DB_NAME,package_name):
		return 0
	else:
		return -1
		
def showDepends(package_name):	
	# get package depends from database package_info 
	#select package_name,depends,pre_depends from table where package_name = "package_name"
	#type: dict {package_name: [depends,pre-depends]}
	dependsDict = manipulateCsv.selectRows(DB_NAME)
	"""
	if dependsDict[package_name][0] != "":
		pkgList.append(dependsDict[package_name][0])
	elif dependsDict[package_name][1] != "":
		pkgList.append(dependsDict[package_name][1])
	"""
	print package_name + "依赖列表:"
	pkg_list = dependsDict[package_name][0] + ',' + dependsDict[package_name][1]	
	print  [x.strip() for x in pkg_list.split(',') if x != '']
	return  [x.strip() for x in pkg_list.split(',') if x != '']
	
def showrDepends(package_name):
	
	#get package depends from database package_info 
	#select package_name , depends , pre-depends from system_package_info ; store {package_name:[depends,pre-depends]}
	#type: rDict [pre-depends]
	rdependsDict = manipulateCsv.selectRows(DB_NAME)
	rDict = []
	for key,value in rdependsDict.items():
		rpkg_list = []
		pkg_list = value[0] + ',' + value[1]
		for x in pkg_list.split(','):
			if x.find('(') != -1:
				rpkg_list.append(x.split('(')[0].strip())
			elif x == "":
				continue
			else:
				rpkg_list.append(x.strip())
		if package_name in rpkg_list:
			rDict.append(key)

			
			
		"""
		if value[0] != "":
			if package_name in [elem.split(' ')[0] for elem in [x.strip() for x in value[0].split(',')]]:
				pkgList.append(key.replace(":","_"))			
		elif value[1] != "":
			if package_name in [elem.split(' ')[0] for elem in [x.strip() for x in value[1].split(',')]]:
                                pkgList.append(key.replace(":","_"))
		"""
	print package_name + "被依赖关系:"
	print rDict
	return rDict
			
def showDependsGraph(package_name,img_name,depth):
        dependsList = [] 
	dependsList = getDepends(package_name,depth)
        dep_node_list = getDependsNodes(dependsList)
        dep_edge_list = getDependsEdges(dependsList) 
        graphCreate.show_graph(dep_node_list,dep_edge_list,img_name)

def showrDependsGraph(package_name,img_name,depth):
	rdependsList = []
	rdependsList = getRdepends(package_name,depth)
	rdep_node_list = getDependsNodes(rdependsList)	
	rdep_edge_list = getRdependsEdges(rdependsList)
	graphCreate.show_graph(rdep_node_list,rdep_edge_list,img_name)

def showiDependsGraph(package_name,img_name):
	dependsList = showDepends(package_name)
	dep_node_list = [package_name]
	dep_edge_list = []
	for elem in dependsList:
		dep_node_list.append(elem)		
		dep_edge_tuple = (package_name , elem)	
		dep_edge_list.append(dep_edge_tuple)
	graphCreate.show_graph(dep_node_list,dep_edge_list,img_name)
"""
"""
def showirDependsGraph(package_name,img_name):
	rdependsList = showrDepends(package_name)	
	rdep_node_list = [package_name]
        rdep_edge_list = []
        for elem in rdependsList:
                rdep_node_list.append(elem)
                rdep_edge_tuple = (elem,package_name)
                rdep_edge_list.append(rdep_edge_tuple)
        graphCreate.show_graph(rdep_node_list,rdep_edge_list,img_name)

if __name__ == "__main__":
	"""
		python list_depends  packagename
	"""
	if len(sys.argv) != 3 and len(sys.argv) != 2:
		print "usage: python mainXX.py package_name optional:depth"
		sys.exit()
	if checkValidPackage(sys.argv[1]) == -1:
        	print "未找到该包"
	else:
		if len(sys.argv) == 3:
			showDependsGraph(sys.argv[1],"依赖",int(sys.argv[2]))
			showrDependsGraph(sys.argv[1],"被依赖",int(sys.argv[2]))
		else:
			showiDependsGraph(sys.argv[1],"依赖")			
			showirDependsGraph(sys.argv[1],"被依赖")
	sys.exit()
	
