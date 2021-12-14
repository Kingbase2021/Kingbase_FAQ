Python通过PyODBC连接Kingbase的说明
=====================================


环境配置
--------

###安装 pyodbc:
   推荐使用`pip`进行安装，执行`pip install pyodbc`

###安装 unixodbc:
   在终端输入并执行`sudo apt-get install unixodbc`


KingbaseV7驱动配置
--------------------------



###配置数据源和驱动
   安装iodbc后，在终端中输入并执行`odbcinst -j`，可以看到配置文件的路径，然后根据本机情况进行配置。

在`odbcinst.ini`文件中添加以下内容：

.. code::

	[Kingbase_v7]
	Driver = /lib/kdbodbc7.so ## odbc驱动库路径
	SETUP  = /lib/kdbodbc7S.so ## odbc安装库路径
	UsageCount = 1

在`odbc.ini`文件中添加以下内容：

.. code::

	[Kingbase_v7]
	Description = Kingbase V7
	Trace = On
	TraceFile = stderr
	Driver = Kingbase_v7 ## odbcinst.ini文件中的标签名
	SERVER = 192.168.8.52 ## 服务器地址
	USER = nli ## 用户名
	PASSWORD =  ##密码
	PORT = 54321 ##端口号
	DATABASE = TEST ##数据库名


KingbaseV8驱动配置
-------------------------


###配置数据源和驱动
   安装iodbc后，在终端中输入并执行`odbcinst -j`，可以看到配置文件的路径，然后根据本机情况进行配置。

在`odbcinst.ini`文件中添加以下内容：

.. code::

	[Kingbase_v8]
	Driver = /lib/kdbodbcw.so ## odbc驱动库路径
	SETUP  = /lib/kdbodbcw.so ## odbc安装库路径
	UsageCount = 1

在`odbc.ini`文件中添加以下内容：

.. code::

	[Kingbase_v8]
	Description = Kingbase V8
	Trace = On
	TraceFile = stderr
	Driver = Kingbase_v8 ## odbcinst.ini文件中的标签名
	SERVER = 192.168.8.132 ## 服务器地址
	USER = nli ## 用户名
	PASSWORD =  ##密码
	PORT = 54321 ##端口号
	DATABASE = TEST ##数据库名


连接测试
-------------

编写测试用python文件并执行

.. code::

    import pyodbc

	#非DSN方式
	conn = pyodbc.connect("DRIVER={Kingbase_v8};SERVER=192.168.8.132;port=54321;database=TEST;UID=nli;")

	#DSN方式
	#conn = pyodbc.connect('DSN=Kingbase_v7;SERVER=192.168.8.52;UID=nli')

	cursor = conn.cursor()
	cursor.execute("select * from TEST_BLOB;")
	rows = cursor.fetchall()
	for row in rows:
	    print(row)
	conn.commit()