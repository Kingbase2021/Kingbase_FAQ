数据安全
================


Sys_rman备份报“current time may be rewound”
-------------------------------------------------------

适用版本：V8R3

原因分析：数据库初始化后，系统往回修改了时间（从2029年改回2020年），备份时由于存在比当前时间之后的数据库对象，导致备份失败。

处理：使用sys_dump 导出、导入后，sys_rman 备份正常。


如何导出一致时间点的数据
------------------------------

适用版本：V8R3 ， V8R6

问题描述：默认sys_dump 导出的数据是表级的一致性，也就是对表发出copy命令时间点已提交的数据，但由于不同表copy时间点不同，因此，sys_dump导出的数据不是完全一致时间点。如何导出一致时间点数据？

解决方法：

   Session A: sys_export_snapshot实际返回的是当前事务ID，实际可以不需要isolation level repeatable read。 

   .. figure:: images/FAQ31140.png
      :width: 554px
      :height: 125px

   Session B: sys_dump --snapshot=00000806-1

   Session A: 结束事务

   .. note::

      Sesssion B 导出的是Session A 运行sys_export_snapshot时间点已提交的数据，即使在导出过程中其他会话对数据库进行了修改并提交。


索引问题导致数据访问问题
--------------------------------

版本：V8R3

问题原因：系统在进行压力测试，同时系统主备切换。主备间采取异步方式

问题现象：

   可以看到，根据条件返回的记录数据与where条件不匹配。这3个条件是主键。

   .. figure:: images/FAQ31384.png
      :width: 554px
      :height: 299px

解决方案：rebuild index

原因分析： 

   1. 这条SQL采取的是索引访问；

   2. 根据索引取得两个ctid，再根据ctid取得数据；

   3. 通过访问表记录的xmax ，确定记录是有效的（未被删除）；

   4. 问题1：为什么索引entry的值（4,3,2521）与table tuple（7,5,998）值不一致？索引通过ctid与table tuple关联，当索引异常时，就可能出现该问题。

   5. 问题2：既然是主键，索引entry为什么会出现两个entry？索引是没有有效性判断的，需要访问表进行判断，也就是说就算索引存在两个相同entry，理论上通过tuple有效判断后最多只能留1条。