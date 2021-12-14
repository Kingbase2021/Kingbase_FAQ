Mybatis 常见问题
========================


Mybatis设置SQL超时时间
-----------------------------

mybatis如果不指定,默认超时时间是不做限制的,默认值为0.

mybatis sql配置超时时间有两种方法:

**1. 全局配置**

    在mybatis配置文件的settings节点中,增加如下配置

    .. code::

        <settings>  
        <setting name="defaultStatementTimeout" value="25"/>  
        </settings> 

    以秒为单位的全局SQL超时时间设置,当超出了设置的超时时间时,会抛出SQLTimeoutException

**2. Mapper XML配置**

    在mapper xml文件中对具体一个sql进行设置,方法为在select/update/insert节点中配置timeout属性,超时时间并只作用于这一个sql.

    .. code::

        <insert  
          id="insert"  
          parameterType="com.test.abc.Person"  
          flushCache="true"  
          statementType="PREPARED"  
          keyProperty=""  
          keyColumn=""  
          useGeneratedKeys=""  
          timeout="10">



Mybatis非法long值问题
-----------------------------

1. 这个问题是由于V7的JDBC默认把TEXT类型对应为LONGVARCHAR，而Mybatis又把LONGVARCHAR类型默认按照CLOB对象处理，造成和Hibernate非法long值的情形类似，但是Mybatis没有提供方言机制，所以无法像Hibernate那样同过方言包控制，只能把V7的JDBC的TEXT类的值对应到Varchar来处理，就解决非法值问题。

2. 如果用新的JDBC还出此问题，说明用户自己把string类型的jdbcType手动设置为LONGVARCHAR了。解决办法：就是把jdbcType去掉或者设置为VARCAHR即可。




Mybatis 报错：字段的类型为 TEXT, 但表达式的类型为 BYTEA你需要重写或转换表达式
----------------------------------------------------------------------------

1. 这个问题需要查看出错SQL的mapper文件，需要知道mapper中参数是否指定了类型，从正常逻辑上来说不应该出现这样的转换，应该可通过调整参数类型解决。

2. 这个也可以从JDBC入手，把所有Bind参数设置Oid.BYTEA的全都改为0，让服务器自己推断类型。


Mybatis 控制JDBC底层不走预编译
-----------------------------


在mapper文件中可以使用statementType标记使用什么的对象操作SQL语句。 

statementType：标记操作SQL的对象 ，如statementType=”STATEMENT” 

要实现动态传入表名、列名，需要做如下修改，sql里的所有变量取值都改成${xxxx}，而不是#{xxx}

取值说明： 

    1. STATEMENT:直接操作sql，不进行预编译，获取数据：$—Statement 
    2. PREPARED:预处理，参数，进行预编译，获取数据：#—–PreparedStatement:默认 
    3. CALLABLE:执行存储过程————CallableStatement 


Mybatis 控制Bind参数
-----------------------------

#{}：相当于JDBC中的PreparedStatement，走Bind报文。

${}：是输出变量的值，字串替换，不走Bind。

简单说，#{}是经过预编译的，是安全的；${}是未经过预编译的，仅仅是取变量的值，是非安全的，存在SQL注入。


Mybatis 使用pagehelper插件
-----------------------------

Mybatis使用该插件需要将helperDialect设置成postgresql，如不指定，会报错：com.github.pagehelper.PageException：无法自动获取数据库类型，请通过helperDialect参数指定！

1. 直接使用Mybatis设置如下：
   
.. code::

        <plugins>
                   <!-- com.github.pagehelper为PageHelper类所在包名 -->
                   <plugin interceptor="com.github.pagehelper.PageInterceptor">
                            <property name="helperDialect" value="postgresql" />
                   </plugin>
        </plugins>


2. springboot整合mybatis使用如下：

在pom文件中引入Pagehelper分页插件：

.. code::

    <!-- 分页插件 -->
    <dependency>
        <groupId>com.github.pagehelper</groupId>
        <artifactId>pagehelper-spring-boot-starter</artifactId>
        <version>1.2.5</version>
    </dependency>

配置分页插件，打开application.properties，添加如下配置信息：

.. code::

    #分页插件
    pagehelper.helper-dialect=postgresql


Mybatis 使用自动返回主键功能
-----------------------------

该功能使用在V7仅支持insert语句

建表语句，要求表含有主键，且主键自增：

.. code::

   create table t_user (id int identity primary key,username text,password text,sex boolean);

在mapper文件里配置：

.. code::

    <!-- useGeneratedKeys：（仅对 insert 有用）这会告诉 MyBatis 使用 JDBC 的getGeneratedKeys方法来取出由数据内部生成的主键。默认值： false。 -->
    <!--keyProperty：（仅对 insert有用）标记一个属性， MyBatis 会通过 getGeneratedKeys或者通过 insert 语句的 selectKey 子元素设置它的值。默认：不设置。 -->

             <insert id="insertUser" useGeneratedKeys="true" keyProperty="id">
                       insert into t_user (username,password,sex) values
                       (#{username},#{password},#{sex})
             </insert>

.. note::

  如果使用tk-mybatis提供的mapper接口，V7需要mapper包的版本在3.4.0及以上，否则使用update相关的接口时，会报“不能返回generatedkeys或没有指定返回”的错误。


Mybatis配置databaseId
-----------------------------

.. code::

    <!--数据库厂商标示 -->
        <databaseIdProvider type="DB_VENDOR">
            <property name="KingbaseES" value="kingbase"/>
        </databaseIdProvider>

    <select id="getAllProduct" resultType="product" databaseId="kingbase">
            SELECT * FROM product3 
    </select>


Mybatis使用匿名块插入语句报错
-----------------------------


Mybatis中使用begin insert ...;insert...; end;格式的语句插入数据，报无法识别的GBK编码：'0x00'或者指定了连接参数prepareThreshold=-1报Can‘t change resolved type for param:1 from 1043 to 25.该问题属于plsql问题需要升级数据库版本。

在升级数据库版本后，如果出现类型转换错误，则使用强转（例如?::bytea）把其转换为对应类型，出现该错误的原因为匿名块无法识别oid绑定类型为0的参数，会将其默认识别为text，传给下层时无法转换为对应类型，就会报错。特别地，如果字段类型为二进制，如bytea、blob，如果参数内容有数据库无法识别的编码的话，转换成text就会报无法转换的编码错误，此时指定连接参数bytestype=bytea即可。


Mybatis使用ScriptRunner执行含plsql的sql脚本报错
-----------------------------------------------

1. ScriptRunner默认按照自定义的分隔符每行执行，分隔符默认为分号，如果sql脚本中包含plsql语句，按照分号分割出来的语句是不正确的，所以可以使用setDelimiter(String)来设置自定义的分隔符，如设置分隔符为"/"，则sql脚本中的每条语句后都添加"/"，ScriptRunner将会按照此对语句进行分割，连接KingbaseES时，普通语句之间无需使用分隔符，驱动会对普通语句进行分割；

2. 或者可以通过runner.setSendFullScript(true);设置将sql脚本一次发送，但是由于驱动不会对包含plsql的多语句进行分割，所以会报”无法插入多条命令到一个准备好的语句中“，此时指定jdbc连接参数preferQueryMode=simple走简单查询报文即可。



Mybatis使用游标的注册方式
-----------------------------

.. code::

    <select id="selectTempManualDataTest" statementType="CALLABLE">
            {#{out_return,mode=OUT,javaType=ResultSet,jdbcType=OTHER, resultMap=tempMap} = call proc_aaaaa() }
        </select>

.. note::

    1. jdbcType只能设置为OTHER，不能设置为CURSOR，Mybatis的CURSOR的值为-10，是OracleCURSOR的值，不是Types.REF_CURSOR的值，我们不支持；
    2. 如果没有设置javaType的类型，返回值的类型为ResultSet，如果设置了返回值的类型为ResultSet，则返回值为List对象。


Mybatis写json类型示例
-----------------------------

建表：

.. code::

   create table t_json(id serial,content json);

实体类：

.. code::

    package com.test.entity;

    public class JsonEntity {

       private int id;
       private Object fcontent;

        public  int getId() {
            return id;
        }
        public void setId( int id) {
            this.id =  id;
        }

        public  Object getContent() {
            return fcontent;
        }
        public void setContent(Object b) {
            this.fcontent =  b;
        }

        @Override  
        public String toString() {  
            return "id=" + this.id ;  
        }  
    }


**JsonTypeHandler.java**

.. code::

    package com.test.handler;

    import java.sql.CallableStatement;
    import java.sql.PreparedStatement;
    import java.sql.ResultSet;
    import java.sql.SQLException;

    import org.apache.ibatis.type.BaseTypeHandler;
    import org.apache.ibatis.type.JdbcType;

    import com.test.utils.JsonUtil;


    // 继承自BaseTypeHandler<Object> 使用Object是为了让JsonUtil可以处理任意类型
    public class JsonTypeHandler extends BaseTypeHandler<Object> {

        @Override
        public void setNonNullParameter(PreparedStatement ps, int i, Object parameter,
                JdbcType jdbcType) throws SQLException {

            ps.setString(i, JsonUtil.stringify(parameter));
        }

        @Override
        public Object getNullableResult(ResultSet rs, String columnName)
                throws SQLException {

            return JsonUtil.parse(rs.getString(columnName), Object.class);
        }

        @Override
        public Object getNullableResult(ResultSet rs, int columnIndex) throws SQLException {

            return JsonUtil.parse(rs.getString(columnIndex), Object.class);
        }

        @Override
        public Object getNullableResult(CallableStatement cs, int columnIndex)
                throws SQLException {

            return JsonUtil.parse(cs.getString(columnIndex), Object.class);
        }

    }


**JsonUtil.java**

.. code::

    package com.test.utils;


    import java.io.OutputStream;
    import java.text.SimpleDateFormat; 

    import org.apache.ibatis.logging.Log;
    import org.apache.ibatis.logging.LogFactory;
    import org.codehaus.jackson.map.DeserializationConfig;
    import org.codehaus.jackson.map.ObjectMapper;
    import org.codehaus.jackson.map.annotate.JsonFilter;
    import org.codehaus.jackson.map.ser.impl.SimpleBeanPropertyFilter;
    import org.codehaus.jackson.map.ser.impl.SimpleFilterProvider;
    import org.springframework.core.annotation.AnnotationUtils;
    import org.codehaus.jackson.map.SerializationConfig;

    public class JsonUtil {

        private static Log log = LogFactory.getLog(JsonUtil.class);

        private static ObjectMapper objectMapper = null;

        static {

            objectMapper = new ObjectMapper();

            objectMapper.setDateFormat(new SimpleDateFormat("yyyy-mm-dd"));
            objectMapper.disable(DeserializationConfig.Feature.FAIL_ON_UNKNOWN_PROPERTIES);
            objectMapper.configure(SerializationConfig.Feature.FAIL_ON_EMPTY_BEANS, false);
            objectMapper.setFilters(new SimpleFilterProvider().setFailOnUnknownId(false));
        }

        /*
        public static JsonUtil getInstance() {

            if (instance == null) {
                synchronized (JsonUtil.class) {
                    if (instance == null) {
                        instance = new JsonUtil();
                    }
                }
            }

            return instance;
        }
        */

        public static String stringify(Object object) {

            try {
                return objectMapper.writeValueAsString(object);
            } catch (Exception e) {
                log.error(e.getMessage(), e);
            }

            return null;
        }

        public static String stringify(Object object, String... properties) {

            try {
                return objectMapper
                        .writer(new SimpleFilterProvider().addFilter(AnnotationUtils.getValue(
                            AnnotationUtils.findAnnotation(object.getClass(), JsonFilter.class)).toString(), 
                                    SimpleBeanPropertyFilter.filterOutAllExcept(properties)))
                        .writeValueAsString(object);    
            } catch (Exception e) {
                log.error(e.getMessage(), e);
            }

            return null;
        }

        public static void stringify(OutputStream out, Object object) {

            try {
                objectMapper.writeValue(out, object);
            } catch (Exception e) {
                log.error(e.getMessage(), e);
            }
        }

        public static void stringify(OutputStream out, Object object, String... properties) {

            try {
                objectMapper.writer(new SimpleFilterProvider().addFilter(
                            AnnotationUtils.getValue(AnnotationUtils.findAnnotation(object.getClass(), JsonFilter.class)).toString(), 
                                SimpleBeanPropertyFilter.filterOutAllExcept(properties))).writeValue(out, object);    
            } catch (Exception e) {
                log.error(e.getMessage(), e);
            }
        }

        public static <T> T parse(String json, Class<T> clazz) {

            if (json == null || json.length() == 0) {
                return null;
            }

            try {
                return objectMapper.readValue(json, clazz);
            } catch (Exception e) {
                log.error(e.getMessage(), e);
            }

            return null;
        }

    }


映射文件：

.. code::

    <?xml version="1.0" encoding="UTF-8"?> 
    <!DOCTYPE mapper
    PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">    
    <mapper namespace="com.test.interfaces.MybatisDao">    


       <!-- json的相关SQL指令 -->
       <resultMap id="JsonTableMap" type="JsonEntity">
           <result column="id" property="id" />
           <result column="content" property="fcontent" typeHandler = "com.test.handler.JsonTypeHandler"/>
       </resultMap>

       <select id="selectJsonTableList" resultMap="JsonTableMap">
          select * from ${name}
       </select>
       <select id="selectJsonTableByID" resultMap="JsonTableMap">
          select * from t_json where id=#{id}
       </select>
        <insert id="insertJsonTable"> 
            insert into t_json (content) values ((#{fcontent, typeHandler=com.test.handler.JsonTypeHandler})::json)
        </insert>
        <update id="updateJsonTable" parameterType="JsonEntity" >
            update t_json set content=(#{fcontent, typeHandler=com.test.handler.JsonTypeHandler})::json where t_json.id=#{id}
        </update>
        <delete id="deleteJsonTable">
            delete from ${name}
        </delete>
    </mapper>   