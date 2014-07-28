.. _design:


***********
Design 系统设计
***********



.. _webapp_design

Web框架
=======================

.. _url

URL (webapp.web.Application)
------------------------

* 模仿web框架,先定义好匹配的字典,满足正则匹配则调用相应的方法

* 此处的调用是以类为handler,再调用类里面对应的get或者post方法


Request (webapp.web.Request)
--------------------------------

* 基于CGI协议

* 关键是从CGI从提取出需要的URL,METHOD等信息,然后构造相关的response


Response (webapp.web.BaseHandler)
--------------------------------

* 所有的handlers继承这个基类,里面有设置cookie, http head, template等基本方法


Template (webapp.web.BaseHandler)
----------------------------------------

* 设计了一个简单的template方式,预先将html存在templates文件中,需要时候,读取相关文件,替换需要的部分,重新输出

* 输出时,相当于将拼接好的字符串直接print


Cookie (webapp.utils)
------------------------

* 仿照Tornado secret cookie原理

* 利用时间戳和用户自定义secret串,加密cookie作为用户的验证标准


XSRF (webapp.web)
------------------------

* 仿照Tornado生成随机xsrf cookie原理

* 用uuid生成随机串,在所有post表单中加入xsrf的cookie作为核对标准,与post表单一起提交后在服务器后台核对


.. _database_design

数据库设计
=======================

.. _database

数据库 (model.dbapi)
------------------------

* 数据库的设计请见dbinit.sql这个文件，主要为用户表

* 创建数据库yagra,一个新的用户yagra并为yagra授予必要的权限

* 用户密码使用md5存储


功能处理
=======================


图片上传 (webapp.handlers.UploadHandler)
------------------------

* 图片直接存储在本地的images文件中(需要赋予第三方images可读可写的权限)

* 上传时候,检查图片格式(白名单过滤),同时限制大小,避免存储过大的文件



