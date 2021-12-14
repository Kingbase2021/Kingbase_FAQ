Hibernate使用常见问题
==============================


Hibernate使用需要配置方言包
-----------------------------------


Hibernate的使用需要配置方言包，使用方言包的版本需要根据Hibernate核心包的版本来确定。Hibernate核心包通常由客户从网络下载，核心包的包名为hibernate-core-xxx.jar或hibernate-xxx.jar或hibernatex.jar。目前R2、R3提供以下版本的方言包。

	+-----------------------------------+------------+
	| 方言包                            | 适用范围   |
	+===================================+============+
	| hibernate-2.0.3dialect.jar        | [2.0,2.1） |
	+-----------------------------------+------------+
	| hibernate-3.1dialect.jar          | [3.1,3.2） |
	+-----------------------------------+------------+
	| hibernate-3.2.7gadialect.jar      | [3.2,3.3） |
	+-----------------------------------+------------+
	| hibernate-3.3dialect.jar          | [3.3,3.6） |
	+-----------------------------------+------------+
	| hibernate-3.6.10dialect.jar       | [3.6,4.0） |
	+-----------------------------------+------------+
	| hibernate-4.0.1finaldialect.jar   | [4.0,4.3） |
	+-----------------------------------+------------+
	| hibernate-4.3.11finaldialect.jar  | [4.3,5.0） |
	+-----------------------------------+------------+
	| hibernate-4.3.2finaldialect.jar   | [4.3,5.0） |
	+-----------------------------------+------------+
	| hibernate-5.0.12.Finaldialect.jar | [5.0,5.2） |
	+-----------------------------------+------------+
	| hibernate-5.2.17.Finaldialect.jar | [5.2,5.4） |
	+-----------------------------------+------------+
	| hibernate-5.4.6.Finaldialect.jar  | [5.4,6.0） |
	+-----------------------------------+------------+

V7的方言包类名都是KingbaseDialect，V82的方言包类名都是Kingbase8Dialect。请注意类名配置。

使用时注意配置是否填写正确

V7的hibernate 的dialect配置例子

.. code::

	<property name="dialect">org.hibernate.dialect.KingbaseDialect</property>  
	<property name="connection.driver_class">com.kingbase.Driver</property>   
	<property name="connection.url">jdbc:kingbase://192.168.87.128:5421/TEST</property>

V82的hibernate 的dialect配置例子

.. code::

	<property name="dialect">org.hibernate.dialect.Kingbase8Dialect</property>  
	<property name="connection.driver_class">com.kingbase8.Driver</property>   
	<property name="connection.url">jdbc:kingbase8://192.168.87.128:54333/TEST</property>  

在运行项目时如果遇到以下两种异常，均是因为项目未导入方言包：

	1.java.lang.ClassNotFoundException: Could not load requested class : org.hibernate.dialect.Kingbase8Dialect

	2.org.hibernate.boot.registry.selector.spi.StrategySelectionException: Unable to resolve name [org.hibernate.dialect.Kingbase8Dialect] as strategy [org.hibernate.dialect.Dialect]

目前遇到的情况有：

	1.未将方言包加入项目的classpath中；

	2.将核心包当成方言包导入。


V8 Hibernate非法long值问题
-----------------------------------


这个问题是由于V8 hibernate把TEXT类型默认对应到CLOB类型处理，但是CLOB是通过OID来访问的，所以造成类型转换报错。解决办法更换新的方言包，新的dialect。

方言包把TEXT类型默认对应到LONGVARCHAR就解决了。


Hibernate 无法确定参数类型$1
-----------------------------------

1. 使用cast函数对于不识别的类型进行强转，如cast(? as timestamp)，as后面的类型需要为hibernate类型，hibernate类型自行百度。

2. 对于V7，这个问题可能是用户打开了Hibernate的SQL注释功能，改为false即可。

.. code::

	<property name="use_sql_comments">false</property>

	parse JDBC_STATEMENT_7: /* from TestDb  where username=$1 */ select testdb0_.id as id0_, testdb0_.username as username0_, testdb0_.btest as btest0_ from hibernate_test testdb0_ where testdb0_.username=$2
	ERROR:  could not determine data type of parameter $1



Hibernate 错误: 字段的类型为 TEXT, 但表达式的类型为 BYTEA你需要重写或转换表达式
---------------------------------------------------------------------------------------------------------

问题分析：

	这个问题原因是JDBC指定了bytea的OID传给服务器，而服务器实际字段类型是TEXT，不支持类型转换。

	查看hibernate源码：

	.. code::

		public Query setParameter(int position, Object val) throws HibernateException    {
		      if (val == null) {
		         setParameter( position, val, Hibernate.SERIALIZABLE );
		      }
		}

	看出对于null值，hibernate都是按照Hibernate.SERIALIZABLE类型处理。而Hibernate.SERIALIZABLE类型使用Hibernate.BINARY.set(st, toBytes(value), index)。

	Hibernate.BINRAY底层使用JDBC的setBinaryStream或者setBytes绑定参数。

解决办法：

   JDBC直接修改所有Bind参数传bytea的地方都改成0。如仍需绑定为bytea，可通过连接参数bytestype=bytea来指定。


Hibernate控制输出真实SQL日志
-----------------------------------

编辑hibernate.cfg.xml，配置方法：

1. 参数：show_sql=true 打印SQL语句；

2. 参数：format_sql=true 使SQL语句格式更加美观统一；

3. 参数：use_sql_comments=true 使SQL语句中自动注入注释，增加可读性。

.. code::

	<property name="show_sql">true</property>    //控制台打印SQL语句
	<property name="format_sql">true</property>  //格式化SQL语句
	<property name="use_sql_comments">true</property>  //指出是什么操作生成了该语句


Springboot JPA配置方言包问题
-----------------------------------


org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'entityManagerFactory' defined in class path resource
Caused by: org.hibernate.HibernateException: Access to DialectResolutionInfo cannot be null when 'hibernate.dialect' not set

Hibernate SQL方言没有设置导致的，在properties文件中增加下面这行：

  spring.jpa.database-platform=org.hibernate.dialect.Kingbase8Dialect或者spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.Kingbase8Dialect


hibernate-spatial方言包配置
-----------------------------------

hibernate-spatial是hibernate的数据空间插件，该方言包只在pg兼容版提供，依赖于hibernate方言包，目前只有5.3.7一个版本，使用该方言只需要将原先配置的hibernate方言的名称改为org.hibernate.spatial.dialect.kingbase.PostgisDialect即可，其他参见hibernate配置。如：

.. code::

   <property name="dialect">org.hibernate.spatial.dialect.kingbase.PostgisDialect</property>


hibernate使用numeric或char(1)映射java的boolean
-----------------------------------

当java类型为boolean，数据库字段类型为char(1)或numeric类型时，需将映射类型设置为org.hibernate.type.NumericBooleanType，例如：

.. code::

	<property name="sex" type="org.hibernate.type.NumericBooleanType">
	         <column name="sex"/>
	</property>

否则，映射为char(1)的时候会报“对于字符类型来说这个值太长了(1)”的错误，映射为numeric时且当该字段作为查询条件时，会在查询的时候无结果，原因是jdbc实际绑定的参数都是0和1，但oid类型为boolean，所以数据库查询时会自动推断类型，参数值被推断为f和t，但实际存储的是0和1，导致查询无结果。

这个问题在后续已修复，可直接更换新的驱动包。但是对于类似于from Person p where p.sex=true;的bool作为查询条件参数写死的hql，还需导入扩展方言hibernate-dialect-extension.jar，方言包名称修改为：org.hibernate.dialect.Kingbase8ExtensionDialect。该方言包依赖原先的方言包。


The column name sequence_catalog was not found in this ResultSet.
-----------------------------------------------------------------

Hibernate查询sequence的语句从5.4开始发生了改变，该错误需替换对应版本的方言包，目前我们提供了5.4.6版本的方言包，使用5.4版本以上的核心包，使用5.4.6的方言包。


主键自增策略hilo
-----------------------------------

使用hilo策略，默认的表hibernate_unique_key需要自己建立，而且必须拥有默认的字段next_hi，建表后，需要插入一条数据作为起始值。

.. code::

	create table hibernate_unique_key (next_hi integer not null);
	insert into hibernate_unique_key (next_hi) values(1);



Method com.kingbase8.jdbc.KbPreparedStatement.setCharacterStream(int, Reader, long) is not yet implemented.
-----------------------------------------------------------------------------------------------------------

该问题通常因为客户未使用ES的hibernate方言包，在使用了ES的hibernate方言包时，不会走到ES驱动未实现的方法中，解决方案就是配置ES的hibernate方言包。


Hibernate的hql不支持部分数据库函数的使用
----------------------------------------

1. 将hql语句转换为sql语句，createQuery使用的是hql，createSQLQuery使用的是sql语句；

2. 在方言包里注册函数解决。



Hibernate设置为update已经建好表，仍旧去建表
------------------------------------------

原因为使用了大小写不敏感的数据库，在大小写不敏感的库中，查询返回的表名与建表时的大小写保持一致。如果建表时使用小写，Hibernate查询返回的表名为小写，本地的表名是转为大写去比较，找不到所以会去建表，请改为大小写敏感的数据库。

**修改后可能存在的问题：**

1. 索引重复创建

  应用可能是从MySQL、SQLServer迁移过来的。索引名称在某些数据库中（如 MySQL、SQLServer），索引是以表为维度创建的，在不同的表中的索引是可以重名的； 而在另外的一些数据库中（如 PostgreSQL、Oracle、KingbaseES），索引是以数据库为维度创建的，即使是作用在不同表上的索引，它们也要求其名称的唯一性。所以需要修改索引名称。


java.lang.NoSuchMethodError: javax.persistence.Table.indexes()[Ljavax/persistence/Index;
----------------------------------------------------------------------------------------

jar包冲突，有多个jar包存在javax/persistence/Index类。


表取名user怎么规避？
-----------------------------------

在映射上@Table(name=“t_user")换个名字或者@Table(name="user",schema="xxx")显示指定模式名


其它模式下有同名表，导致当前模式没有表但未去建表
-----------------------------------------------

目前已知5.0.12这个版本的hibernate在查找表时，如果没有显示指定模式名，查询顺序为先查当前模式，没有查找默认模式，再没有就查找全模式，其他模式下有表，就会导致当前模式下创建失败，解决方法：1.在@Table显示指定schema；2.删除其他模式下的同名表；3.升级hibernate版本。