#!/usr/bin/env python
# coding=utf-8

import time
import hashlib
import globaldb


class User(object):

    def __init__(self):
        self.db = globaldb.db
        #self.db.autocommit = True

    # password encoding
    def encode_pwd(self, str):
        if str is not None:
            m = hashlib.md5()
            m.update(str)
            return m.hexdigest()
        else:
            return ""

    def insert_user(self, email, password):
        password = self.encode_pwd(password)
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
        c = self.db.cursor()
        try:
            c.execute(sqlstr, (email, password, email,
                               time.strftime('%Y-%m-%d %H:%M:%S')))
            self.db.commit()
            lastinsertid = c.lastrowid
            print "inser user ", sqlstr
            return lastinsertid
        except:
            self.db.rollback()
            return -1

    def get_user(self, name):
        sqlstr = "SELECT * FROM yagra_user WHERE user_email = %s"
        c = self.db.cursor()
        c.execute(sqlstr, (name,))
        result = c.fetchall()
        print "database user result ", result
        if len(result) is not 0:
            return 0
        else:
            return -1

    def get_user_all(self, name):
        sqlstr = "SELECT * FROM yagra_user WHERE user_email = %s"
        c = self.db.cursor()
        c.execute(sqlstr, (name,))
        result = c.fetchall()
        print "database result ", result
        if len(result) is not 0:
            return result[0]
        else:
            return None

    def check_user(self, name, password):
        password = self.encode_pwd(password)
        sqlstr = "SELECT * FROM yagra_user WHERE user_email = %s AND user_passwd = %s"
        c = self.db.cursor()
        c.execute(sqlstr, (name, password))
        result = c.fetchall()

        if len(result) is not 0:
            return 0
        else:
            return -1

    def update_password(self, name, password):
        password = self.encode_pwd(password)
        sqlstr = "UPDATE yagra_user SET user_passwd = %s WHERE user_email = %s"
        c = self.db.cursor()
        try:
            result = c.execute(sqlstr, (password, name))
            self.db.commit()
            if result > 0:
                return 0
            else:
                return -1
        except:
            self.db.rollback()
            return -1
