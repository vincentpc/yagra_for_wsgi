.. _installation-and-configuaration:


**************************************
Installation and Configuration 系统安装及运行
**************************************

.. _installation

Installation 
===============

.. _dependency

Dependency
----------

* Python 2.7:

 	参考网址 [Python 2.7](http://www.python.org/download/releases/2.7/)
 	
* Apache 2:
	
	sudo apt-get install apache2

	参考网址 [Apache](http://httpd.apache.org/)

* Mysql:

	sudo apt-get install mysql

    	sudo apt-get install mysql-dev
    
 	参考网址 [mysql](http://www.mysql.com/)

* Mysql-python(可使用make init自动安装):

    	pip install mysql-python

 	参考网址 [MySQL for Python](http://sourceforge.net/projects/mysql-python/)


.. note:

   	make init 自动安装依赖软件(mysql-python)
   	
   	make doc  自动生成使用文档,文档目录在doc/_build下

       
.. _install

Install
-------

.. _making-a-list:
   		
* 初次运行设置apache(请根据系统apache安装目录调正路径)::

 		vi /etc/apache2/sites-enable/default
 		
* 对于Apache，我们首先需要打开它的rewrite模块。因为需要Apache将所有的请求全部rewrite到指定处理器后面::

		a2enmode rewrite
		service apache2 restart

* 初次运行创建数据库::

   		mysql -uname -ppassword < dbinit.sql      
   
* 初次运行设置参数(设置一次即可,详细介绍见下文)::

   		vi config.py            

* 在根目录下创建log及images目录(存放log和上传图片)::
  (`将images目录权限改为可写可读,以便上传照片`)
	
* 运行(使用apache服务器分发请求)::

   		python main.py

.. _configuration

Configuration 
================

Apache Configuration
-------------
Apache2服务器设置

主要为两部分,对于特定静态文件(css,js等),直接映射;其他动态文件,交由程序动态处理

端口假定为8080

网站程序目录为/home/ubuntu/yagra::

    #######################
    # Apache Configure ##
    #######################
    
    <VirtualHost *:8080>
    ServerName vincentpc.servehttp.com
        ServerAdmin webmaster@servehttp.com

    DocumentRoot /home/ubuntu/yagra
    ErrorLog /home/ubuntu/yagra/log/yagra_errors.txt

    AddHandler cgi-script .py
    DirectoryIndex main.py

    Alias /css /home/ubuntu/yagra/static/css/
    Alias /js /home/ubuntu/yagra/static/js
    Alias /images /home/ubuntu/yagra/images/
    <Directory /home/ubuntu/yagra/static/css>
        Order allow,deny
        Allow from all
    </Directory>
        <Directory "/home/ubuntu/yagra">
                AllowOverride None
                Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
                Order allow,deny
                Allow from all
        <IfModule mod_rewrite.c>
            RewriteEngine on
            RewriteBase /
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteCond %{REQUEST_FILENAME} !-d
            RewriteRule ^(.*)$ main.py/$1 [L]
        </IfModule>
        </Directory>


        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn

        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>


.. _database-config:

Database Configuration
----------------------

使用dbinit.sql脚本创建数据库

默认创建名字为yagra的数据库,如果存在则会删除后创建

默认创建一个yagra账户(`密码为abcd!1234,与config对应`)并用此用户访问该数据库::




System Configuration
-------------
初始设置系统参数说明(config.py)::

    #######################
    # system Configure ##
    #######################
    #初始运行时设置cookie加密密钥,任意字符串
    COOKIE_SECRET =  'thisis secret' 

    
    
    #######################
    # Database Configure ##
    #######################
    
    #数据库连接设置,依次为IP,端口,用户名,用户密码,数据库名称
    DB_HOST = 'localhost' 
    DB_PORT = 3306
    DB_USER = 'yagra'
    DB_PASSWD = 'abcd!1234'
    DB_NAME = 'yagra'


Documentation
===============  
使用make doc创建项目文档

存储在 /docs/_build/html(首页为index.html)
    
