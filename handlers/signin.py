#!/usr/bin/env python
# coding=utf-8

from webapp.web import BaseHandler
from model import dbapi


class SigninHandler(BaseHandler):

    def post(self):
        email = self.get_arg("email")
        email = email.strip()
        password = self.get_arg("password")
        if self.check_xsrf_cookie() == False:
            error = "Xsrf Token Invalid, Try Again"
        elif email:
            user = dbapi.User()
            if user.check_user(email, password) == 0:
                self.set_secure_cookie('email', str(email))
                self.redirect("/user")

            error = "Password Invalid"
        xsrf_token = self.xsrf_from_html()
        param = {"error_info": error, "xsrf_token": xsrf_token}
        body = self.wrap_html('templates/index.html', param)
        self.write(body)
        # self.redirect("/")
