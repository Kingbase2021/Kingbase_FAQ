扩展组件
==========

如何查看系统是否支持某组件
---------------------------------------

适用版本：所有版本

问题描述：KES与原生PG不同，许多开源的组件不能直接在KES上使用，需要研发针对特定平台重新编译。如果用户想知道当前的版本自带或支持哪些组件，只需查询sys_available_extensions



oracle_fdw支持平台
---------------------------------------

适用版本：V8R6 , V8R6

目前只支持linux x86_64


create extension oracle_fdw报.so找不到加载失败
------------------------------------------------------------------------------

适用平台：[KESV8R2/3]

依赖oracle官方instantclient-basic-linux.x64-11.2.0.4.0.zip，目前推荐使用11.2版本，其他版本可能跟操作系统存在兼容问题，解决方法根据现场选择以下之一。

方法1（当机器上安装了>11.2的instantclient时推荐使用）：

   解压后将so拷贝到kingbase安装后的lib目录下

方法2（当机器上没有安装过instantclient时选用）：

   解压到/usr/lib/路径下后执行ldconfig



oracle_fdw支持功能
---------------------------------------

基本的select insert delete， 简单的join


Sys_pathman
---------------------------------------

问题描述: pathman_config、pathman_config_params 删除后，如何重建？

问题解决：pathman_config、pathman_config_params这两个表是sys_pathman插件的表，想找回来可以drop extension之后再create extension; extension。



Separate_power
---------------------------------------

问题描述: 需要开启审计日志，没有SYSSAO和SYSSSO用户，有什么解决办法吗

问题解决：create extensionSeparate_power



Sysaudit
---------------------------------------

如何删除语句审计日志？
^^^^^^^^^^^^^^^^^^^^^^^^^^

语句审计日志可以通过视图sysaudit.sysaudit_records查询。如果要删除语句审计记录，只需将移除$KINGBASE_DATA/aud目录下的文件。

