TPCC测试类
==================

tpcc测试中是否需要开启autovacuum
------------------------------------------

在tpcc运行时间小于30分钟的时候禁用该参数，tpcc测试大于30分钟的时候需要开启。


index_cursor_id参数的数值是固定的么？
------------------------------------------

不是固定的，在tpcc测试中需要每次到数据库中查询到该参数的数值，然后配置到参数文件中，查询语句是

.. code::
 
   select oid from sys_class where relname like' bmsql_new_order_pkey';

 

在tpcc测试中unixdomain作用是？
------------------------------------------

Unix domain socket 或者 IPC socket是一种终端，可以使同一台操作系统上的两个或多个进程进行数据通信。与管道相比，Unix domain socket既可以使用字节流，又可以使用数据队列，而管道通信则只能使用字节流。

Unix domain socket的接口和Internet socket很像，但它不使用网络底层协议来通信。Unix domain socket 的功能是POSIX操作系统里的一种组件。Unix domain socket 使用系统文件的地址来作为自己的身份。它可以被系统进程引用。所以两个进程可以同时打开一个Unix domain sockets来进行通信。不过这种通信方式是发生在系统内核里而不会在网络里传播。
 

集群环境下测试tpcc连接参数怎样配置？
------------------------------------------

集群环境下连接参数和非集群环境一样。

.. code::

   driver=com.kingbase8.Driver
   conn=jdbc:kingbase8://127.0.0.1:54888/BENCHMARKSQL
   user=BENCHMARKSQL
   password=123456