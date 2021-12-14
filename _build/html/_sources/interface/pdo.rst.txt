Pdo接口常见问题
=======================

导入驱动失败
----------------------

常见如下情况:

   .. figure:: images/pdo-1.png

问题现象：

   提示libkci没有找到

解决方案：

	1. ldd pdo_kdb.so 文件查看是否没有找到 libkci 驱动

	.. figure:: images/pdo-2.png

	2. 修改环境变量，LD_LIBRARY_PATH 指向金仓数据的 Server/lib 目录

	.. code::

	   export LD_LIBRARY_PATH=XXX/Server/lib


加载 PDO_KDB 报错
----------------------

PHP Warning:  PHP Startup: Unable to load dynamic library '/usr/lib64/php/modules/pdo_kdb.so' - /usr/lib64/php/modules/pdo_kdb.so: undefined symbol: pdo_raise_impl_error in Unknown on line 0

解决方案：

   查看 PDO_KDB.SO 驱动在 php.ini 中加载顺序，确保PDO_KDB.SO的驱动加载顺序在 php 的PDO.SO 模块之后


PHP的线程安全和非线程安全
-------------------------------

PHP发布的版本分为支持线程安全和不支持线程安全两种：

通过命令查看： 

.. code::

   php –i|grep –i thread

.. figure:: images/pdo-3.png


PDO编译依赖于PHP的configure  所以，PDO适配的时候也需要跟随PHP的配置。即如果PHP打开了Thread  Safety则，PDO也需要提供线程安全的版本。

.. figure:: images/pdo-4.png

例如：PHP 打开了线程安全，PDO是没打开的版本则会报错：找不到file_globals

PHP通过在configure的时候指定--enable-maintainer-zts来支持线程安全。PDO编译的时候需要依赖PHP的configure，来实现线程安全与否。



使用的PDO驱动与PHP版本不匹配
----------------------------

.. figure:: images/pdo-5.png

此图表示PHP5.6.40使用了PHP5.3编译的PDO驱动，导致加载失败。

.. code::

	Module compiled with module API
	PHP compiled with module API

不匹配。

.. code::

	PHP5.2     API=20060613
	PHP5.3     API=20090626
	PHP5.4     API=20100525
	PHP5.5     API=20121212
	PHP5.6     API=20131226
	PHP7.2     API=20170718


Windows下使用PDO驱动的方法
---------------------------------

将解压出的php_pdo_kdb.dll与libkci.dll 放到php7ts.dll文件所在的目录，因为php_pdo_kdb.dll需要依赖php7ts.dll 。  此目录一般为php.exe所在的目录。

.. figure:: images/pdo-6.png

修改php.ini  加入

.. code::

   extension=C:\php-7.2.0\x64\Release_TS\php_pdo_kdb.dll

请将C:\php-7.2.0\x64\Release_TS\php_pdo_kdb.dll 修改为实际的路径

执行php -m 可以检测驱动是否加载成功

.. figure:: images/pdo-7.png


thinkphp使用过程中报函数不存在的问题
----------------------------------------------

问题描述：

.. figure:: images/pdo-8.png

解决方案：在使用thinkphp时，用 ksql 导入kingbase.sql文件，创建框架所需函数，解决上述问题。


通过金蝶等中间件查看驱动加载信息时，看不到pdo_kdb或者pdo_pgsql的信息
-------------------------------------------------------------------


问题描述：

.. figure:: images/pdo-9.png

.. figure:: images/pdo-10.png

问题分析：php扩展功能的文件，一般放在/lib/php/extensions/**/下，在php.ini中配置是，只需要将相关功能的extension=功能名；如果配置了功能扩展文件夹，php可以识别的到该路径，所以看到使用php -m可以看到功能加载信息，但有些第三方代理不一定可以识别的到，所在，建议最好扩展放在默认路径下！
