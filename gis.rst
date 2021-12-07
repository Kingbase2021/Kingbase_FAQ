空间组件
=================

Create extension postgris 报错“GLIBC_2.18 not defined in file libc.so.6”
---------------------------------------------------------------------------

适用版本：V8R3 , V8R6

问题描述：

   create extension postgis，报错如下：无法加载库“postgis-2.5.si”: Server/lib/libstdc++.si.6: symbol \__cxa_thread_atexit_impl, version GLIBC_2.18 not defined in file libc.so.6 with link time reference

问题分析：

   1) lddServer/lib/libstdc++.si.6 ，确认动态链接操作系统的 libc.so.6

   2) strings libc.so.6 | grep GLIBC | more , 看到最高只到GLIBC_2.17，也就是说操作系统自带的gcc版本不支持postgis-2.5。经验证，操作系统的gcc版本是4.8.5，而我们的编译环境的gcc版本是5.3.1，需要升级操作系统的gcc版本或根据底版本的gcc重新编译。



acgis版本备份还原
---------------------------------------

适用版本：V8.3.1

问题描述：注意acgis备份还原不可将用户权限忽略，否则可能赵成acgis空间信息错乱，导致备份还原后acgis无法连接数据库。

注意sys_restore时候，千万不可带-x参数。


R6 是否支持超图
---------------------------------------

适用版本：V8R6

问题描述：RT

问题解答：R6 支持超图 10.1.1连接，但前提是必须要有postgis组件。