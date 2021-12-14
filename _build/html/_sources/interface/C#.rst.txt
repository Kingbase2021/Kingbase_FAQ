C# 常见通过问题
======================

NDP的连接数问题
----------------------------

NDP驱动默认使用连接池连接池大小默认是20，所以如果要建立更多连接需要改连接参数。

例子：

Pooling
  指定是否使用连接池。可取值为 True 和 False。默认为 True

MaxPoolSize
  连接池中最大连接数，超过该数字则新建连接失败。默认为 20。


NDP驱动net45、net451, netcore2.0有什么不同？
-------------------------------------------------

net45，net451主要只要的.net framework 的版本号，该已net45,net451只能在指定的.net framwork 中使用，有事也可在高于指定版本的.net framework中使用，该驱动是在windows平台下使用的，而netcore2.0指的是既可以在.net framework框架中也可以在netcore框架中使用，而且netcore2.0为跨平台驱动，可以再linux中使用。(jexus中可以将net45等驱动在linux下使用)