Perl 常见问题
====================


Perl 驱动pdi无法加载问题
--------------------------------

1. 首先查看用户的Perl是不是支持ithreads的。

查看方法：perl –V |grep use.*threads

要能看到：useithreads=define, usemultiplicity=define 就表示是支持的

如果看到的是：useithreads=undef 那就是不支持。

2. 查看用户的Perl的版本

目前V8支持的Perl版本是5.16的，如果用户不是这个版本可能无法加载驱动。

3. 执行加载测试

执行：perl -MDBI -e 'DBI-> installed_versions;'

如果成功能看到DBD::KB         : 2.19.3

如果失败能看到报错信息：无法加载

.. figure:: images/perl-1.png


怎么在perl中配置金仓perl驱动
--------------------------------

在perl安装目录下/p5281/lib/perl5/5.28.1/x86_64-linux-thread-multi/DBI.pm中添加如下内容

.. code::

   my $dbd_prefix_registry = {
                                                  ......
                                                  kb_          => { class  => 'DBD::KB',      },
                                                 ......
   }



如何排查perl驱动加载失败步骤
--------------------------------

1. 首先确认，金仓的perl的驱动是否放到了指定文件路径下：

如：/perl/lib 下一般驱动下有三个文件夹：auto Bundle DBD，三个文件夹，以perl/lib下也有对应的单个文件夹

2. 在/perl/lib/auto/DBD/KB中找到KB.so

使用ldd KB.so，查看是否缺失，一般KB.so 依赖libkci.so以及openssl.so的库文件，只需要将依赖库的路径添加至LD_LIBRARY_PATH中或者拷贝至KB.so中即可。