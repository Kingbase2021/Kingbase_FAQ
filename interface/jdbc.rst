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

   .. image:: images/FAQ33958.png
      :width: 554px
      :height: 416px
 

KBBlob 迁移至Oracle
-----------------------------

适用版本：所有版本

问题描述：用户将BLOB从Kingbase迁移至Oracle，报错如下：“kblob cannot be cast to oracle.sql.blob”

问题分析：KBBlob 不支持迁移至Oracle Blob，只能是Oracle Blob迁移至KBBlob