#!/usr/bin/env python
# coding=utf-8

from webapp.web import BaseHandler


class ErrorHandler(BaseHandler):

    def get(self):
        error = "Page Not Found "
        return self.write(error)
