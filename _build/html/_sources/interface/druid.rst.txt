Druid 数据库连接池配置问题
====================================


Druid 配置国产金仓数据库
---------------------------------

需要配置driverClassName才能支持国产数据库

Druid 金仓V8数据源的配置例子：

.. code::

	jdbc.driverClassName=com.kingbase8.Driver 
	jdbc.url=jdbc:kingbase8://127.0.0.1:54321/test 
	jdbc.username=root 
	jdbc.password=1qaz!QAZ
	filters= stat,log4j   
	(filters常用种类：
	监控统计用的filter:stat
	日志用的filter:log4j
	防御sql注入的filter:wall目前不支持国产数据库)

.. note:

	1. java.sql.SQLException:unknown jdbc driver:jdbc:kingbase8://127.0.0.1:54321/test 
	没有配置driverClassName。
	2. java.lang.IllegalStateException: dbType not support : null, url jdbc:kingbase8://127.0.0.1:54321/xxx

配置了wall过滤器。配置了wall过滤器后，如果配置了dbType可以解决该异常，但是有些语句的语法Druid无法解析，会抛出其他的异常，所以不要配置wall。


Druid 配置例子
---------------------------------

.. code::

	 <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource" 
	  init-method="init" destroy-method="close"> 
	  <property name="driverClassName" value="${jdbc.driverClassName}" /> 
	  <property name="url" value="${jdbc.url}" /> 
	  <property name="username" value="${jdbc.username}" /> 
	  <property name="password" value="${jdbc.password}" /> 
	  <!-- 配置初始化大小、最小、最大 --> 
	  <property name="initialSize" value="10" /> 
	  <property name="minIdle" value="10" /> 
	  <property name="maxActive" value="100" />
	  <!-- 配置获取连接等待超时的时间 单位毫秒--> 
	  <property name="maxWait" value="10000" />
	  <!-- 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒 
	有两个含义:
	Destroy线程会检测连接的间隔时间;
	testWhileIdle的判断依据，详细看testWhileIdle属性的说明--> 
	  <property name="timeBetweenEvictionRunsMillis" value="60000" />
	  <!-- 配置一个连接在池中最小生存的时间，单位是毫秒
	Destory线程中如果检测到当前连接的最后活跃时间和当前时间的差值大于
	minEvictableIdleTimeMillis，则关闭当前连接 --> 
	  <property name="minEvictableIdleTimeMillis" value="18000000" />
	  <property name="testWhileIdle" value="true" />
	  <!-- 这里建议配置为TRUE，防止取到的连接不可用 --> 
	  <property name="testOnBorrow" value="true" /> 
	  <property name="testOnReturn" value="false" />
	  <!-- 这里配置提交方式，默认就是TRUE，可以不用配置 -->
	  <property name="defaultAutoCommit" value="true" />
	  <!-- 验证连接有效与否的SQL，不同的数据配置不同 --> 
	  <property name="validationQuery" value="select 1 " /> 
	  <property name="filters" value="stat" /> 
	 </bean>


Druid的连接强制回收
---------------------------------

.. code::

	<!-- 连接泄露检查，打开removeAbandoned功能 , 连接从连接池借出后，长时间不归还，将触发强制回连接。回收周期随timeBetweenEvictionRunsMillis进行，如果连接为从连接池借出状态，并且未执行任何sql，并且从借出时间起已超过removeAbandonedTimeout时间，则强制归还连接到连接池中。
	removeAbandoned是连接池的高级功能，理论上这中配置不应该出现在实际的生产环境，因为有时应用程序执行长事务，可能这种情况下，会被连接池误回收，该种配置一般在程序测试阶段，为了定位连接泄漏的具体代码位置，被开启。
	生产环境中连接的关闭应该靠程序自己保证 -->        
	<property name="removeAbandoned" value="false" />         
	<!-- 超时时间，秒 -->        
	<property name="removeAbandonedTimeout" value="80"/>        
	<!-- 关闭abanded连接时输出错误日志，这样出现连接泄露时可以通过错误日志定位忘记关闭连接的位置 -->        
	<property name="logAbandoned" value="true" />
