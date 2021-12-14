Maven 仓库使用常见问题
=============================

Maven本地仓库使用KingbaseES的JDBC驱动
-------------------------------------------

需要在本地仓库上方我们的JDBC驱动文件，注意目录结构

- GroupID是文件目录名字，每一个. 都是一级目录

- artifactId 是里面的目录名字

- version 是更里面的目录名字

- 最后文件名构成是  artifactId-version.jar

例如V82的JDBC驱动在pom.xml中配置如下：

.. code::

   <dependency>
         <groupId>com.kingbase8</groupId>
         <artifactId>kingbase8</artifactId>
         <version>8.2.0</version>
         <!-- scope>system</scope>
      <systemPath>${project.basedir}/lib/kingbase8-8.2.0.jar</systemPath-->
      </dependency>

V82的JDBC驱动对应的本地仓库目录：

.. code::

   E:\maven_repository_325\com\kingbase8\kingbase8\8.2.0\kingbase8-8.2.0.jar



Maven本地仓库使用KingbaseES的dialect方言包
-------------------------------------------

直接举例说明
   
例如Hibernate的4.3.2方言包在pom.xml中配置如下：

.. code::

   <dependency>
         <groupId>org.hibernate.dialect</groupId>
         <artifactId>hibernate</artifactId>
         <version>4.3.2finaldialect</version>
      </dependency>

Hibernate的4.3.2方言包对应的本地仓库目录：

.. code::

   E:\maven_repository_325\org\hibernate\dialect\hibernate\4.3.2finaldialect\hibernate-4.3.2finaldialect.jar