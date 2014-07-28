#!/usr/bin/env python
# coding=utf-8

from webapp.web import BaseHandler


class ErrorHandler(BaseHandler):

    def get(self):
        self.write("Page Not Exist")
