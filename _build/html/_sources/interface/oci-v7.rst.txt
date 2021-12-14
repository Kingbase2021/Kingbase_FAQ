V7 OCI常见问题
==============================


OCI读写分离配置
-----------------------------------------

.. code::

   #打开读写分离功能，该配置项时读写分离功能的前提，必须开启后续的配置项才有意义；若未开启，则host配置项只使用第一个地址
   UseDispatch=1
   #服务器地址（包括主机和备机，用“|”分割）
   HOST=192.168.28.21|192.168.28.20
   #主机读负载率，默认为0
   HOSTLOADRATE=50
   #发送语句失败后的重试次数，默认为5次
   RETRYTIMES=10
   #发送语句失败后的重试等待时间，单位为秒，默认5秒
   RETRYINTERVAL=5
   #监控线程的检查等待时间，单位为秒，默认5秒
   MONITORINTERVAL=5
     #写函数列表，调用该函数的sql语句将发送至主机（用“;”分割）
   BlackList=setData;setValue;removeData

在支持读写分离的驱动版本中，useHA功能已经被弃用，后续也不再支持。


OCI日志分析
-----------------------------------------

常用的OCI日志的命令：

1. 比如我要看一个线程的日志，假如131 是线程ID，

.. code::

   grep "\[131\]" ./oci_new.log > 131.log

这样就能看到131线程的完整OCI日志，这样就能看到这个线程都干了什么事情，反推应用的业务逻辑。

2. 比如我要看 monitor线程的日志

从全日志里搜monitor找到对应的线程ID比如是[32]

.. code::

   grep "\[32\]" ./oci_new.log > 32.log

这样就能看到monitor不停的刷在线的主备机的IP，这样基本就能看到集群的历史和现在的状态，主备机都是谁。

3. 比如我要看是哪条SQL把事务设置为写事务了，从而不再分发备机。

从日志里搜”The statement switches to write transaction”，后面的SQL就是被识别为写语句的SQL。

例子：

.. code::

   [114][2019-07-19 21:04:04.1470]DEBUG3: The statement switches to write transaction: select pk_value from ecms_gen_pk where pk_name = 'pk_web_url_access_log' for update .

4. 查看sql语句预备发送至哪个服务器

在日志中搜索“Dispatch pickTheConnection,”，就能看到所有的语句预备发送至哪个服务器。

例子：

.. code::

   [6512][2019-08-22 20:46:55.1700]DEBUG3:      Dispatch pickTheConnection, select count(*) from sys_class send to 192.168.28.48


OCI日志配置说明
-----------------------------------------

1. sys_service.conf 文件中 DCILog 指定日志文件路径，DCILogLevel 指定日志级别, 如下：
   
.. code::

   DCILog=/tmp/oci.log
   DCILogLevel=DEBUG3

2.sys_service.conf 文件中第一次出现的 DCILog 和 DCILogLevel 才会生效，后续的配置不再读取。

比如 sys_service.conf 文件中有如下配置：

.. code::

      [KingbaseES_1]
      DCILog=/tmp/oci1.log
      DCILogLevel=DEBUG3

      [KingbaseES_2]
      DCILog=/tmp/oci2.log
      DCILogLevel=DEBUG1

则生效的是：

.. code::

      [KingbaseES_1]
      DCILog=/tmp/oci1.log
      DCILogLevel=DEBUG3

这是因为应用程序加载DCI驱动的时候，就会来读取 sys_service.conf 中的日志文件相关配置，  而此时还不知道应用程序使用的服务名。所以，以找到的第一个 DCILog 和 DCILogLevel 为准。


OCI配置文件如何配置
-----------------------------------------

首先设置环境变量：KINGBASE_CONFDIR指定sys_service.conf配置文件所在目录路径，如果是在windows下配置环境变量，需要重启应用程序，环境变量才能在环境变量中生效。

其次：配置文件信息如下

.. code::

   [KingbaseES_R3]
   dbname=TEST
   port=54322
   host=192.168.28.151
   Print=1
   DCILog=oci.log
   DCILogLevel=DEBUG1
   UseExtendedProtocol=1


OCI 和DCI的头文件可以混用吗？
-----------------------------------------

OCI的头文件是使用的oracle相关的头文件,DCI使用的是金仓提供的，一般提供驱动时会一起提供。