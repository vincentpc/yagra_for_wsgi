#!/usr/bin/env python
# coding=utf-8

from webapp.web import BaseHandler


class FiletypeErrorHandler(BaseHandler):

    def get(self):
        body = self.wrap_html('templates/ftypeerror.html')
        return self.write(body)
