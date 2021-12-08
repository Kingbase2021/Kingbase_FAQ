# KingbaseES Frequently Asked Questions

该文档库中所有文档都基于 sphinx-doc 构建，支持编译为HTML、PDF、WORD等sphinx-doc支持的文档类型。


## v8r6_document_dev简介

_build：生成的文件的输出目录。
_static：静态文件目录，比如控制输出html的.css .js文件。
_themes：sphinx-doc的主题和扩展。
images:图片
conf.py：存放 Sphinx 的配置，包括在 sphinx-quickstart 时选中的那些值，可以自行定义其他的值。
index.rst：文档项目起始文件。
legalnotice:版权申明
make.bat：Windows 用命令行。
Makefile：可以看作是一个包含指令的文件，在使用 make 命令时，可以使用这些指令来构建文档输出。
README.md:说明文件
reStructuredText-style.rst: reStructuredText语法结构快速入门手册
sublime.rst: Sublime Text快速入门手册




## 编辑

### 编辑现有页面

要编辑现有页面，找到对应.rst源文件，在您喜欢的文本编辑器中将其打开：

  - Sublime Text。
     添加插件 
     1. OmniMarkupPreviewer—用于解析渲染rst等多种标记语法，安装之后，按快捷键Ctrl+Alt+o预览； 
     2. reStructuredText—用于语法着色；
     3. sublime-rst-completion—用于自动补全，在制表时非常有用 
  - Vscode支持对sphinx的预览，并且Vscode的扩展Table Formatter能够自动补全sphinx中表格。（添加扩展restructuredtext、table-formatter）
  - notepad

reStructuredText语法规则详见 style.txt和《产品手册编制规范》

然后，提交更改，推送至Git。


### 添加新页面

要添加新页面，请在要向其中添加文件的部分中创建一个具有有意义名称（并且不与现有.rst文件名称重复）的.rst文件。
例如Kingbase_FAQ/interface/odbc.rst。
像编写任何其他文件一样编写其内容，并确保在文件的开头定义Sphinx的引用名称（检查其他文件的语法），该文件的名称基于前缀“ doc _”（例如.. _sql-xxx:）。
然后，将页面添加到相关的“ toctree”（目录，例如Kingbase_FAQ/index.rst）。



## 文档编译

构建HTML（或Sphinx支持的任何其他格式，例如PDF，EPUB或LaTeX），需要安装[Sphinx] >= 1.3以及（对于HTML）[readthedocs.org theme] 主题。

###  环境配置

- sphinx安装（基于python ）

    pip install -U Sphinx

- 样式主题:

    pip  install sphinx-rtd-theme

- `搜索`扩展:

    pip install readthedocs-sphinx-search

- `表格`扩展

    pip install kirlent_sphinx



### rst2html

    make html

### rst2PDF（texlive）

    make latexpdf

### CHM 构建方法（需要安装好HTML Help Workshop）：

    make htmlhelp	
	run HTML Help Workshop with the ".hhp project file in $(BUILDDIR)/htmlhelp."

	





