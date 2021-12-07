工具类
==================


客户端连接找 .s.PGSQL.5432
-------------------------------------

适用版本：所有版本   

问题描述：

   客户端连接报错如下

   .. image:: images/FAQ28490.png
      :width: 650px
      :height: 47px

问题分析：   

   - ksql 连接时，正常会去寻找 .s.KINGBASE.54321文件，这里却去找 PGSQL文件，说明了可能相关lib干扰了。

   - ldd ksql，确认libpq.so是否没有正确指向/opt/kb86/ES/V8/Server/lib目录，而是指向链接到其他目录。

   - 确认LD_LIBRARY_PATH环境变量，确实包含第二步所指的“其他目录”。

   - 修改LD_LIBRARY_PATH环境变量，去除“其他目录”，或者将/opt/kb86/ES/V8/Server/lib放于LD_LIBRARY_PATH 最前面

   KES在编译时，会设置runpath，可以不设置LD_LIBRARY_PATH就能找到lib目录。但如果设置了LD_LIBRARY_PATH，LD_LIBRARY_PATH环境变量所指的路径优先级更高，这时可就会影响到数据库正常运行。



客户端管理工具无法加载ER图问题
---------------------------------------

适用版本：所有版本   

问题描述：客户端管理工具无法加载ER图

问题解决：   

   以下文件内容取自 ManagerTools/configuration/\*/bundles.info

   .. image:: images/FAQ28979.png
      :width: 650px
      :height: 148px

   标注的这行，然后删掉configuration下，除了config.ini和bundles.info所在的目录以外的其他目录，再删掉安装目录下的.kingbase，重启工具。

原因分析：

   plugin下每一个com.kingbase开头的jar包对应着一个插件，加载插件的配置文件就是bundles.info，现场的环境没有加载erd那个插件，导致er图打开失败



如何修改管理工具client_encoding
--------------------------------------------

适用版本：所有版本

问题描述：RT

问题解答：

   manager连接数据库所使用的client_encoding是通过ManagerTools/manager.ini设置的。

   .. image:: images/FAQ29287.png
     :width: 510px
     :height: 128px



迁移工具对于同名对象处理
-------------------------------

适用版本：所有版本   

问题描述：DTS从oracle迁移数据时，报错同名问题。

问题分析：对于oracle，同一schema下索引与表可以同名，但kingbase不允许。迁移工具在遇到同名时，会报错，需要用户手动处理。



数据迁移报“invalid byte sequence for encoding "UTF8": 0x00 "
-------------------------------------------------------------------

适用版本：V8R3 , V8R6

问题描述：如题

问题分析：0x00 是ascii 的0值，表示null，通过设置添加参数ignore_char_null_check=on ， 避免空值检查。



开始菜单没有数据库快捷工具图标
----------------------------------

适用版本：V8R3 , V8R6   

问题描述：

   正确安装数据库后，切换到kingbase用户，开始菜单没有数据库快捷工具图标。/home/kingbase/.local/share/applications/下也没有快捷方式

解决方式：   

   - 把安装路径下/home/kingbase/ES/V8/desktop下的文件拷贝到/home/kingbase/.local/share/applications/

   - 有的版本的操作系统，在安装完数据库软件后，需要注销，重新登录，才能看到开始菜单。



缺少操作系统GUI组件
---------------------------------

适用版本：所有版本   

问题描述：KES以console安装报错，unable to load and prepare the installer in console

原因分析：

   可能的原因是操作系统图形组件的缺失，需要安装相关组件。

   .. code::

      yum install gui
      yum install gnome
      yum install xorg



R3客户端无法使用scram-sha-256认证
---------------------------------------

适用版本：V8R3   

问题描述：JDBC驱动连接数据库时，报错如下：提示“The authentication type 10 is not supported. Check that you have configured the sys_hba.conf file to include the client's IP address or subnet, and that it is using an authentication scheme supported by the driver.”

问题解答：R3 的驱动无法使用scram-sha-256 认证，只能使用MD5认证



undefined symbol: PqgssEncInUse
---------------------------------------------

适用版本：V8R6

问题描述：

   运行ksql报错：

   .. code::

      $ ksql -Usystem -dtest -p36521 -h172.16.24.240
      ksql (V008R006C002B0016)
      ksql: symbol lookup error: ksql: undefined symbol: PqgssEncInUse

问题解答：通常是LD_LIBRARY_PATH环境变量设置问题。



Bulkload并行加载报错
------------------------------

适用版本：V7

问题描述：Bulkload并行加载报错，ERROR:  parallel threads initilization failed

问题分析：bulkload并行导入数据，需要在数据库的配置文件kingbase.conf中修改参数max_work_threads.如果没有，添加到配置文件。

例如：max_work_threads=16

 

 