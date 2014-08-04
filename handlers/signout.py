#!/usr/bin/env python
# coding=utf-8

from webapp.web import BaseHandler


class SignoutHandler(BaseHandler):

    def get(self):
        self.clear_cookies()
        self.session.kill()
        return self.redirect("/")

    def post(self):
        self.get()
