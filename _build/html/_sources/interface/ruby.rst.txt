Ruby 常见问题
=====================


如何使用ruby-pg驱动连接至kingbaseES V8R3数据库
--------------------------------------------------------

分为修改驱动代码部分和表等数据库对象映射部分：

1. 修改驱动代码

进入驱动源码ext 目下下，修改/ext/pg_connection.c 871行代码,修改如下:

.. code::

    /*
                static VALUE pgconn_server_version(VALUE self)
                {
                         return INT2NUM(90600);
                }

                (备注：修改之后需要重新编译；使用修改之后如果还是报版本过低的问题，请检查是否       应用了修改过的驱动)
    */


2. 在用户用户模式下创建以下视图和函数

映射表视图如下：

.. code::

    create or replace view pg_type as select oid,* from sys_type;
    create or replace view pg_range as select * from sys_range;
    create or replace view pg_class as select oid,* from sys_class;
    create or replace view pg_namespace as select oid,* from sys_namespace;
           create or replace view pg_extension as select oid,* from sys_extension;
           create or replace view pg_constraint as select oid,* from sys_constraint;
           create or replace view pg_index as select * from sys_index; 


创建函数如下：

.. code::

    create or replace function pg_try_advisory_lock(key bigint)returns boolean 
           as $$
           declare
           begin
           return sys_try_advisory_lock($1);
           end;
           $$language plsql;

           create or replace function pg_try_advisory_lock(key1 int,key2 int)returns boolean 
           as $$
           declare
    begin
     return sys_try_advisory_lock($1,$2);
    end;
    $$language plsql;
    create or replace view pg_attribute as select * from sys_attribute;
    create or replace function pg_get_expr(v1 sys_node_tree,v2  oid, v3 boolean)returns text
    as $$
    declare
    begin
     return sys_get_expr($1,$2,$3);
    end;
    $$language plsql;

    create or replace function pg_get_expr(v1 sys_node_tree,v2  oid)returns text
    as $$
    declare
    begin
     return sys_get_expr($1,$2);
    end;
    $$language plsql;
    create or replace view pg_collation as select oid,* from sys_collation;
    create or replace function pg_advisory_unlock(key bigint)returns boolean
    as $$
    declare
    begin
     return sys_advisory_unlock($1);
    end;
    $$language plsql;

    create or replace function pg_advisory_unlock(key1 int,key2 int)returns boolean
    as $$
    declare
    begin
     return sys_advisory_unlock($1,$2);
    end;
    $$language plsql;     