# -*- coding: utf-8 -*-
#
# KES_FAQ文档构建配置文件

#import sphinx_rtd_theme
import sys
import os

# readthedocs-sphinx-search扩展
#extensions = [
#    'sphinx_search.extension'
#]

# kirlent_sphinx扩展
#extensions = ["kirlent_sphinx"]


# -- 通用配置 ------------------------------------------------

needs_sphinx = "3.1"

# 源文件的文件扩展名。Sphinx将带有此后缀的文件视为源。
source_suffix = ".rst"
# 所有reST源文件的编码。推荐的编码和默认值是'utf-8-sig'。
source_encoding = "utf-8-sig"

# “主”文档的文档名称，即包含根toctree指令的文档。
master_doc = "index"

# 通用信息
project = "KingbaseES Frequently Asked Questions"
copyright = (
    "1999-2021, 北京人大金仓信息技术股份有限公司"
)
author = "北京人大金仓信息技术股份有限公司"

# 项目的版本信息，以 |version| 和 |release| 作为代替
version = " "
# 完整的版本，包括alpha/beta/rc标签
release = version


# 查找源文件时应排除的全局样式模式列表。
exclude_patterns = ["_build"]

smartquotes = False

# 用于突出显示源代码的样式名称。如果未设置，'sphinx'则选择主题的默认样式或选择HTML输出。
pygments_style = "sphinx"


# 创建全局替换
rst_prolog = """

"""

# -- 图、表编号配置 ------------------------------------------

math_number_all = True  # Set this option to True if you want all displayed math to be numbered. The default is False.
math_eqref_format = 'Eq.{number}'  # gets rendered as, for example, Eq.10.

# If True, displayed math equations are numbered across pages when numfig
# is enabled. The numfig_secnum_depth setting is respected. The eq, not
# numref, role must be used to reference equation numbers. Default is
# True.
math_numfig = True

# see http://www.sphinx-doc.org/en/master/usage/configuration.html#confval-numfig
# If true, figures, tables and code-blocks are automatically numbered if they have a caption.
# The numref role is enabled. Obeyed so far only by HTML and LaTeX builders. Default is False.
# The LaTeX builder always assigns numbers whether this option is enabled or not.
numfig = True
numfig_secnum_depth = 2

# A dictionary mapping 'figure', 'table', 'code-block' and 'section' to strings that are used for format of figure numbers.
# As a special character, %s will be replaced to figure number.
# Default is to use 'Fig. %s' for 'figure', 'Table %s' for 'table', 'Listing %s' for 'code-block' and 'Section' for 'section'.
numfig_format = {
    'figure': 'Fig. %s',
    'table': 'Table %s',
}

numfig_format = {
    'figure': '图 %s',
    'table': '表 %s',
}



# -- HTML输出选项 ----------------------------------------------


html_theme = "sphinx_rtd_theme"
html_theme_path = ["_themes",]


# 主题选项
html_theme_options = {
    # 如果为False,仅显示徽标图像，不在侧边栏顶部显示项目名称
    "logo_only": True,
    # 折叠导航
    "collapse_navigation": False,
}


# 这些文件夹被复制到文档的HTML输出中
html_static_path = ["_static"]


html_css_files = [
    "css/custom.css",
]

html_js_files = [
    "js/custom.js",
]


# Path to find HTML templates.
templates_path = ['templates']

# If not '', a '最后更新于:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'


# HTML帮助文件名
htmlhelp_basename = "FAQ-doc"


# -- reStructuredText语法选项 ----------------------------------
# Enable directives that insert the contents of external files
file_insertion_enabled = False



# -- LaTeX输出选项 ---------------------------------------------
latex_engine = 'xelatex'

# 封面logo
# latex_logo = "images/logo.png"

# 文档名称列表，作为所有手册的附录。
latex_appendices = ['legalnotice']






  

# 将文档树分组到LaTeX文件中。
# 元组列表 (source start file, target name, title, author, document class [howto/manual]).
_stdauthor = r' '
latex_documents = [
    ('index-manual', 'KES-FAQ.tex',
     'KingbaseES常见问题手册', _stdauthor, 'manual'),
]



