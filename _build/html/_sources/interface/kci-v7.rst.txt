V7 KCI常见问题
==========================


用KCI操作大对象写到用户的表里，发现OID不是创建的OID
------------------------------------------------------------

原因是最后写OID到用户表的时候，需要注意类型转换问题，否则可能被当做普通字串插入，造成重新生成一个对象OID。

例子：

.. code::

    sprintf(sql, "insert into %s values (%ld::OID);", tbl_name, blobid);
                       res = KCIStatementExecute(conn, sql);