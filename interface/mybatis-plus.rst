Mybatis-plus常见问题
=============================


Mybatis-plus使用
-------------------------

Mybatis-plus适配KingbaseES，只使用基本功能，无需替换jar包，可正常使用。如需使用分页功能和代码生成器需替换jar包，目前提供了2.2.0和3.1.2两个版本。使用分页插件配置，需配置方言类型，类型为kingbasees，如：<property name="dialectType" value="kingbasees" />，其余正常使用即可，同时支持V7和V8。如只使用mybatis-plus的分页插件，也可不替换jar包，将dialectType配置为postgresql即可。

例如：

.. code::

	<property name="plugins">
	         <array>
	                   <!-- 分页插件配置 -->
	                   <bean id="paginationInterceptor"
	                                              class="com.baomidou.mybatisplus.plugins.PaginationInterceptor">
	                            <property name="dialectType" value="kingbasees" />
	                   </bean>
	         </array>
	</property>