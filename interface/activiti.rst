Activiti使用常见问题
======================


Activiti使用
-------------

Activiti使用报错：org.activiti.engine.ActivitiException: couldn't deduct database type from database product name 'KingbaseES'，是因为Activiti不支持国产数据库。适配KingbaseES，修改方式有两种：

1. 将Activiti参数databaseType配置为postgres。配置示例如下：

.. code::

  <bean id="processEngineConfiguration" class="org.activiti.engine.impl.cfg.StandaloneProcessEngineConfiguration">
          <property name="jdbcDriver" value="com.kingbase8.Driver"></property>
          <property name="jdbcUrl" value="jdbc:kingbase8://192.168.222.128:54321/TEST"></property>
          <property name="jdbcUsername" value="SYSTEM"></property>
          <property name="jdbcPassword" value="123456"></property>
          <!-- 没有表创建表 -->
          <property name="databaseSchemaUpdate" value="true"></property>
          <property name="databaseType" value="postgres"></property>
   </bean>

该方法会在第二次启动时出现自动建表表已存在问题（这是因为R3默认为大写，pg为小写），解决方案为在表建成功后，将参数databaseSchemaUpdate的值改为none。

.. code::

   <property name="databaseSchemaUpdate" value="none"></property>

SpringBoot整合Activiti时，无法直接配置databaseType参数，因为activiti-spring-boot-starter-basic里没有提供该参数。可以更换新的驱动包（官网的驱动包即可），然后配置连接参数productName=PostgreSQL，如：

.. code::

   jdbc:kingbase8://192.168.222.128:54321/TEST?productName=PostgreSQL

如果无法更换驱动包，则需要自行扩展配置。添加如下两个文件：


**ActivitiConfig.java**

.. code::

  package com.example.activiti.config;

  import java.io.IOException;

  import javax.sql.DataSource;

  import org.activiti.spring.SpringAsyncExecutor;
  import org.activiti.spring.SpringProcessEngineConfiguration;
  import org.activiti.spring.boot.AbstractProcessEngineAutoConfiguration;
  import org.activiti.spring.boot.ActivitiProperties;
  import org.activiti.spring.boot.JpaProcessEngineAutoConfiguration;
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.boot.autoconfigure.AutoConfigureAfter;
  import org.springframework.boot.autoconfigure.AutoConfigureBefore;
  import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
  import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
  import org.springframework.boot.context.properties.EnableConfigurationProperties;
  import org.springframework.context.annotation.Bean;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.jdbc.datasource.DataSourceTransactionManager;
  import org.springframework.transaction.PlatformTransactionManager;

  @Configuration
  @AutoConfigureAfter({ DataSourceAutoConfiguration.class })
  @AutoConfigureBefore({ JpaProcessEngineAutoConfiguration.class })
  public class ActivitiConfig {

     @Configuration
     @EnableConfigurationProperties({ ActivitiProperties.class })
     public static class ActivitiConfiguration extends AbstractProcessEngineAutoConfiguration {
        private ActivitiDatasourceProperties activitiDatasourceProperties;

        public ActivitiDatasourceProperties getActivitiDatasourceProperties() {
           return activitiDatasourceProperties;
        }

        @Autowired
        public void setActivitiDatasourceProperties(ActivitiDatasourceProperties activitiDatasourceProperties) {
           this.activitiDatasourceProperties = activitiDatasourceProperties;
        }

        @Bean
        @ConditionalOnMissingBean
        public PlatformTransactionManager transactionManager(DataSource dataSource) {
           return new DataSourceTransactionManager(dataSou-rce);
        }

        @Bean
        @ConditionalOnMissingBean
        public SpringProcessEngineConfiguration springProcessEngineConfiguration(DataSource dataSource,
              PlatformTransactionManager transactionManager, SpringAsyncExecutor springAsyncExecutor)
              throws IOException {
           SpringProcessEngineConfiguration config = baseSpringProcessEngineConfiguration(dataSource,
                 transactionManager, springAsyncExecutor);
           config.setDatabaseType(this.activitiDatasourceProperties.getDatabaseType());
           return config;
        }
     }
  }


**ActivitiDatasourceProperties.java**

.. code::

  package com.example.activiti.config;

  import org.springframework.boot.context.properties.ConfigurationProperties;
  import org.springframework.stereotype.Component;

  @ConfigurationProperties(prefix = "spring.activiti")
  @Component
  public class ActivitiDatasourceProperties {

     private String databaseType;

     public String getDatabaseType() {
        return databaseType;
     }

     public void setDatabaseType(String databaseType) {
        this.databaseType = databaseType;
     }

  }

**application.properties**

.. code::

  #数据库类型，必须配置
  spring.activiti.database-type=postgres
  #第一次执行配置为true，自动建表，之后执行改为none
  spring.activiti.database-schema-update=none

2. 替换activiti-engine.jar包，目前R2、R3支持5.10,5.14,5.20,5.21.0,6.0.0五个版本，使用该方式无需配置databaseType，也不会出现自动建表表已存在问题，但是支持版本较少，activiti各版本之间不通用，所以推荐使用第一种方式。