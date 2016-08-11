  该项目是主要是为了帮助Debian系列的专家用户获得系统中软件包的依赖关系并以可视化的形式输出。
=====================================================================================
适合试用系统 
  Debian系列系统： linux Mint ; ubuntu 14.04；等等 。
  
一、 导入系统中已安装包信息到CSV文件中 
执行命令： python mainParser.py [optional:isopath+isoname]

eg. 
    
    python mainParser.py  #默认从当前系统/var/lib/dpkg/status中导入软件包数据到CSV中 
    
    python mainParser.py /path/*.iso  #将从指定iso中获得软件包数据，导入CSV中
    
二、 列出单个软件包的依赖关系 
  执行命令： python mainListDepends.py [package_name] [optional:depth]
eg. 
   
    python mainListDepends.py zip #默认列出zip包的单层依赖和被依赖关系，并且可视化数据输出到image目录中
    
    python mainListDepends.py zip  #列出zip包的多层依赖和被依赖关系，并且可视化数据输出到image目录中 
  
三、 获得系统中所有没有被其他包依赖的列表
  执行命令: python userApi.py #将导出系统中未被依赖的软件包到指定名称的CSV文件中
  
  
  
