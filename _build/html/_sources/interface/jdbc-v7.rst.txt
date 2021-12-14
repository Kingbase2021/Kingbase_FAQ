V7 JDBC常见问题
========================


JDBC读写分离配置
-------------------------

.. code::

	#打开读写分离功能
	USEDISPATCH=true
	#主机负载率，范围0到100，根据当前发给主机的语句数目与总语句数目的比例与HOSTLOADRATE设置的比例进行比较，当前者大于后者时，发给备机，否则发给主机。
	HOSTLOADRATE=33
	#备机地址，可指定多个，用“,”隔开
	SLAVE_ADD=192.168.28.20
	#备机端口，与备机地址对应，可指定多个，用“,”隔开
	SLAVE_PORT=54321
	#在新建连接时检查当前连接DB是不是Master,如果不是回去slave检查有没有Master,如果还是找不到Master就会向上报错
	MASTER_CHECK=true
	#开启集群备机监测线程定时监测集群备机状态
	CLUSTER_MONITOR=true
	#监测线程每次监测的间隔时间（单位：秒）
	MONITORINTERVAL=5
	#失败重发的最高次数
	RETRYTIMES=10
	#失败重发每次的间隔时间（单位：秒）
	RETRYINTERVAL=5
	#指定连接参数配置文件的路径，该参数需在连接串指定
	ConfigurePath=jdbc_v7.conf
	#黑名单，指定写函数，可指定多个，以分号分隔
	BlackList=writeFunction;updateFunction
	#指定事务中的分发策略，1表示事务都不分发，2表示事务中的写语句之前的语句可以分发，默认取值为：“2”
	TransactionDispatchStrategy=2
	#指定底层socket receive的超时时间，单位是秒，值可以为任意正整数，“0”表示没有超时，一直等，直到返回，默认取值为：“0”。
	socketTimeout=10

JDBC日志分析
-------------------------

常用的JDBC日志的命令：

1. 比如我要看一个线程的日志，假如131 是线程ID，

.. code::

   grep "\[131\]" ./jdbc_new.log > 131.log

这样就能看到131线程的完整JDBC日志，这样就能看到这个线程都干了什么事情，反推应用的业务逻辑。

2. 比如我要看 131这个线程里的所有执行语句

.. code::

   grep "consume time" ./131.log > 131_consume.log

这个日志就是这个线程里执行的全部的SQL是什么和SQL执行的时间。

例子：

.. code::

   [2019-08-23 19:57:00] [1] [com.kingbase.dispatcher.executor.DispatchAbstractStatement-->executeTemplet] DispatchPreparedStatementV2.execute(select 2;) consume time:::5(ms)

3. 比如我要看 monitor线程的日志

从全日志里搜  monitor找到对应的线程ID比如是[32]

.. code::

   grep "\[32\]" ./jdbc_new.log > 32.log

这样就能看到monitor不停的刷在线的主备机的IP，这样基本就能看到集群的历史和现在的状态，主备机都是谁。

4. 比如我要看是哪条SQL把事务设置为写事务了，从而不再分发备机。

从日志里搜”Enter transactional state from sql”，后面的SQL就是被识别为写语句的SQL。

例子：

.. code::

   [2019-08-23 20:14:41] [1] [com.kingbase.dispatcher.sqlParser.sql.SqlParser-->parse] Enter transactional state from sql[create temp table testk(id int)].

5. 比如我要看看都发生了什么错误

从日志里搜“Exception”，就能看到所有的异常信息。

例子：

.. code::

   [2019-08-23 20:14:41] [1] [com.kingbase.dispatcher.executor.DispatchAbstractStatement-->executeTemplet] failare execute in Master Exception: (e.getSQLState={42601},e.getMessage={[KingbaseES Server]ERROR: 语法错误 在 ")" 附近 Line 1 at SQL statement})


JDBC读写分离分发策略
-------------------------

根据当前发给主机的语句数目与总语句数目的比例与HOSTLOADRATE设置的比例进行比较，当前者大于后者时，发给备机，否则发给主机。为防止语句数目统计的Integer类型溢出，当总语句数目达到Integer.MAX_VALUE时，通过计算当前分发至主机语句的百分比，更新当前发给主机的语句数目与总语句数目。


FastPath call returned invalid large object descriptor：0.
---------------------------------------------------------

V7出现非法大对象操作符异常，原因是多线程操作同一个连接，默认发布版本不支持这样使用，需替换支持该使用方法的jar包。


fetchsize功能
-------------------------

通过配置连接串参数ClientCursor=false&FetchSize=10000开启fetchsize功能，FetchSize的默认值为50，无需开启事务，但当语句里有绑定参数时，不支持使用该功能。也可通过ps.setFetchSize(int);来指定fetchsize的大小。


mybatis一次执行多条语句时报错，错误信息为：“预置的语句中不能插入多个命令”
-----------------------------------------------------------------------

原因是V7不支持多语句。