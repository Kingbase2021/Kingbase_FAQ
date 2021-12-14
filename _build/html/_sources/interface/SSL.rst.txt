.. _SSL认证常见问题:

SSL认证常见问题
===================


证书生成
--------------------

**服务器：**

1. 确保安装openssl

2. 在数据库data目录下，创建自签名的证书

   为服务器创建一个快速的自签名的证书，填充那些openssl要求的信息。确保把本地主机名当做"Common Name"输入；挑战密码可以留空。该程序将生成一个用口令保护的密钥，它不会接受小于四字符的口令。

   .. code::

      openssl req -new -text -out server.req

   要移去密钥（如果你想自动启动服务器就必须这样），运行下面的命令：

   .. code::

      openssl rsa -in privkey.pem -out server.key
      rm privkey.pem

   将一个证书变成自签名的证书并复制密钥和证书到服务器将要查找它们的地方

   .. code::

      openssl req -x509 -days 3650 -in server.req -text -key server.key -out server.crt

   修改文件权限，如果文件的权限比这个更自由，服务器将拒绝该文件。

   .. code::

      chmod og-rwx server.key

   生成根证书

   .. code::

      cp server.crt root.crt


3. 配置kingbase.conf文件

   打开文件 找到如下属性 放开注释并修改值

   .. code::

      ssl = on                                                  # (change requires restart)
      ssl_ca_file = ' root.crt '                       # (change requires restart)

4. 配置sys_hba.conf文件

   打开文件，修改ipv4连接host->hostssl, METHOD一栏增加clientcert=1，原有密码认证方式不变，如下所示

   .. code::

      # IPv4 local connections:
      hostssl    all             all             0.0.0.0/0               md5  clientcert=1


5.重启数据库服务器

6.为客户端创建所需证书

   生成kingbase8.key

   .. code::

      openssl genrsa -des3 -out kingbase8.key 1024
      openssl rsa -in kingbase8.key -out kingbase8.key
      chmod 400 kingbase8.key

   生成kingbase8.csr，CN需要指定为要连接数据库的用户名，如需匹配不同的用户，可指定为*

   .. code::

      openssl req -new -key kingbase8.key -out kingbase8.csr -subj '/C=GB/ST=Berkshire/L=Newbury/O=Kingbase/CN=SYSTEM'

   生成kingbase8.crt

   .. code::

      openssl x509 -req -days 3650 -in kingbase8.csr -CA root.crt -CAkey server.key -out kingbase8.crt -CAcreateserial

   JDBC额外步骤 其他请省略此步骤 私钥转pkcs格式

   生成kingbase8.pk8

   .. code::

      openssl pkcs8 -topk8 -outform DER -in kingbase8.key -out kingbase8.pk8 -nocrypt


证书配置
-----------------------


拷贝出客户端证书文件kingbase8.crt/kingbase8.key及root.crt放到客户端相应目录。
通过参数sslmode配置证书验证方式，该参数支持四个值：disable（禁用SSL）、require、verify-ca、verify-full。使用verify-ca和verify-full时，需配置证书位置，支持如下三种方式。

1. 默认路径。windows默认路径位置为%APPDATA%\kingbase\,linux下为~/.kingbase/，将客户端证书文件放入，系统会自动查找。只需指定"sslmode=verify-ca";

2. 环境变量。通过设置环境变量PGSSLROOTCERT、PGSSLCERT 、PGSSLKEY指定证书位置。连接参数同默认路径。

3. 绝对路径。通过设置sslrootcert、sslcert、sslkey参数指定。
使用verify-ca常常就可以提供足够的保护。只有verify-full模式会对主机名进行验证。

4. 绝对路径连接参数示例

gorm:

.. code::

   dsn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=verify-ca sslrootcert=C:\\Users\\GBJ-0256\\AppData\\Roaming\\kingbase8\\root.crt sslcert=C:\\Users\\GBJ-0256\\AppData\\Roaming\\kingbase8\\kingbase8.crt sslkey=C:\\Users\\GBJ-0256\\AppData\\Roaming\\kingbase8\\kingbase8.key",host, port, user, password, dbname)   

QT:

.. code::

   QString connOption="sslmode=verify-ca;sslrootcert=/home/wli/cert/root.crt;sslcert=/home/wli/cert/kingbase8.crt;sslkey=/home/wli/cert/kingbase8.key";
   conn.setConnectOptions(connOption); 


证书有效期
--------------------

.. figure:: images/ssl-1.png

openssl默认生成的证书有效期为30天，通过-days 参数指定证书有效时间，单位为天。
查看证书文件有效期

.. code::

   openssl x509 -in server.crt -noout -dates