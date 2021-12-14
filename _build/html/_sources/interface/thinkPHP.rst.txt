ThinkPHP接口常见问题
==============================


如何在搭建Thinkphp+apache+kdb环境
-----------------------------------

apache环境搭建
^^^^^^^^^^^^^^^^^^

源码编译
~~~~~~~~~~~~~~

.. code::

	#tar httpd-*.tar.gz
	#cd httpd-*
	#configure --prefix=`pwd`/release


配置httpd.conf
~~~~~~~~~~~~~~~~

在conf目录中，打开httpd.conf

1. 配置加载库路径

找到LoadModule位置，增加或者修改如下配置

.. code::

	LoadModule php5_module        modules/libphp5.so
	PHPIniDir /opt/php/php-5.6.40/release/lib

2. AddType

.. code::
   
   AddType application/x-httpd-php .php　

3. 配置默认访问首页

最后需要增加首页文件，让apache支持默认首页是index.php

.. code::

	<IfModule dir_module>
	    DirectoryIndex index.html index.php
	</IfModule>　

4. 配置项目路径

在配置文件httpd.conf中，修改

.. code::

   DocumentRoot "/opt/httpd-2.2.15/release/htdocs"修改DocumentRoot路径即可


php环境搭建
^^^^^^^^^^^^^^^^^^

配置驱动
~~~~~~~~~~~

将pdo_kdb.so、 kdb.so驱动，放至 
/php-5.6.40/lib/php/extensions/no-debug-non-zts-20131226修改配置文件php.ini

extension=/opt/php/php-5.6.40/release/lib/php/extensions/no-debug-non-zts-20131226/pdo_pgsql.so

extension=/opt/php/php-5.6.40/release/lib/php/extensions/no-debug-non-zts-20131226/pgsql.so


thinkphp在httpd中使用
^^^^^^^^^^^^^^^^^^^^^^^

配置数据库连接
~~~~~~~~~~~~~~~~

下载thinkphp3.1.2完整版本，加压之后，拷贝至httpd/htdocs中，执行index.php生成工程文件

.. code::

	<?php
	//开启调试模式
	define('APP_DEBUG',true);
	//定义项目名称和路径
	define('APP_NAME', 'app');
	define('APP_PATH', './app/');
	// 加载框架入口文件
	require( "./ThinkPHP/ThinkPHP.php");


配置数据库连接
~~~~~~~~~~~~~~~~

打开app/Conf/config.php

.. code::

	<?php
	return array(
	    'URL_MODEL' =>      3, // 如果你的环境不支持PATHINFO 请设置为3
	    'DB_TYPE'   =>      'kdb'
	    'DB_HOST'   =>      '127.0.0.1',
	    'DB_NAME'   =>      'test',
	    'DB_USER'   =>      'system',
	    'DB_PWD'    =>      '',
	    'DB_PORT'   =>      '54322',
	    'DB_PREFIX' =>      'think_',
	);


修改控制文件
~~~~~~~~~~~~~~~~

打开app/Lib/Action/IndexAction.class.php

.. code::

	<?php
	class IndexAction extends Action {
	    public function index(){
	        $user=M('Form');   //大M方法访问数据表
	        $sql=$user->select();  //thinkPHP 封装的SQL查询所有数据
	        
	        echo $sql['id'];
	        var_dump($sql['id']);
	        var_dump($sql['title']);
	        var_dump($sql['content1']);
	        var_dump($sql['create_time']);
	​
	        $data['id'] = 10;
	        $data['title'] = 'ThinkPHP@gmail.com';
	        $data['content1'] = 'ThinkPHP@gmail.com';
	        $data['create_time'] = 15;
	        $user->data($data)->add();
	        $sql=$user->select();  //thinkPHP 封装的SQL查询所有数据
	        var_dump($sql);     //打印出数据
	    }
	}


添加html文件
~~~~~~~~~~~~~~~~