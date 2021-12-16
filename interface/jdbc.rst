JDBC接口
========================


JDBC打开日志方式
--------------------------

JDBC驱动支持控制日志打印级别和日志输出到文件或者控制台。

日志级别：loggerLevel = 日志级别  指定日志记录级别。例如："OFF", "INFO", "DEBUG", "TRACE"，默认值是null即不输出日志。

日志输出：loggerFile = 日志文件名字

指定日志信息保存文件或者console 输出：

   1：如果没有指定loggerFile，表示不生成JDBC日志文件,日志信息全部打印到当前console输出。
   
   2：如果loggerFile有指定路径，则只打印到文件。例如：LogFile=e:\\logFile.txt，默认值是null。这个路径可以是相对路径，也可以是绝对路径。
 

没有VIP情况下，JDBC连接如何配置？
---------------------------------------------

JDBC驱动通过IP，端口，数据库名，用户名，密码来连接数据库，没有VIP情况下，就配置数据库的集群所有主机实际的地址。

配置文件的内容在开始配置后不会变更，连接成功后，驱动会给数据库发送查询语句来判断当前配置的主机是否是主机，不是的话回去更新主备机的记录，但这个是记录在驱动的内部的，不会去写配置文件。

jdbc不支持自带连接池，客户可以使用第三方连接池，如druid，c3p0,dbcp等


V8R6 JDBC能否使用VIP？
-----------------------------

不能使用vip。

jdbc.conf文件有 host和 slave_add项，表示主、备节点。比如，初始配置 host=VIP，而VIP是飘移的，如果VIP飘移到备机，那相当于集群少了一台主机（原主机“不见”了）


LOB对象update机制
---------------------------

应用SQL：1条语句，update GA_MSGS set "MSG_BODY"=$1 where MSG_ID ='$2'。

数据库日志捕获SQL为:大约50条，update GA_MSGS set "MSG_BODY"=$1 where "CTID"=$2 and  "XMIN"= $3 returning CTID,XMIN;

尝试ksql执行update GA_MSGS set "MSG_BODY"=$1 where MSG_ID = '$2'，数据库日志捕获为1条update GA_MSGS set "MSG_BODY"=$1 where MSG_ID = '$2'，未发生变化。

是java驱动转化了SQL语句吗，另外50条update语句中的blob字段参数值，是一个不断增长的过程，每自动更新下一次，参数值会补充一断新的值。

日志分析：

   1、应用没有这种SQL，是JDBC接口自动转换的。

   2、每次update操作  "CTID"=$2 and  "XMIN"= $3参数值 ctid每次增加 1，xmin都是相同的。

   3、库日志中的update语句blob参数$1，目前看着符合规律，继承之前的参数变得越来越长，比如第一次a，第二次ac，第三次acb，第四次acbd…

结论：

   用select ... for update，查询大对象，然后用大对象的set方法（如blob.setBytes）设置大对象的值时，驱动实际执行了一条update语句，这条update语句是驱动构造的。

   因为R3的大对象实际是bytea和text，数据都是写在用户表里的，内容都是一次写过去的。

   如果应用本身是update语句，驱动不会去修改语句，只有通过大对象的方法去写大对象才会生成该语句。

   这个write方法每次调用一次就会调用update语句写一次，Blob实际是bytea，没法分片写，所以实际blob内容是缓存在本地的，每次添加内容，都会在原来的内容上加上新的内容更新一次。

   .. figure:: images/jdbc-33958.png
      :width: 554px
      :height: 416px
 

KBBlob 迁移至Oracle
-----------------------------

适用版本：所有版本

问题描述：用户将BLOB从Kingbase迁移至Oracle，报错如下：“kblob cannot be cast to oracle.sql.blob”

问题分析：KBBlob 不支持迁移至Oracle Blob，只能是Oracle Blob迁移至KBBlob



JDBC的jar包需要区分JDK版本，需要区分OS和CPU平台吗？
----------------------------------------------------------

适用版本：V8R2


问题分析：JDBC目前编译时，是根据JDK环境编译的jar包。所以请使用时检查应用的JDK环境。V82的JDBC驱动支持Oracle 1.6，1.7，1.8 和OpenJDK 1.6,1.7,1.8

兼容度：低版本JDK环境编译的jar包可以运行在高版本的JDK环境下，反之则不行。
JAVA程序编译出来都是class文件的中间码(运行在JVM虚拟机上)，不是机器码所以不区分OS和CPU，只区分JDK环境。所以正常来说只需要保证JDK的版本匹配即可。



JDBC的连接参数只能通过URL串来填写吗？
-------------------------------------------------

适用版本：V8R2

问题描述：JDBC的连接参数只能通过URL串来填写吗？

问题分析：不是，除了ConfigurePath外，其它也可用配置文件方式。JDBC的可选的连接串参数是比较多的，当你需要的参数较多时都写在连接串上显得比较笨拙，为了方便现场人员运维管理，新提供了JDBC配置文件的方式来配置参数。



如何使用JDBC配置文件方式？
-------------------------------------------------

适用版本：V8R2


问题分析：JDBC是否使用配置文件，是通过连接串参数ConfigurePath控制。当你ConfigurePath=jdbc.conf时，会优先使用配置文件里的参数。如果没有ConfigurePath参数，就只使用URL连接串中的参数。



JDBC读写分离怎么打开关闭?
-------------------------------------------------

适用版本：V8R2


问题分析：JDBC是否使用读写分离功能,通过USEDISPATCH控制。USEDISPATCH=true时就会使用读写分离功能进行分发。USEDISPATCH=false，或者不写这个参数时，就使用原JDBC单机方式。



JDBC 读写分离都需要配置哪些参数？
----------------------------------------------------------

适用版本：V8R2

一般情况下，只需额外5个参数来控制。

.. code::

  #打开读写分离功能，
  USEDISPATCH=true
  #备机地址
  SLAVE_ADD=192.168.8.223,192.168.8.130
  #备机端口
  SLAVE_PORT=54321,54321
  #主机读负载率，备机之间轮询平分，取值范围0-100,例如0表示读语句全部分发备机，100表示读语句全部发送主机
  HOSTLOADRATE=33
  #底层socket receive的超时时间
  socketTimeout=10
  #是否使用连接池缓存连接
  USECONNECT_POOL=false



JDBC读写分离一主两备的URL和配置文件的样例
----------------------------------------------------------

适用版本：V8R2

.. node::

  JDBC读写分离的IP地址都只能使用真实IP地址，不能使用虚拟IP地址，否则可能造成切机后判断主机不准问题，连接建立数不对等问题。

1：只用连接串,开启JDBC读写分离 一主两备：

URL   

.. code::

  jdbc:kingbase8://192.168.8.128:54321/TEST?USEDISPATCH=true&SLAVE_ADD=192.168.8.223,192.168.8.130&SLAVE_PORT=54321,54321&HOSTLOADRATE=33&USECONNECT_POOL=false  

2：连接串+配置文件,开启JDBC读写分离 一主两备：
  
URL  

.. code::

  jdbc:kingbase8://192.168.8.128:54321/TEST?ConfigurePath=jdbc.conf
  
配置文件

.. code::

  USEDISPATCH=true
  SLAVE_ADD=192.168.8.223,192.168.8.130
  SLAVE_PORT=54321,54321
  HOSTLOADRATE=33
  socketTimeout=10
  USECONNECT_POOL=false

3：目前读写分离实际项目中用到的配置文件参数样例：

.. code::

    #主机地址
    HOST=121.1.20.3
    PORT=54321
    DBNAME=NPC
    user=RDWWpom

    password=RDWW123456
    #loggerLevel can be OFF, INFO, DEBUG, TRACE
    loggerLevel=OFF
    loggerFile=jdbc_test.log
    preferQueryMode=extendedForPrepared
    #是否使用读写分离功能
    USEDISPATCH=true
    HOSTLOADRATE=33
    #备机地址
    SLAVE_ADD=192.168.8.220,192.168.8.221
    SLAVE_PORT=54321,54321
    #是否使用连接池缓存连接
    USECONNECT_POOL=false
    CONNECT_POOLSIZE=1
    #在新建连接时检查当前连接DB是不是Master,如果不是回去slave检查有没有Master,如果还是找不到Master就会向上报错
    MASTER_CHECK=true
    #失败重发的最高次数
    RETRYTIMES=10
    #失败重发每次的间隔时间（单位：秒）
    RETRYINTERVAL=5
    #开启集群备机监测线程定时监测集群备机状态
    CLUSTER_MONITOR=true
    #监测线程每次监测的间隔时间（单位：秒）
    MONITORINTERVAL=5
    #指定底层socket receive的超时时间，值可以为任意正整数，“0”表示没有超时，一直等，直到返回，默认取值为：“0”（单位：秒）
    #socketTimeout=10
    #指定Socket做connect时的超时时间，默认取值为：“10”（单位：秒）
    #connectTimeout=10


JDBC连接池功能，是否开启，开启后的功能及性能
----------------------------------------------------------

适用版本：V8R2

问题分析：

  如果应用已经有了连接池，就不开启JDBC连接池，因为连接池需要锁来管理全局队列，高并发建连接会有性能损耗。
    
  如果应用没有连接池，可以开启JDBC连接池，因为频繁建连接时很耗时的行为。开启连接池可以降低应用频繁建连接的损耗。
  
  JDBC连接池功能限制：JDBC连接池只是为了读写分离测试性能时使用，只支持相同用户的连接。如果是不同用户的连接，不要使用，会有模式混乱问题。


JDBC读写分离配置参数依赖关系                
----------------------------------------------------------

适用版本：V8R2

关于JDBC 读写分离配置项的依赖关系：

USEDISPATCH=false       
  #是否使用读写分离功能,此配置项关闭JDBC就变成单机JDBC，无读写分离功能。

MASTER_CHECK=true    
  #在新建连接时检查当前连接DB是不是Master,如果不是会去slave节点中检查有没有新升级的Master,如果还是找不到Master节点就会向上报错。（此功能开启需要同时开启读写分离功能）。

USECONNECT_POOL=false   
  #是否使用连接池缓存连接，此功能开启需要同时开启读写分离功能。（此功能开启需要同时开启读写分离功能）。

MASTER_CHECK=true    
  #在新建连接时检查当前连接DB是不是Master,如果不是回去slave检查有没有Master,如果还是找不到Master就会向上报错。（此功能开启需要同时开启读写分离功能）。

RETRYTIMES=10        
  #连接异常问题造成的语句执行失败情况下，重建连接并重发的最高重试次数（0~100）。（此功能开启需要同时开启读写分离功能）

RETRYINTERVAL=10     
  #失败时重建连接并重发的每次的间隔时间（单位：秒）。（此功能开启需要重试次数大于0）

CLUSTER_MONITOR=true 
  #开启集群备机监测线程定时监测集群备机状态，更新全局备机信息（无锁）。（此功能开启需要同时开启读写分离功能）。

MONITORINTERVAL=5    
  #备机监测线程每次查询备机信息的间隔时间（单位：秒）。（此功能开启需要同时开启读写分离功能）。

TransactionDispatchStrategy=2 
  #事务中语句的分法策略，1表示事务中的所有语句都不分发，默认是2 表示事务中遇到写语句之前的读语句可以分发。（此功能开启需要同时开启读写分离功能）。
         


JDBC读写分离在哪些情况下重发也不会成功
----------------------------------------------------------

适用版本：V8R2

JDBC支持切机本意就是指尽量让应用的语句不因为切机造成执行失败，让应用对切机无感知。对于单事务语句基本都可以重发成功。

但是并不是所有的语句都可以重发成功。

- 涉及连接会话上下文的情况。

- 游标：cursor，refcursor切机后全部丢失，重发不能成功。

- 事务：切机后连接全部都断掉了，事务回退失败，不能重发。

- 结果集遍历：和游标类似，重发不能成功。

- 批量执行。



JDBC读写分离分发策略
----------------------------------------------------------

适用版本：V8R2

读语句分发，分两种情况：

1. 单语句事务，这种情况下每条语句都是一个独立的事务，所以读语句分发备机没有问题

2. 多语句事务，这种情况下，读语句处于事务内，分发需要考虑事务隔离级别，V82支持的三种隔离级别：可重复读，读提交，序列化。严格意义上这三种都不允许读语句分发，因为可能出现不可重复读或者读不到已提交的内容。

但是如果事务内的语句就不分发的话，读写分离就失去大半意义了，因为无论是应用还是框架基本上都是用事务控制的，所以JDBC提供一个分发策略参数控制，

TransactionDispatchStrategy可以选择分发策略：（性能优先，默认是2） 

1. 事务内的所有语句都只发主机，完全不分发备机。

2. 事务内遇到写语句之前的读语句，可以分发备机，遇到写语句之后就只发主机。



JDBC读写分离相关参数默认值
----------------------------------------------------------

适用版本：V8R2


loggerLevel=OFF
  #默认 OFF，可用参数OFF, DEBUG, TRACE

loggerFile=jdbc_test.log
  #默认 null，日志文件名，可以是相对路径，也可以是绝对路径，如果默认null就是不生成日志文件

preferQueryMode=extendedForPrepared
  #默认 extend，可用参数simple，extend，extendedForPrepared

socketTimeout=10
  #默认 0（没有超时，一直等，直到返回），单位是秒，可选值为任意正整数，控制底层socket receive的超时时间。次参数设置取决于应用的超时控制机制，如果应用有自己的超时控制比较好，能够自己控制对端不在线而造成的socket receive一直等待的时间，这个值可以设0完全让应用去控制超时时间。但是如果应有没有超时控制或者控制的不好，只要JDBC不返回，应用不能自己根据超时返回，一直阻塞，那就需要设置这个超时时间，一般设置为该应用查询语句正常返回的最长返回时间。

USEDISPATCH=true
  #默认 false，用来控制是否使用读写分离功能

HOSTLOADRATE=33
  #默认 0，用来控制主机读负载率

SLAVE_ADD=192.168.8.228,192.168.8.229
  #备机地址
  #默认 null

SLAVE_PORT=54321,54321
  #默认 null

USECONNECT_POOL=false
  #是否使用连接池缓存连接
  #默认 false，开启连接池

CONNECT_POOLSIZE=100
  #默认 10个连接

MASTER_CHECK=true
  #在新建连接时检查当前连接DB是不是Master,如果不是回去slave检查有没有Master,如果还是找不到Master就会向上报错
  #默认 true

RETRYTIMES=10
  #失败重发的最高次数
  #默认 10 次

RETRYINTERVAL=5
  #失败重发每次的间隔时间（单位：秒）
  #默认 5 秒

CLUSTER_MONITOR=true
  #开启集群备机监测线程定时监测集群备机状态
  #默认 开启

MONITORINTERVAL=5
  #监测线程每次监测的间隔时间（单位：秒）
  #默认 50秒

TransactionDispatchStrategy =2  默认是2
  #事务内语句分发策略，提供两种策略选择
  #1：事务内语句全都不分发，只发给主机。2：事务内遇到写语句之前读语句可以分发

集群状态正常，sockettimeout设置大于0时，为什么执行时间超长的事物会失败并导致jdbc重建连接？
---------------------------------------------------------------------------------------

适用版本：V8R2

sockettimeout是控制底层socket超时返回的最长时间，默认是0，即没有超时。如果指定大于0的值，意思就是最多等待sockettimeout的时间socket的receive操作就会返回，这主要是用来防止当server掉线时，client端socket的receive操作会一直等待。但是这会带来副作用，就是如果一条语句真的执行很长时间超过了sockettimeout的值时，会被认为是超时而中断receive返回超时错误，如果是在读写分离状态下，超时会造成重建连连接重发语句。一条语句如果是因为大于设置的socketTimeout而超时退出，那么应用需等待（socketTimeout * （RETRYTIMES + 1）+ RETRYINTERVAL * RETRYTIMES）才会收到异常。此时需要根据用户的语句最长执行时间来设置sockettimeout或者设置为0一直等待。

如果应用自己有防这种JDBC操作一直不返回的机制，JDBC调用不返回，应用会有自己的超时控制，那就不需要JDBC设置soc kettimeout，让应用自己控制超时时间就好。

如果应用没有这种防呆机制，一个JDBC操作不返回就会造成应用完全卡死，那就需要设置JDBC的sockettimeout值，让JDBC来控制超时时间。



主备切换后，备机rewind，或者备机故障后，备机恢复时为什么 备机的连接数是持续上升，而不是一次性全部建好？
--------------------------------------------------------------------------------------------------

适用版本：V8R2

主备切换后，连接不是马上就全部建立起来的，而是应用确实调用到JDBC时，JDBC才会去判断集群是否切换了，重建连接，重发语句执行。所以连接数是恢复速度和应用的操作JDBC负荷有关，通常是慢慢建立起来的，备机的连接会稍滞后于主机连接恢复速度，因为切机重发时，都是只要能找到新的主机就可以重发成功了，不会等到所有备机重启完成。只有等到下一次发送语句触发备机时，JDBC才会去检测备机是否已经起来了，如果是才会重建备机连接。


主机切机后，应用第一次登陆WEB慢，JDBC等待时间分析
----------------------------------------------------------

适用版本：V8R2

1. 局域网内 测试拔网线切机 

    1) 集群的新主机起来可连接后->
    2) 应用用户登录WEB->
    3) 使用连接池中已经有的JDBC连接(主机的连接都已经失效，备机的连接在rewind之前都还有效) ->
    4) 发送SQL ->
    5) (I/O Error 20秒)收到错误返回 ->
    6) 重建JDBC连接 （sleep 5秒）->
    7) (在线0.1秒返回)+(不在线的需要10秒返回) ->
    8) 重建连接完成开始执行登陆SQL返回，总计35秒左右。

2. 其中 (不在线的需要10秒返回) 这个可以通过connectTimeout 参数控制connect超时时间，默认是10秒。

  其中 (sleep 5秒) 这个可以通过RETRYINTERVAL参数控制重建连接的间隔时间，默认是5秒。

  其中 (I/O Error 20秒) 这个可以通过socketTimeout参数控制receive的超时时间，默认是0无限等待。

3. 备机的连接不是马上断掉，而是在一段时间内都还可以使用，等到rewind时连接才会全部断掉。



JDBC打开日志方式 
----------------------------------------------------------

适用版本：V8R2

JDBC驱动支持控制日志打印级别和日志输出到文件或者控制台。

**日志级别：** 

loggerLevel = 日志级别
  指定日志记录级别。例如："OFF", "INFO", "DEBUG", "TRACE"，默认值是null即不输出日志。通常读写分离将日志开启到INFO，单机将日志开到TRACE。

**日志输出：** 

loggerFile = 日志文件名字
  **指定日志信息保存文件或者console 输出：**

    - 如果没有指定loggerFile，表示不生成JDBC日志文件,日志信息全部打印到当前console输出。

    - 如果loggerFile有指定路径，则只打印到文件。例如：loggerFile=e:\\logFile.txt，默认值是null。这个路径可以是相对路径，也可以是绝对路径。



JDBC 报错：无效的 "UTF8" 编码字节顺序
----------------------------------------------------------

适用版本：V8R2

V82早期版本的JDBC默认都是UTF8编码的，需要设置client_Encoding=GBK来指定客户端编码。这个参数现在已经变更为clientEncoding

V82目前版本的JDBC 默认都是获取系统默认编码，自动设置为系统的clientEncoding，绝大多数情况下是不需要用户再自己指定这个参数的。
   


系统JVM和应用和JDBC和数据库编码之间的关系
----------------------------------------------------------

适用版本：V8R2

**乱码的问题通常都是编码不一致导致。**

**分析步骤**

第一 落实应用的编码是什么。需要询问应用的开发人员。

第二 落实JVM的file.encoding 是什么？一般Windows环境是GBK，linux是UTF8。

第三 如果应用的编码和JVM的file.encoding一致，JDBC默认使用JVM的编码，不需要额外指定clientEncoding参数。否则需要指定JVM的-Dfile.encoding=GBK或者JDBC的clientEncoding参数。

第四 如果还是报无效编码错误，就把JDBC日志打开到INFO或者TRACE，确认连接串信息对不对，再去看日志里是否有乱码数据。

**编码解释**

1. 系统JVM的默认编码：file.encoding 通常和操作系统默认编码一样。当然用户可以同过jvm参数-Dfile.encoding=UTF8 来手动指定期望的编码格式。JDK1.7及以上的可以通过命令java -XshowSettings:properties –version 产看jvm参数值。

2. 应用的编码：应用开发的时候自己指定的编码格式。通常应用的编码是要和运行环境的jvm的file.encoding保持一致。

3. JDBC的编码：JDBC通过参数clientEncoding指定编码格式，包括JDBC发给数据库的内容和返回给应用的内容都是按clientEncoding编码。通常需要和应用的编码保持一致。

4. 数据库的编码：

  - client_encoding 就是客户端编码，JDBC通过clientEncoding指定。
  - server_encoding 就是服务端编码，这个是数据库自身存储时的编码。


V7 V8 JDBC 混用问题
----------------------------------------------------------

适用版本：V8R2

V8的JDBC 连接 V7的数据库出现的错误:

  com.kingbase8.util.KSQLException: FATAL: 3 在参数 "extra_float_digits" (-15 .. 2)的有效范围之外

V7的JDBC 连接 V8的数据库出现的错误：

  [KingbaseES JDBC Driver]不能与数据库建立连接: 不支持的前端协议 3.3: 服务端支持 1.0 到 3.0。


JDBC读写分离模式混淆找不到表
----------------------------------------------------------

适用版本：V8R2

如果是开启读写分离的，可能是开启了JDBC连接池，目前JDBC连接池只支持相同的URL相同用户的连接，不支持多用户名。

解决办法关闭JDBC连接池指定连接参数 USECONNECT_POOL=false 即可



JDBC读写分离日志分析办法
----------------------------------------------------------

适用版本：V8R2

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

   [2019-08-08 11:17:29] [114] [com.kingbase8.dispatcher.executor.DispatchAbstractStatement-->executeTemplet] DispatchPreparedStatementV2.executeQuery(select pk_value ,CTID,XMIN from ecms_gen_pk where pk_name = 'pk_web_url_access_log' for update;) consume time:::17(ms)

3. 比如我要看 monitor线程的日志

从全日志里搜  monitor找到对应的线程ID比如是[32]

.. code::

   grep "\[32\]" ./jdbc_new.log > 32.log

这样就能看到monitor不停的刷在线的主备机的IP，这样基本就能看到集群的历史和现在的状态，主备机都是谁。

4. 比如我要看是哪条SQL把事务设置为写事务了，从而不再分发备机。

从日志里搜”Enter transactional state from sql”，后面的SQL就是被识别为写语句的SQL。

例子：

.. code::

   [2019-08-08 11:17:29] [114] [com.kingbase8.dispatcher.sqlParser.sql.SqlParser-->parse] Enter transactional state from sql[select pk_value from ecms_gen_pk where pk_name = 'pk_web_url_access_log' for update].


5. 比如我要看应用建一个新的JDBC连接的时间消耗

从日志里搜“this connect consume time”，这个会显示建一个连接的时间消耗。

例子：

.. code::

   [2019-08-08 11:25:16] [302] [com.kingbase8.Driver-->makeConnection] this connect consume time:::135(ms)

6. 比如我要看看都发生了什么错误

从日志里搜“Exception”，就能看到所有的异常信息。

例子：

.. code::

   [2019-08-08 11:21:29] [302] [com.kingbase8.Driver-->connect] Unexpected connection error: java.sql.SQLException: JDBC can't find a vaild master database in cluster...



JDBC使用SSL加密
----------------------------------------------------------

适用版本：V8R2

**1. 使用LibPQFactory**

**服务器：**

  1)确保安装openssl

  2)在data目录下，创建自签名的证书

    为服务器创建一个快速的自签名的证书，填充那些openssl要求的信息。确保把本地主机名当做"Common Name"输入；挑战密码可以留空。该程序将生成一个用口令保护的密钥，它不会接受小于四字符的口令。

    .. code::

      openssl req -new -text -out server.req

    要移去密钥（如果你想自动启动服务器就必须这样），运行下面的命令：

    .. code::

      openssl rsa -in privkey.pem -out server.key
      rm privkey.pem

    将一个证书变成自签名的证书并复制密钥和证书到服务器将要查找它们的地方

    .. code::

      openssl req -x509 -days 3650 -in server.req -text -key server.key -out server.crt
      
      修改文件权限，如果文件的权限比这个更自由，服务器将拒绝该文件。

    .. code::

      chmod og-rwx server.key

    生成根证书

    .. code::

      cp server.crt root.crt

  3)配置kingbase.conf文件

    .. code::

      ssl = on                                 # (change requires restart)
      #ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL' # allowed SSL ciphers
                                                     # (change requires restart)
      #ssl_prefer_server_ciphers = on              # (change requires restart)
      #ssl_ecdh_curve = 'prime256v1'               # (change requires restart)
      #ssl_cert_file = 'server.crt'               # (change requires restart)
      #ssl_key_file = 'server.key'                # (change requires restart)
      ssl_ca_file = ' root.crt '                       # (change requires restart)
      #ssl_crl_file = ''                           # (change requires restart)


  4)配置sys_hba.conf文件

    .. code::

       hostssl    all             all             0.0.0.0/0               md5  clientcert=1

  5)重启数据库服务器

  6)为客户端创建所需证书

    生成kingbase8.key

    .. code::

      openssl genrsa -des3 -out kingbase8.key 1024
      openssl rsa -in kingbase8.key -out kingbase8.key
      chmod 400 kingbase8.key
      
    生成kingbase8.csr，CN需要指定为要连接数据库的用户名，如需匹配不同的用户，可指定为*
      
    .. code::

      openssl req -new -key kingbase8.key -out kingbase8.csr -subj '/C=GB/ST=Berkshire/L=Newbury/O=Kingbase/CN=SYSTEM'
      
    生成kingbase8.crt
     
    .. code::

      openssl x509 -req -days 3650 -in kingbase8.csr -CA root.crt -CAkey server.key -out kingbase8.crt -CAcreateserial
      
    生成kingbase8.pk8

    .. code::

      openssl pkcs8 -topk8 -outform DER -in kingbase8.key -out kingbase8.pk8 -nocrypt


**jdbc：**

  通过参数sslmode配置证书验证方式，该参数支持四个值：disable（禁用SSL）、require、verify-ca、verify-full。使用verify-ca和verify-full时，需通过连接参数sslrootcert指定根证书文件的位置，如不指定，Linux默认路径为$HOME/.kingbase8/root.crt，Windows默认路径为%APPDATA%\kingbase8\root.crt，将服务器data目录下的root.crt放到对应目录下即可。只有verify-full模式会对主机名进行验证。

  通过参数sslcert配置客户端证书位置，如不指定，Linux默认路径为$HOME/.kingbase8/kingbase8.crt，Windows默认路径为%APPDATA%\kingbase8\kingbase8.crt，将服务器data目录下的kingbase8.crt放到对应目录下即可。

  通过参数sslkey配置秘钥文件位置，如不指定，Linux默认路径为$HOME/.kingbase8/kingbase8.pk8，Windows默认路径为%APPDATA%\kingbase8\kingbase8.pk8，将服务器data目录下的kingbase8.pk8放到对应目录下即可。

  举例：

  .. code::

     jdbc:kingbase8://192.168.222.128:54321/TEST?sslmode=verify-ca&sslrootcert=root.crt&sslcert=kingbase8.crt&sslkey=kingbase8.pk8


**2. 使用默认的SSLSocketFactory**

**服务器：**

  1)、2)、3)、4)、5)见上

  6)创建truststore，用于认证服务器端证书

    把服务器证书转化为der格式

    .. code::

      openssl x509 -in server.crt -out server.crt.der -outform der

    创建truststore，装入服务器证书

    .. code::

      keytool -keystore ./truststore -alias kingbase8server -import -file ./server.crt.der


  7)创建keystore，保存客户端证书

    生成客户端的keyPair

    .. code::

      keytool -genkeypair -dname "cn=kingbase8client, ou=basesoft, o=basesoft, c=CN" -alias kingbase8client -keystore ./keystore -validity 180

    生成证书请求

    .. code::

      keytool -certreq -alias kingbase8client -file ./kingbase8client.csr -keystore ./keystore 


    用root.crt签发客户端证书

    .. code::

      openssl x509 -sha1 -req -in ./kingbase8client.csr -CA ./root.crt -CAkey ./server.key -CAcreateserial -out ./kingbase8client.crt.der -outform DER -days 365 -passin pass:123456 -extfile /etc/pki/tls/openssl.cnf -extensions v3_req


    把证书添加到keystore中

    .. code::

      keytool -keystore ./keystore -alias kingbase8server -import -file ./server.crt.der
      keytool -keystore ./keystore -alias kingbase8client -import -file ./kingbase8client.crt.der

**jdbc：**

  1)只需配置连接参数ssl=true；

  2)将truststore和keystore拷贝到客户端；

  3)执行程序时指定java运行参数

  .. code::

    -Djavax.net.ssl.trustStore=truststore -Djavax.net.ssl.trustStorePassword=123456
    -Djavax.net.ssl.keyStore=keystore -Djavax.net.ssl.keyStorePassword=123456


  .. note::

    1. 生成keystore时，签发客户端证书命令，可能会对openssl的版本有一定的要求，自测使用版本为OpenSSL 1.0.1e-fips，可以通过命令openssl version查看openssl版本。

    2. 如果需要不与主机名和用户名绑定，使用LibPQFactory方式，需要配置jdbc连接参数sslmode为verify-ca，指定该参数不会验证主机名，生成kingbase8.csr时，CN指定为*，可匹配不同的用户。使用SSLSocketFactory不验证主机名和用户名。

    3. 使用java命令执行应用程序时，可以通过-cp或-Djava.ext.dirs指定jar包路径。但通过后者指定时，会覆盖Java本身的ext设置，如果未指定该系统属性的原加载路径，将失去一些功能，如java自带的加解密算法实现，会报NOSuchAlgorithmException的错误。故需同时在该设置下指定路径$JAVA_HOME/jre/lib/ext，如-Djava.ext.dirs=./plugin: $JAVA_HOME/jre/lib/ex。

  4)如果openssl版本太高，使用其生成的证书服务器可能会报"unknown message digest algorithm"错误，此时需将openssl.cnf配置加密算法改为sha1，并且通过环境变量OPENSSL_CONF指定该文件的位置。

    openssl version      查看openssl的版本
    openssl version -d   查看openssl.cnf所在目录



JDBC常见异常
----------------------------------------------------------

适用版本：V8R2

1. com.kingbase8.util.KSQLException:The column index is out of range: 1, number of columns: 0. 

  该异常报错原因是sql无需绑定参数（如空sql:””），然后进行了参数绑定，请客户自己排查原因。

2. Bad version number in .class file(unable to load class com.kingbase8.Driver)

  异常原因为jdk的版本小于jdbc驱动包编译的版本，提升jdk版本或使用与jdk版本对应的jar包。

3. java.lang.NoClassDefFoundError或java.lang.ClassNotFoundException

  这两个异常都是找不到类，通常是缺少jar包，百度下该类在什么包里，导入对应jar包即可。

  查看是否导入jar包：

  **工具idea**：

  1）点击File –> Project Structure；

  2）找到Modules，选中项目，点击Dependencies；

  3）如果缺少，点击右侧+号即可导入。

  .. figure:: images/jdbc-1.png

  **工具eclipse：**

  1）点击项目，右键，选中Build Path，Configure Build Path，在Libraries中查看所有导入的包。缺少可通过Add JARs导入。

  .. figure:: images/jdbc-2.png

  2）直接展开项目，也可以查看，如未导入，直接选中未导入的jar包，右键，Build Path，Add to Build Path。

  .. figure:: images/jdbc-3.png

4. This connection has been closed.

  该异常是因为使用了已关闭的连接，该连接可能由客户端关闭，也可能是jdbc遇到了I/O异常时，关闭当前连接。应用程序未处理I/O异常，直接使用该连接，就会导致该异常。

5. I/O异常( An I/O e rror occurred while sending to the backend.)

  通常是由网络原因导致的，也有可能是超时导致或者磁盘满了。如果是单条语句报I/O异常，通常是语句超时导致，语句超时指的就是语句执行时间超过了socketTimeout设置的时间。如果多条语句报错，那就是其他两个原因。

  也有可能是绑定的从参数个数超过了SQL的参数限制（Short.MAX_VALUE:32767)。（java.io.IOException:Tried to send an out-of-range integer as a 2-byte value:）

  如果是在流写入的过程中遇到该异常，也可能是创建临时文件失败。写入的流如果大于50k，就会在默认临时文件目录（java.io.tmpdir的值)中创建一个文件来缓存内容，中间出现IO异常，也会抛出该错误信息。

  以上错误可以通过错误堆栈来区分。


6. 替换jar包未生效问题

  原因是之前的jar包未删除。排查方法：可以删除新导入的jar包，看项目是否可以正常运行，如果可以正常运行，说明还存在其他jar包，删掉之前的jar包，再导入新的jar包。找不到其他的jar包可能原因是用户修改了驱动包名称或者驱动包被打在了其他jar包里。

7. 连接错误分析

  1）java.net.SocketTimeoutException:connect time out

  该错误表示底层的socket连接在10s内（connectTimeout默认值为10s）建立失败，此时客户端与服务器之间网络不通。

  2）com.kingbase8.util.KSQLException: Connection to 192.168.19.128:5432 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
  Caused by: java.net.ConnectException: Connection refused: connect

  该错误表示设置的端口无法连接，可能是数据库未开启或者端口填写错误。

  3）The authentication type 10 is not supported. Check that you have configured the sys_hba.conf file to include the client's IP address or subnet, and that it is using an authentication scheme supported by the driver.

  该错误是R3的驱动连接了R6的数据库。原因是R3的驱动不支持sha256验证，R6数据库默认就是sha256验证方式。

  4）SCRAM authentication is not supported by this driver. You need JDK >= 8 and pgjdbc >= 42.2.0 (not \".jre\" versions)

  R6 jdk1.6版本的驱动不支持sha256验证，需要使用md5验证方式。首先需要修改sys_hba.conf中的验证方式为md5，然后需要创建一个md5加密的用户。show password_encryption查看密码加密方式，不是md5的话需要修改加密方式为md5再创建用户。创建好后可以使用SELECT rolname,rolpassword FROM pg_authid;查看用户名和密码。

  5）FATAL:invalid value for parameter "client_encoding":XXX

  该错误是指服务器不支持XXX客户端编码。JDBC驱动连接数据库时默认设置的客户端编码是JVM的编码，如果该编码服务器不支持就会报上述错误。可以通过修改JVM编码或者通过设置JDBC连接参数clientEncoding来解决。

8. 无法确定参数$1的类型

  使用$1::type或cast函数对参数进行类型强转。使用Hibernate通常用cast函数，否则无法通过hibernate的语句解析。




JDBC读取BLOB乱码
----------------------------------------------------------

适用版本：V8R2

BLOB存储的内容为二进制，不会出现乱码。

1.如果打印内容为com.kingbase8.jdbc.KbBlob@14ae5a5，这个是Blob的对象名称，需要调用Blob的getBytes等方法，把Blob的存储内容拿出来，具体的参考手册示例。

2.如果打印内容为\x开头的十六进制字符串，和ksql查询出的内容一样，或者转字符串的时候使用了其他编码，打印出来的也可能是乱码，此时可以直接比较byte数组的大小，如果取出来的结果的数组是写之前的2倍加2的大小，那么需要更换新驱动或者在连接串指定连接参数prepareThreshold=-1。
如果不是以上两种情况，那就是写之前就已经转成了乱码，直接把待写入的byte数组转成字符串看是否是乱码。


读写分离分发现象分析
----------------------------------------------------------

适用版本：V8R2

问题描述1：集群状态正常，主机负载率也不是100，但是查询语句全部分发主机。

问题分析：原因可能为连接数据库的用户的权限小于流复制的权限，导致JDBC检测线程查不到在线备机，所有语句全部分发主机。是否该原因可通过工具或者ksql使用相同用户连接相同数据库，执行select CLIENT_ADDR from sys_stat_replication;看是否可以查询到备机。

解决办法：使用超级用户


问题描述2：读语句发往同一台备机

问题分析：使用同一个Statement执行的读语句都会发往同一台备机，原因是Statement的底层实际是有一个主Statement和一个备Statement，如果备Statement不为空时，不会去重新获取新的Statement，会一直使用同一个。如果想将语句进行分发，就建立新的Statement来执行语句。使用PreparedStatement/CallableStatement定义语句后，反复使用execute执行，多次执行都是发往同一台机器。



com.kingbase8.util.KSQLException: ERROR: type "q" does not exist（R6）
----------------------------------------------------------

适用版本：V8R2

问题分析：该问题是由于服务器开启了空串转为null参数（ora_input_emptystr_isnull=true），开启该参数后，原先为空串可以用q'<>'表示，但是有些版本驱动已经修改，服务器未修改，所以会有该问题。

解决办法：通过升级服务器版本或者关闭空串转为null参数（ora_input_emptystr_isnull=false）来解决。


fetchsize功能
----------------------------------------------------------


V8R3：使用参数defaultRowFetchSize指定返回行数即可。

V8R6：自动提交模式下，使用参数defaultRowFetchSize指定返回行数即可。

非自动提交模式下，使用参数defaultRowFetchSize指定返回行数，同时指定连接参数     useFetchSizeInAutoCommit=true。同时还需将服务器的GUC参数enable_autocommit_crossquery和enable_autocommit_fetch置为true。


同时使用R3和R6，jar包冲突的解决方案
----------------------------------------------------------


V8R6使用别名包，驱动名称为com.kingbase86.Driver。连接串示例：jdbc:kingbase86://localhost:54321/test



如何查看jar包的版本号？
----------------------------------------------------------

.. code::

   java -jar kingbase8-8.6.0.jar -version
