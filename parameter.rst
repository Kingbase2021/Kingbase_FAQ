参数相关
======================


Kingbase.conf 与 kingbase.auto.conf 参数文件
------------------------------------------------------

适用版本：V8R3 , V8R6

问题描述：这两个参数文件的读取先后、优先级

问题解答：

   1) 对于kingbase.conf 与 kingbase.auto.conf文件，如果有相同条目，则以\ kingbase.auto.conf文件参数值为准（忽略 kingbase.conf 相同条目）。

   2) 读取先后顺序：数据库启动时先读取 kingbase.conf，再读取kingbase.auto.conf，如果二者相同条目，会忽略kingbase.conf文件的相同条目。

   3) 所有文件读取完成后，才apply参数，由于kingbase.conf参数读取在前，kingbase.auto.conf读取在后，对于有先后顺序要求的参数必须注意。

举例如下：

   kingbase.conf 文件有 error_user_connect_times and max_error_user_connect_times这两个参数，但是用户又运行了alter system setmax_error_user_connect_times，相当于在kingbase.auto.conf文件增加了max_error_user_connect_times条目。当系统启动时，先读取kingbase.conf文件，再读取kingbase.auto.conf文件，由于kingbase.auto.conf文件也有max_error_user_connect_times条目，就会忽略kingbase.conf文件中的同样条目。而apply的顺序是按读取先后进行的，当apply error_user_connect_times （假设100）参数时，由于还没apply max_error_user_connect_times（在kingbase.auto.conf）参数 ，认为 max_error_user_connect_times 值为默认的 5 ，导致报错。



不同参数如何生效
--------------------------------------------


适用版本：V8R3 , V8R6

问题描述：为什么有些参数reload就可以生效，而有些参数必须重启数据库？

问题解析：

   修改参数后，如何生效是由pg_settings.context值决定的。具体如下：

   - internal：这些参数是在编译或initdb时设定的，不能修改。如：block_size， database_mode

   - kingbase: 修改这些参数要求重启数据库。如：archive_mode

   - sighup: 不需要重启数据库，只需reload就可生效。Kingbase会把sighup传递给子进程，通知子进程重新读取配置。如：archive_command

   - backend: 不需要重启数据库，只需reload就可生效，但只影响后续启动的会话。如：log_connections

   - user: 表示可以在会话中用 set 命令设置。如：bytea_output



error_user_connect_times and max_error_user_connect_times 
-----------------------------------------------------------

适用版本：V8R3 , V8R6

问题描述：为什么数据库启动报错：\ *100000 is outsize the max valid range for parameter "max_error_user_connect_times" 5*\ ，而实际的\ *max_error_user_connect_times*\ 参数值并不是5

问题解答：这两个参数要求先后顺序，max_error_user_connect_times参数必须放于error_user_connect_times
前面，否则会默认为max_error_user_connect_times是5 ，报错。



Exclude_reserved_words 排除关键字
--------------------------------------------

适用版本：V8R3 , V8R6

问题描述：客户设置Exclude_reserved_words=’level’，导致show transaction isolation level 语法错误。

问题分析：关键字可配置功能实际实现：将原来的关键字配置为非关键字，词法解析到该字符串时，不再将其识别为关键字，而认为是一个普通的字符串。该功能风险点：排除该关键字，那么语法规则中涉及到该关键字的语法规则都将失效，甚至出现莫名的错误（以为是关键字，结果识别为字符串，导致语法对应错误，识别为其他语义）。本例中配置了level，导致涉及level的语法失效。



max_locks_per_transaction设置过大引发数据库启动问题
---------------------------------------------------------

适用版本：V8R3 , V8R6

问题描述：数据库无法启动，报无法分配内存

问题解析：

   - max_locks_per_transaction：这个参数控制每个事务能够得到的平均的对象锁的个数，默认值是64。数据库在启动以后创建的共享锁表最大可以保存max_locks_per_transaction * (max_connections + max_prepared_transactions)个对象锁。每个锁空间需预留270个字节的共享内存。单个事务可以同时获得的对象锁的数目可以超过max_locks_per_transaction的值，只要共享锁表中还有剩余空间。

   - max_connections(integer)：这个参数只有在启动数据库时，才能被设置。它决定数据库可以同时建立的最大的客户端连接的数目。默认值是100。每个连接占用 400字节共享内存。
     
     .. note::

       Increasing max_connections costs ~400 bytes of shared memory per connection slot, plus lock space (see max_locks_per_transaction).

   - 用户将 max_locks_per_transaction值设置 为 215927809，导致系统启动时要求分配  215927809 * 270 * 1000（max_connections）= 54TB的内存空间，数据库启动失败


max_identifier_length
--------------------------------------------

适用版本：V8R3 , V8R6

问题描述：对象名称能否超过63字符？

问题解答：参数 max_identifier_length决定最大的对象名称长度，该参数只能在编译时指定，不能修改。默认是63。对于汉字表名，根据编码的不同，一个汉字占2-3字符。


数据库启动失败，报“内存段超过可用内存”
--------------------------------------------

适用版本：所有版本

问题描述：

   数据库启动报内存不足，错误信息如下：

   .. figure:: images/FAQ20071.png
      :width: 553px
      :height: 84px

原因分析：

   - 原因1：实际物理内存不够

   .. figure:: images/FAQ20092.png
      :width: 460px
      :height: 44px

   - 原因2：swap 与 shared_buffers 相差过大，如以上例子，Swap才配置2G，而Shared_buffers 16G

   - 原因3：系统参数设置过小

   .. figure:: images/FAQ20175.png
      :width: 421px
      :height: 36px

   .. figure:: images/FAQ20177.png
      :width: 267px
      :height: 177px

   - 原因4：启用了大页，但是大页内存却不够。数据库参数huge_pages = on，表示数据库启动时只能用大页。如果操作系统大页内存设置过小，数据库就无法启动

   .. figure:: images/FAQ20260.png
      :width: 312px
      :height: 64px

   - 原因5：数据库参数设置不合理。除了内存相关的参数，如shared_buffers外，还有其他参数也会要求内存段：max_connections, max_prepared_transactions都会影响内存段的分配。还有 max_locks_per_transaction参数，每个需要270字节的内存。

 