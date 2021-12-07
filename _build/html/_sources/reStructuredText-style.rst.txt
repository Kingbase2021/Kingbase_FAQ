.. _restructuredText样式:

=================================
restructuredText样式（一级标题）
=================================


章节标题（二级标题）
----------------------------


三级标题
^^^^^^^^^^^^^^

四级标题
~~~~~~~~~~~~~~~

五级标题
############

六级标题
************


段落
------------

段落由空白行分割，左侧必须对齐（没有空格，或者有相同多的空格）。缩进的段落意味着引用。
例如


这是第一段

这是第二段
这还是第二段




行内标记
---------------------------

*斜体*

**加粗**

`强调解释`

``行内代码``

A下标xxx    A :sub:`xxx`
A上标xxx    A :sup:`xxx`

注意：
  对于行内标记, 标记前后要留有至少一个空格. 如 你好*我没变斜*你好 –> 你好*我没变斜*你好, 正确为: 你好 *我变斜了* 你好 –> 你好 我变斜了 你好, 或 你好\ *我变斜了*\ 你好 –> 你好我变斜了你好.



列表
------------------------

无序列表使用 ``-`` , ``*`` , ``+`` 来标记:

- 无序列表第一项
- 无序列表第二项

有序列表使用 ``num.`` 来标记:

1. 有序列表第一项
2. 有序列表第二项

自动编号列表必须使用 ``#.`` 来标记:

#. 自动编号的列表第一项
#. 自动编号的列表第二项

这是一个定义列表:

term
    术语定义必须缩进

    可以包含多个段落

next term
    术语描述

下面是一个嵌套列表, 每一级别向右缩进一次, 同级别缩进应相同:

1. 有序列表第一项
    * 无序列表第一项
    * 无序列表第二项
#. 有序列表第二项
    + 无序列表第一项
    + 无序列表第二项
  


表格
-------------------------------

网格表（带表标题和编号）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

网格表中使用的符号有：-、=、|、+。
- 用来分隔行， = 用来分隔表头和表体行，| 用来分隔列，+ 用来表示行和列相交的节点。

以下代码段指定四列的相对宽度，更改每列的文本对齐方式，禁用第三、四列的文本换行：

.. table:: Grid Table Demo
   :name: table-gridtable
   :widths: 3 1 1 1 
   :column-alignment: left center right right
   :column-wrapping: false true true  false

   +------------------------+----------+-------------+----------+
   | Header row, column 1   | Header 2 | Header 3    | Header 4 |
   | (header rows optional) |          |             |          |
   +========================+==========+=============+==========+
   | body row 1, column 1   | column 2 | column 3    | column 4 |
   +------------------------+----------+-------------+----------+
   | body row 2             | ...      | ...         |          |
   +------------------------+----------+-------------+----------+

可以使用 :ref:`table-gridtable` 引用, 在Sphinx中还可以使用 :table:numref:`table-gridtable` 来引用.



简单表格（无表标题和编号）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

书写简单, 但有一些限制: 需要有多行, 且第一列元素不能分行显示, 如下

=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======



CSV表格（带表标题和编号）
^^^^^^^^^^^^^^^^^^^^^^^


.. csv-table:: Frozen Delights!
   :header: "Treat", "Quantity", "Description"
   :widths: 15, 10, 30

   "Albatross", 2.99, "On a stick!"
   "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be
   crunchy, now would it?"
   "Gannet Ripple", 1.99, "On a stick!"


list table（带表标题和编号）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: List tables can have captions like this one.
    :widths: 10 5 10 50
    :header-rows: 1
    :stub-columns: 1

    * - List table
      - Header 1
      - Header 2
      - Header 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Stub Row 1
      - Row 1
      - Column 2
      - Column 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Stub Row 2
      - Row 2
      - Column 2
      - Column 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.
    * - Stub Row 3
      - Row 3
      - Column 2
      - Column 3 long. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sit amet mauris arcu.



sublime text
^^^^^^^^^^^^^^^^^

使用”Restructured Text (RST) Snippets”, 即 sublime-rst-completion , 表格的制作将变得极为简单。详见sublime.txt




注释
-----------------------

..
   这整个缩进块都是
   一个注释.
   你只能在源码中看到我们, 我们不会被渲染出来

   仍是一个评论.

你可以看到我, 我不是注释.



图片
-------------------------

image指令图片
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

无发自动生成编号，不建议使用，后续会将手册中所有image指令图片替换为figure指令图片

.. image:: images/logo.png
   :height: 100px
   :width: 200 px
   :scale: 50 %
   :alt: 对于不能显示图片的时候, 显示这些文字
   :align: right



figure指令图片（包含图片标题、编号和图例）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _figure-logo:

.. figure:: images/logo.png
   :scale: 50 %
   :alt: map to buried treasure

   This is the caption of the figure (a simple paragraph).

   The legend consists of all elements after the caption.  In this
   case, the legend consists of this paragraph



代码块
------------------

.. code:: 

   some codes1
   some codes1



指令
------------------------

.. tip:: This is a tip

.. note:: This is a note

.. hint:: This is a hint

.. danger:: This is a danger

.. error:: This is an error

.. warning:: This is a warning

.. caution:: This is a caution

.. attention:: This is an attention

.. important:: This is an important

.. seealso:: This is seealso 
 
.. include:: sublime.rst



链接
-------------------------


外部链接（外部网页，或不同的rst文件） [1]_ 
  1. 更多信息参考`引用文档 <http://example.com/>`_

  2. 更多信息参考 `引用文档`_.

  .. _引用文档: http://example.com/

  3. 如果链接文本是Web地址，reStructuredText会自动将网址生成超链接。https://github.com/SeayXu/
    

     sublime更多信息参考 :ref:`sublime` 


内部链接

  1. 首先需要在标题, 图像, 表等对象前放置一个标签 `.. _label:`，比如在上方 图片_ 处放置了一个标签 `figure-logo` , 注意空白行:

  2. 引用
  通过 :ref:`figure-logo` 引用, 点击会跳到图像位置


在同一个rst中，小节标题会自动生成超链接地址，使用小节标题作为超链接名称就可以生成隐式链接。例如: 行内标记信息参考 行内标记_




脚注
----------------

包含两步:
1.  在文档底部放置脚注主体, 以 rubric 指令标示:

2.  在需要插入脚注的地方插入脚注名 [#name]
其中, 使用 [#name]_ 可以实现自动编号, 当然也可以使用数字来指示确定的脚注编号 [3]_ .




替换引用
----------------


替换引用就是用定义的指令替换对应的文字或图片
这是 |logo| kingbase的Logo，我的kingbase用户名是:|name|。



.. |logo| image:: images/logo.png
.. |name| replace:: xxx



.. rubric:: Footnotes


.. [1] 第1条脚注的文本.
.. [#name] 第2条脚注的文本.
.. [3] 第3条脚注的文本.









