Apache James适配
=================================

环境搭建参考https://blog.csdn.net/qq_33945246/article/details/91417413

除此外还需两项配置：

V8R3:

	1. 在james-database.properties配置连接参数，并且配置vendorAdapter.database=ORACLE；

	2. 在sqlResources.xml文件的dbMatchers节点中设置
	<dbMatcher db="postgresql" databaseProductName="kingbase.*"/>

V8R6：

	1. 在james-database.properties配置连接参数，并且配置vendorAdapter.database=POSTGRESQL；

	2. 在sqlResources.xml文件的dbMatchers节点中设置
	<dbMatcher db="postgresql" databaseProductName="kingbase.*"/>