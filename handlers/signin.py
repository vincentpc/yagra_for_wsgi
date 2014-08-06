#!/usr/bin/env python
# coding=utf-8

import hashlib

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

                #self.set_secure_cookie('email', str(email))
                
                #change to sssion
                m = hashlib.md5()
                m.update(email)
                email_md5 = m.hexdigest()
                self.session["email"] = email
                self.session["email_md5"] = email_md5
                self.set_secure_cookie('sid', self.session.session_id)

                return self.redirect("/user")

            error = "Password Invalid"
        xsrf_token = self.xsrf_from_html()
        param = {"error_info": error, "xsrf_token": xsrf_token}
        body = self.wrap_html('index.html', param)
        return self.write(body)
        # self.redirect("/")
