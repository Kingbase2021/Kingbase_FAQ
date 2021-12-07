.. _sublime:

sublime text 
================


Usage
-----

Simple snippets work as tab-triggered shortcuts: type the shortcut and press ``<TAB>`` to
replace it with the snippet. If the snippet has placeholders, you can jump between them
using tab.

+------------------------+------------------------------------+----------------------------+
| shortcut               | result                             | key binding                |
+========================+====================================+============================+
| ``h1``                 | Header level 1                     | see `Headers`_             |
+------------------------+------------------------------------+----------------------------+
| ``h2``                 | Header level 2                     |                            |
+------------------------+------------------------------------+----------------------------+
| ``h3``                 | Header level 3                     |                            |
+------------------------+------------------------------------+----------------------------+
| ``e``                  | emphasis                           | ``ctrl+alt+i``             |
|                        |                                    | (``super+shift+i`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``se``                 | strong emphasis (bold)             | ``ctrl+alt+b``             |
|                        |                                    | (``super+shift+b`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``lit`` or ``literal`` | literal text (inline code)         | ``ctrl+alt+k``             |
|                        |                                    | (``super+shift+k`` on Mac) |
+------------------------+------------------------------------+----------------------------+
| ``list``               | unordered list                     | see `Smart Lists`_         |
+------------------------+------------------------------------+----------------------------+
| ``listn``              | ordered list                       |                            |
+------------------------+------------------------------------+----------------------------+
| ``listan``             | auto ordered list                  |                            |
+------------------------+------------------------------------+----------------------------+
| ``def``                | term definition                    |                            |
+------------------------+------------------------------------+----------------------------+
| ``code``               | code-block directive (sphinx)      |                            |
+------------------------+------------------------------------+----------------------------+
| ``source``             | preformatted (``::`` block)        |                            |
+------------------------+------------------------------------+----------------------------+
| ``img``                | image                              |                            |
+------------------------+------------------------------------+----------------------------+
| ``fig``                | figure                             |                            |
+------------------------+------------------------------------+----------------------------+
| ``table``              | simple table                       | ``ctrl+t`` see `Magic      |
|                        |                                    | Tables`_                   |
+------------------------+------------------------------------+----------------------------+
| ``link``               | refered hyperlink                  |                            |
+------------------------+------------------------------------+----------------------------+
| ``linki``              | embeded hyperlink                  |                            |
+------------------------+------------------------------------+----------------------------+
| ``fn`` or ``cite``     | autonumbered footnote or cite      | ``alt+shift+f`` see        |
|                        |                                    | `Magic Footnotes`_         |
+------------------------+------------------------------------+----------------------------+
| ``quote``              | Quotation (``epigraph`` directive) |                            |
+------------------------+------------------------------------+----------------------------+

Also standard admonitions are expanded:

+---------------+
| shortcut      |
+===============+
| ``attention`` |
+---------------+
| ``caution``   |
+---------------+
| ``danger``    |
+---------------+
| ``error``     |
+---------------+
| ``hint``      |
+---------------+
| ``important`` |
+---------------+
| ``note``      |
+---------------+
| ``tip``       |
+---------------+
| ``warning``   |
+---------------+

Render preview
--------------

You can preview your document in different formats converted with different tools
pressing ``ctrl+shift+r``.

The *Quick Window* will offer the format and tool and the result will be automatically open
after the conversion.

By the moment, it can use Pandoc_, rst2pdf_, or ``rst2*.py`` tools (included with
docutils_) to produce ``html``, ``pdf``, ``odt`` or ``docx`` output formats.

Each time you select a ``format + tool`` option, it turns the default the following times.

.. note::

    The original code is from the `SublimePandoc <https://github.com/jclement/SublimePandoc>`_
    project.


Magic Tables
------------

There is a particular *magic* expansion for tables. Here is how it works:

网格表
^^^^^^^^^^^^^^

1. 创建表格提纲, 用一个或多个空格分割列::


      This is paragraph text *before* the table.

      Column 1  Column 2
      Foo  Put two (or more) spaces as a field separator.
      Bar  Even very very long lines like these are fine, as long as you do not put in line endings here.

      This is paragraph text *after* the table.

2. 把鼠标放在要转化成表格的内容里.

3. 按下 ``ctrl+t, enter`` (Linux or Windows) or ``super+shift+t, enter`` (Mac). 将会自动格式化成表格::


      This is paragraph text *before* the table.

      +----------+---------------------------------------------------------+
      | Column 1 | Column 2                                                |
      +==========+=========================================================+
      | Foo      | Put two (or more) spaces as a field separator.          |
      +----------+---------------------------------------------------------+
      | Bar      | Even very very long lines like these are fine, as long  |
      |          | as you do not put in line endings here.                 |
      +----------+---------------------------------------------------------+

      This is paragraph text *after* the table.


现在假设你想增加某一单元格内容::

      +----------+---------------------------------------------------------+
      | Column 1 | Column 2                                                |
      +==========+=========================================================+
      | Foo is longer now     | Put two (or more) spaces as a field separator.          |
      +----------+---------------------------------------------------------+
      | Bar      | Even very very long lines like these are fine, as long  |
      |          | as you do not put in line endings here.                 |
      +----------+---------------------------------------------------------+

按下同样的快捷键, 表格结构会自动调整::


      +-------------------+--------------------------------------------------------+
      | Column 1          | Column 2                                               |
      +===================+========================================================+
      | Foo is longer now | Put two (or more) spaces as a field separator.         |
      +-------------------+--------------------------------------------------------+
      | Bar               | Even very very long lines like these are fine, as long |
      |                   | as you do not put in line endings here.                |
      +-------------------+--------------------------------------------------------+


此外，如果你想保持列宽固定，可以按``ctrl+t, r``  or  ``super+shift+t, r`` (Mac)::


      +----------+---------------------------------------------------------+
      | Column 1 | Column 2                                                |
      +==========+=========================================================+
      | Foo is   | Put two (or more) spaces as a field separator.          |
      | longer   |                                                         |
      | now      |                                                         |
      +----------+---------------------------------------------------------+
      | Bar      | Even very very long lines like these are fine, as long  |
      |          | as you do not put in line endings here.                 |
      +----------+---------------------------------------------------------+

还可以使用鼠标合并单元格::

    +----+----+
    | h1 | h2 |
    +====+====+
    | 11 | 12 |
    +----+----+
    | 21 | 22 |
    +----+----+

移动鼠标到单元格 ``12`` ，按 ``ctrl+t, down``。 将得到::

    +----+----+
    | h1 | h2 |
    +====+====+
    | 11 | 12 |
    +----+    |
    | 21 | 22 |
    +----+----+


.. note::

   The original code of this feature was taken from
   `Vincent Driessen's vim-rst-tables <https://github.com/nvie/vim-rst-tables>`_ :

.. note::

   The original code of `wcwidth <https://github.com/jquast/wcwidth>`_ was taken to solve alignment issue with CJK characters.



简单表格
^^^^^^^^^^^^^

1. 创建表格提纲, 用一个或多个空格分割列::


      This is paragraph text *before* the table.

      Column 1  Column 2
      Foo Put two (or more) spaces as a field separator.
      Bar  Even very very long lines like these are fine, as long as you do not put in line endings here.

      This is paragraph text *after* the table.

2. 把光标放在要转化成表格的内容里.

3. 按下 ``ctrl+t, s`` (Linux or Windows) or ``super+shift+t, s`` (Mac). 将会自动格式化成表格::

      This is paragraph text *before* the table.

      ==========  ================================================================================================
      Column 1    Column 2
      ==========  ================================================================================================
      Foo         Put two (or more) spaces as a field separator.
      Bar         Even very very long lines like these are fine, as long as you do not put in line endings here.
      ==========  ================================================================================================

      This is paragraph text *after* the table.


现在假设你想增加某一单元格内容::


      ==========  ================================================================================================
      Column 1    Column 2
      ==========  ================================================================================================
      Foo is longer now         Put two (or more) spaces as a field separator.
      Bar         Even very very long lines like these are fine, as long as you do not put in line endings here.
      ==========  ================================================================================================

按下同样的快捷键, 表格结构会自动调整::


      ===================  ================================================================================================
      Column 1             Column 2
      ===================  ================================================================================================
      Foo is longer now    Put two (or more) spaces as a field separator.
      Bar                  Even very very long lines like these are fine, as long as you do not put in line endings here.
      ===================  ================================================================================================



.. note::

   The original code of this feature was taken from
   `Vincent Driessen's vim-rst-tables <https://github.com/nvie/vim-rst-tables>`_ :



Smart lists
-----------


Ordered or unordered lists patterns are automatically detected. When you type something
like this::

  1. Some item
  2. Another|

When press ``enter`` the newline will prepended with a logical next item::

  ...
  2. Another
  3. |

If you press ``enter`` when the item is empty, the markup is erased keeping
the same indent as the previous line, in order to allow multilines items.
Also note that orderer list works with an alphabetic pattern or roman numbers pattern
suffixed with a period
(``a. b. c. ...``, ``A. B. C. ...``, ``i. ii. iii. iv. ...``, ``X. XI. XII. ...``, ``#.``);
surrounded by parentheses
(``(a) (b) (c) ...``, ``(A) (B) (C) ...``, ``(i) (ii) (iii) (iv) ...``, ``(X) (XI) (XII) ...``, ``(#)``);
or suffixed with a right-parenthesis.
(``a) b) c) ...``, ``A) B) C) ...``, ``i) ii) iii) iv) ...``, ``X) XI) XII) ...``, ``#)``);

.. tip::

   The very same feature works for  `line blocks <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#line-blocks>`_ starting a line with ``|``.

.. note::

   This feature was proudly stolen from `Muchenxuan Tongh's SmartMarkdown
   <https://github.com/demon386/SmartMarkdown>`_




Headers
--------

.. _header completion:

Autocompletion
^^^^^^^^^^^^^^^^^^^^^^^

You can autocomplete standard headers (over/)underlines with ``TAB``.

For example try this::


    **********<TAB>
    A longer main title
    *******

Or this::

    A subtitle
    ---<TAB>


You'll get::


    *******************
    A longer main title
    *******************

    A subtitle
    ----------

respectively.



Folding/unfolding
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you put the cursor in a completed header and press ``shift + TAB`` (``alt + TAB`` in Mac),
the section under it will be folded/unfolded.

For example::

    Folding/unfolding
    +++++++++++++++++<TAB>

    If you put the cursor in a completed header and press ``shift + TAB``,
    (``alt + TAB`` in Mac) the section under it will be folded/unfolded.

    Navigation
    ++++++++++

    ...

Result in:

    .. image:: https://raw.github.com/dbousamra/sublime-rst-completion/11_foldable_headers/img/folding.png


Nested sections under a header are included.


Navigation
^^^^^^^^^^^^^^^^^^

Also, it's possible to jump between headers.
``alt+down`` and ``alt+up`` move the cursor position to the closer next or
previous header respectively.

``alt+shift+down`` and ``alt+shift+up`` to the same, but only between headers
with the same or higher level (i.e. ignore childrens)

The header level is detected automatically.


Adjust header level
^^^^^^^^^^^^^^^^^^^^^^^

With the cursor in a header, press ``ctrl + +`` (plus key) and ``ctrl + -``
(minus key) (``alt + +`` and ``alt + -``, in Mac) will increase and decrease the
header level respectively. The adornment decoration (underline / overline) are
autodetected from the document and uses Sphinx's conventions as default.

For example, you have the cursor in::

    Magic Footnotes|
    ---------------

Which is a header level 2 and want to convert to a level 3, press ``ctrl + -`` to get::

    Magic Footnotes
    +++++++++++++++
    |




Magic Footnotes
---------------

This is the smarter way to add footnotes, grouping them (and keepping count)
in a common region at the bottom of the document.

When you want to add a new note, press ``alt+shift+f``.
This will happen:

-  A new ``n+1`` (where ``n`` is the current footnotes count) note reference
   will be added in the current cursor position
-  The corresponding reference definition will be added
   at the bottom of the *footnotes region*
-  The cursor will be moved to write the note

After write the note you can go back to the reference with ``shift+up``. Also, if
the cursor is just after a reference (i.e: the caret is next to the underscore like this ``[XX]_|`` ) you can jump to its definition with ``shift+down`` .

This feature is based on the code by `J. Nicholas Geist <https://github.com/jngeist>`_
for `MarkdownEditing <https://github.com/ttscoff/MarkdownEditing>`_









