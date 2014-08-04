#!/usr/bin/env python
# coding=utf-8

import pickle
import base64
import uuid
import time
import datetime

import SessionDb.SessionDB


class Session(object):

    def __init__(self, store, handler):
        self._data = {}
        self.store = store
        self.handler = handler


class Store(object):

    def __init__(self, table_name):
        self.sessiondb = SessionDb.SessionDB()

    def encode(self, data):
        pickled = pickle.dumps(data)
        return base64.encodestring(pickled)

    def decode(self, data):
        pickled = base64.decodestring(data)
        return pickle.loads(pickled)

    def __contains__(self, key):
        result = self.sessiondb.check_key(key)
        return result

    def __getitem__(self, key):
        result = self.sessiondb.get_key(key)
        if result:
            now = time.strftime("%Y-%m-%d %H-%M-%S")
            self.sessiondb.update_key_time(key, now)
            
        return self.decode(result)

    def __setitem__(self, key, value):
        data = self.encode(value)
        if key in self:
            self.sessiondb.update_key_data(key, data)
        else:
            self.sessiondb.insert_key(key, data)

    def cleanup(self, timeout):
        timeout = datetime.timedelat(timeout / 24.0 * 60.0 *60.0)
        last = datetime.datetime.now() - timeout
        last = last.strftime("%Y-%m-%d %H-%M-%S") 
        self.sessiondb.delete_key(last)
