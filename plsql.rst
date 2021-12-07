PLSQL类
=======================


KES创建过程，报错：PL/SQL block not end correctly
--------------------------------------------------------

在使用ORACLE方法创建PLSQL函数时候，需要先设置好SQLTERM结束符。如： 
  
.. code::

   CREATE OR REPLACE PROCEDURE proc1() AS
   BEGIN
            raise notice 'call proc1';
   END;

   报错：PL/SQL block not end correctly


正确执行方式：   

.. code::

   \set SQLTERM /       --设置结束符
   CREATE OR REPLACE PROCEDURE proc1() AS
   BEGIN
      raise notice 'call proc1';
   END;
   /

如何调用含out参数的存储过程
----------------------------

对于 out参数的过程，只能在block里调用，而且必须传入参数。

.. code::

   declare
     v_retcode text;
     v_id integer;
   begin
     CALL proc1(v_id, v_retcode);
   end;
   /



Savepoint 使用问题
----------------------------

适用版本：V8R6

V8R6不支持在 PLSQL块使用，以下不行：

.. code::

   begin
      insert into t1 values(1);
      savepoint sv1;
      insert into t1 values(1,'a');
   exception
      when others then
        rollback to sv1;
   end;

只能在事务块内使用：

.. code::

   begin;
   insert into t2 values(1);
   savepoint sv1;
   insert into t2 values(2);
   rollback to  sv1;
   insert into t2 values(3);
   commit;


Create operator（bool与整型比较）
--------------------------------------------------------

适用版本：V8R3

问题描述：

   对于整数类型数据与bool类型进行比较时，要么转换报错，要么结果错误。具体问题如下例：

   .. image:: images/FAQ15841.png
      :width: 368px
      :height: 232px
 

解决方法：

   创建operator ，具体脚本如下：

   .. code::

      create or replace internal function sys_catalog.bool_eq_numeric(bool,numeric) returns bool as $$ select $1::numeric = $2; $$ language sql; 

      create operator sys_catalog.= (procedure = bool_eq_numeric,leftarg = bool,rightarg = numeric,commutator = =);                              

      create or replace internal function sys_catalog.numeric_eq_bool(numeric, bool) returns bool as $$ select $1 = $2::numeric; $$ language sql; 

      create operator sys_catalog.= (procedure = numeric_eq_bool,leftarg = numeric,rightarg = bool,commutator = =);                              



For循环变量
----------------------------

适用版本：V8R3 , V8R6

问题描述：

   在创建procedure 时，会有如下错误：

   .. code::

      reate or replace procedure plpgsql_proc() as 
      $$
      begin
        for i in select regexp_split_to_table('ab,bc,cd',',') loop
          raise notice '%',i;
        end loop;
      end;
      $$ language plpgsql;

      ERROR:  loop variable of loop over rows must be a record variable or list of scalar variables
      LINE 4:   for i in select regexp_split_to_table('ab,bc,cd',',') loop


问题分析：

   以上的写法实际是plsql的语法，对于R6 版本的database_mode=pg，R3版本大小写不敏感的环境，执行块时默认是plpgsql编译器。因此，以上写法是报错的。

问题解决：

   必须先定义循环变量。

   .. code::

      create or replace procedure plpgsql_proc() as 
      $$
      declare 
        v_text text;
      begin
        for v_text in select regexp_split_to_table('ab,bc,cd',',') loop
          raise notice '%',v_text;
        end loop;
      end;
      $$ language plpgsql;


函数变量不能超过512
----------------------------

适用版本：V8R3

问题描述：

   使用block，function, procedure 时，可能会遇到如下错误：

   .. code::

      ERROR：ANONYMOUS BLOCK has more than 512 arguments。 


问题解析：

   这是由于参数个数超过了512，需要修改代码。参数 max_function_args默认是512，无法修改。