Docker环境相关问题
================================


【exit code 137】错误信息
-------------------------------

Docker环境中，在sys_dump 或其他操作时，如果报错“exit colde 137”，通常表示内存问题。

.. figure:: images/FAQ34211.png
   :width: 554px
   :height: 92px
    

Docker 环境下license机制
---------------------------------

KES 是通过网卡的MAC确定license，但是在Docker环境下没有mac，无法通过原有的mac机制绑定license。Docker环境下，目前采用license版本没有与任何硬件信息绑定，但需要专门申请。