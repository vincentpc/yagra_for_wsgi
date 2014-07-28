#!/usr/bin/env python
# coding=utf-8

import MySQLdb
import sys
sys.path.append("..")

import config


db = MySQLdb.connect(host=config.DB_HOST,
                     port=config.DB_PORT,
                     user=config.DB_USER,
                     passwd=config.DB_PASSWD,
                     db=config.DB_NAME,
                     charset="utf8"
                     )
