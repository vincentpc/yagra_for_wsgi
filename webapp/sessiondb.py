#!/usr/bin/env python
# coding=utf-8

import model.globaldb


class SessionDB(object):

    def __init__(self):
        self.db = model.globaldb.db
        self.table = 'session'

    def check_key(self, key):
        sqlstr = "SELECT * FROM " + self.table + " WHERE session_id = %s"
        c = self.db.cursor()
        c.execute(sqlstr, (key,))
        result = c.fetchone()
        c.close()
        if result is not None:
            return True
        else:
            return False

    def get_key(self, key):
        sqlstr = "SELECT data FROM " + self.table + " WHERE session_id = %s"
        c = self.db.cursor()
        c.execute(sqlstr, (key,))
        result = c.fetchone()
        c.close()
        if result is not None:
            return result
        else:
            return None 

    def update_key_time(self, key, time):
        sqlstr = "UPDATE " + self.table + \
            " SET atime = %s WHERE session_id = %s"
        c = self.db.cursor()
        try:
            result = c.execute(sqlstr, (time, key))
            self.db.commit()
            if result > 0:
                return 0
            else:
                return -1
        except:
            self.db.rollback()
            return -1
        finally:
            c.close()

    def update_key_data(self, key, data):
        sqlstr = "UPDATE " + self.table + \
            " SET data = %s WHERE session_id = %s"
        c = self.db.cursor()
        try:
            result = c.execute(sqlstr, (data, key))
            self.db.commit()
            if result > 0:
                return 0
            else:
                return -1
        except:
            self.db.rollback()
            return -1
        finally:
            c.close()

    def delete_key(self, key):
        sqlstr = "DELETE FROM " + self.table + " WHERE session_id = %s"
        c = self.db.cursor()
        try:
            c.execute(sqlstr, (key,))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            c.close()

    def delete_key_timeout(self, timeout):
        sqlstr = "DELETE FROM " + self.table + " WHERE atime < %s"
        c = self.db.cursor()
        try:
            c.execute(sqlstr, (timeout,))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            c.close()

    def insert_key(self, key, data):
        sqlstr = "INSERT INTO " + self.table + \
            "(session_id, data) VALUES (%s, %s)"
        c = self.db.cursor()
        try:
            c.execute(sqlstr, (key, data))
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            c.close()
