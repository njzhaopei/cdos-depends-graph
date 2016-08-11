#!/usr/bin/python
import manipulateCsv
DB_NAME = "depends_graph.csv"
		
def getIndexPair(key,value):
        print "=============getIndexPair=================="
        rindex_pair = []
        system_pkg_list = manipulateCsv.selectPackageColumn(DB_NAME,"package_name")
        try:
                key_index = system_pkg_list.index(key)
                value_index = system_pkg_list.index(value)
                rindex_pair.append(key_index)
                rindex_pair.append(value_index)
        except ValueError:
                print "VAlUE ERROR:" + key
                return [-1,-1]
        return rindex_pair

#get direct graph info from db
def genDependsMatrix():
        """
        rtype: [
        [ 0 , 0 , 0 , 0 ...]
        [ 0 , 0 , 0 , 0 ...]
          :
          :
       ...]
        """
	# get package name list from db 
	package_name_list = manipulateCsv.selectPackageColumn(DB_NAME,"package_name")
	print package_name_list
	#get package row dictionary from db
	package_rows_dict =  manipulateCsv.selectRows(DB_NAME)
	print package_rows_dict
	#init depends matrix
        depends_matrix =  [[0 for col in range(len(package_name_list))] for row in range(len(package_name_list))]
        i = 0
        for key in package_name_list:
                i = i+ 1
                if key == '':
                        continue
		all_str = package_rows_dict[key][0] + ',' + package_rows_dict[key][1] 
		all_list = all_str.split(',')
		print all_list
                for elem in all_list:
			if elem == '':
				continue
			if elem.find('(') != -1:
                        	index_pair = getIndexPair(key,elem.split('(')[0].strip())
                        	if index_pair[0] == -1 and index_pair[1] == -1:
                                	continue
                        	else:
                                	depends_matrix[index_pair[0]][index_pair[1]] = 1
			else:
				index_pair = getIndexPair(key,elem.strip())
                                if index_pair[0] == -1 and index_pair[1] == -1:
                                        continue
                                else:
                                        depends_matrix[index_pair[0]][index_pair[1]] = 1

        return depends_matrix	

# test
#if __name__ == "__main__":
#	print genDependsMatrix()
