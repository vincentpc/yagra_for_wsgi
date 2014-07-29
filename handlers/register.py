#!/usr/bin/env python
# coding=utf-8

from webapp.web import BaseHandler
from model import dbapi


class RegisterHandler(BaseHandler):

    def check_xsrf(self):
        if self.check_xsrf_cookie() == False:
            error = "xsrf invalid"
            self.get(error)

    def get(self, error=""):
        xsrf_token = self.xsrf_from_html()
        params = {'error_info': error, 'xsrf_token': xsrf_token}
        body = self.wrap_html('templates/register.html', params)
        return self.write(body)

    def post(self):
        self.check_xsrf()
        email = self.get_arg('email')
        email = email.strip()
        password = self.get_arg('password')
        password2 = self.get_arg('password2')

        user = dbapi.User()
        error = ""
        print email,password,password2
        if email and password == password2:
            if user.get_user(email) == 0:
                error = "user already exist"
            else:
                result = user.insert_user(email, password)
                if result != -1:
                    self.set_secure_cookie('email', str(email))
                    print "hello set cookie"
                    return self.redirect("/user")
                else:
                    error = "insert falure, try again later"
        else:
            if password != password2:
                error = "password inconsistent"
            else:
                error = "missing argument"

        return self.get(error)
