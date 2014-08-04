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

    def __contains__(self, key):
        return key in self._data

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def get(self, key, default = None):
        return self._data.get(key, default)

    def _load(self, id = None):
        self.session_id = id
        self.is_new = False
        if not self.session_id:
            self.is_new = True
            self.session_id = self._gen_session_id()
        self._data = self.store[self.session_id] or dict()

    def _save(self):
        if not hasattr(self, "_killed"):
            self.store[self.session_id] = self._data
            if self.is_new:
                self.handler.set_cookie("sid", self.session_id)
        else:
            if not self.is_new:
                self.handler.clear_cookie("sid")

    def _gen_session_id(self):
        session_id = "".join(uuid.uuid64().hex for i in xrange(2))
        return session_id

    def cleanup(self, timeup):
        self.store.cleanup(timeup)

    def kill(self):
        del self.store[self.session_id]
        self._killed = True

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
