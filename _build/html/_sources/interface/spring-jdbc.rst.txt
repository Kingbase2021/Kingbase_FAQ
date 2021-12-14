Spring-JDBC 常见问题
=====================

大字段的设置--lobHandler
----------------------------

LobHandler 接口为操作 BLOB/CLOB 提供了统一访问接口，而不管底层数据库究竟是以大对象的方式还是以一般数据类型的方式进行操作。

大部分数据库厂商的 JDBC 驱动程序（如 DB2）都以 JDBC 标准的 API 操作 LOB 数据，但 Oracle 9i 及以前的 JDBC 驱动程序采用了自己的 API 操作 LOB 数据，Oracle 9i 直接使用自己的 API 操作 LOB 数据，且不允许通过 PreparedStatement 的setAsciiStream()、setBinaryStream()、setCharacterStream() 等方法填充流数据。Spring 提供 LobHandler 接口主要是为了迁就 Oracle 特立独行的作风。所以 Oracle 必须使用 OracleLobHandler 实现类，而其它的数据库统一使用 DefaultLobHandler 就可以了。Oracle 10g 改正了 Oracle 9i 这个异化的风格，所以 Oracle 10g 也可以使用 DefaultLobHandler。

**Oracle 数据库的 LobHandler 配置**

.. code::

	<bean id="oracleLobHandler" 
	class="org.springframework.jdbc.support.lob.OracleLobHandler" lazy-init="true">
	   <property name="nativeJdbcExtractor" ref="nativeJdbcExtractor"/>
	</bean>

**一般数据库 LobHandler 的配置**

.. code::

	<bean id="defaultLobHandler"
	 class="org.springframework.jdbc.support.lob.DefaultLobHandler" lazy-init="true"/>


org.springframework.data.jdbc.repository.config.DialectResolver$NoDialectException: Cannot determine a dialect for org.springframework.jdbc.core.JdbcTemplate@7c90b7b7. Please provide a Dialect.
------------------


堆栈信息：
  
  org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'jdbcConverter' defined in class path resource [org/springframework/boot/autoconfigure/data/jdbc/JdbcRepositoriesAutoConfiguration$SpringBootJdbcConfiguration.class]: Unsatisfied dependency expressed through method 'jdbcConverter' parameter 4; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'jdbcDialect' defined in class path resource [org/springframework/boot/autoconfigure/data/jdbc/JdbcRepositoriesAutoConfiguration$SpringBootJdbcConfiguration.class]: Bean instantiation via factory method failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [org.springframework.data.relational.core.dialect.Dialect]: Factory method 'jdbcDialect' threw exception; nested exception is org.springframework.data.jdbc.repository.config.DialectResolver$NoDialectException: Cannot determine a dialect for org.springframework.jdbc.core.JdbcTemplate@7c90b7b7. Please provide a Dialect.


解决办法：
  
  出现该问题是因为使用了spring-boot-starter-data-jdbc包，该包要求提供jdbcDialect，目前未适配，推荐使用spring-boot-starter-jdbc。