文件说明
.
├── depends_graph1.csv  用于测试的文件的数据库文件
├── depends_graph.csv   正确从系统中导入的依赖关系的数据库文件
├── eggs.csv		
├── graphCreate.py	可视化输出文件
├── graphCreate.pyc
├── graphStore.py	数据存储文件
├── graphStore.pyc
├── img
│   ├── 被依赖
│   ├── 被依赖.svg
│   ├── 依赖
│   └── 依赖.svg
├── insertData2Db.py   #deprecated 
├── insertData2Db.pyc   #deprecated 
├── mainListDepends.py   系统的主入口，列出软件包的依赖关系和被依赖关系（单层或者多层 ）
├── mainParser.py	解析依赖文件/var/lib/dpkg/status , 允许两种输入方式，另一种方式是iso作为输入.
├── manipulateCsv.py    用来取代insertData2Db.py
├── manipulateCsv.pyc
├── manipulateDb.py     #deprecated 
└── manipulateDb.pyc    #deprecated 
