DBCP连接池配置问题
========================

常用dbcp配置金仓V8数据库
-------------------------------

.. code::

	<bean id="dataSource_dbcp"
	      class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close"><!--设置为close使Spring容器关闭同时数据源能够正常关闭，以免造成连接泄露 -->
	      <property name="driverClassName" value="${jdbc.driver}" />
	      <property name="url" value="${jdbc.url}" />
	      <property name="username" value="${jdbc.username}" />
	      <property name="password" value="${jdbc.password}" />
	</bean>