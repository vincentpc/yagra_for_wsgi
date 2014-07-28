.. _api:

*********
API 客户端接口
*********

头像访问API
===============

url:
----
   http://example.com/avatar/xxx
   
   也可以直接包括在img的html tag中(如<img src="http://example.com/avatar/xxx" />)

HTTP请求方式:
---------
   GET
   
  

请求参数:
-----


* xxx为账户email的hash值(md5)

   如http://example.com/avatar/63268799c152a440cfe11a4f3ea62f45


返回数据:
-----
      
      提供原始头像图片,可以另存为(保存原有格式)


