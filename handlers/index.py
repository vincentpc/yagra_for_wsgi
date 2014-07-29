#!/usr/bin/env python
# coding=utf-8

from webapp.web import BaseHandler
from model import dbapi


class IndexHandler(BaseHandler):

    def get(self, error=""):

        email = self.get_secure_cookie("email")
        user = dbapi.User()
        print email
        if email and user.get_user(email) == 0:
            return self.redirect("/user")
        else:
            self.clear_cookies()
            param = {"error_info": error, "xsrf_token": self.xsrf_from_html()}
            body = self.wrap_html('templates/index.html', param)
            return self.write(body)
