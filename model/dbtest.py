#!/usr/bin/env python
# coding=utf-8

import MySQLdb
import time
import sys

sys.path.append("..")
import config


db =  MySQLdb.connect(host=config.DB_HOST,
                     user=config.DB_USER,
                     passwd=config.DB_PASSWD,
                     db=config.DB_NAME,
                     charset="utf8"
                    )       

def test_insert(name="vincent"):
    sqlstr = """
        INSERT INTO `yagra`.`yagra_user`
        (
        `user_login`,
        `user_passwd`,
        `user_email`,
        `user_time`
        )
        VALUES
        (%s, %s, %s, %s)
    """
    c = db.cursor()
    c.execute(sqlstr, (name, "1234", name + "@gmail.com",
                       time.strftime('%Y-%m-%d %H:%M:%S')))
    db.commit()


def test_select():
    import pprint
    sqlstr = "SELECT * FROM yagra_user"
    c = db.cursor()
    c.execute(sqlstr)
    pprint.pprint(c.fetchall())
    c.close()


def dbtest():
    #import sys
    #test_insert(sys.argv[1])
    test_select()
    db.close()


if __name__ == "__main__":
    dbtest()
