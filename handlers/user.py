#!/usr/bin/env python
# coding=utf-8

import hashlib
import os

from webapp.web import BaseHandler
from model import dbapi


class UserHandler(BaseHandler):

    def check(self):
        email = self.get_secure_cookie("email")
        user = dbapi.User()
        if email and user.get_user(email) == 0:
            profile = user.get_user_all(email)
            if profile:
                self.time = profile[4].date()
                self.email = email
        else:
            self.clear_cookies()
            return self.redirect("/")

    def get(self):
        self.check()

        m = hashlib.md5()
        m.update(self.email)
        email_md5 = m.hexdigest()
        fn = "images/" + email_md5
        path = os.path.join(os.path.dirname(__file__), "..", fn)
        if os.path.isfile(path):
            imagetag =  """<img src="%s" height="400"  class="rounded" alt="Upload Image Below">""" % fn 
        else:
            imagetag = """<p class="text-warning">Avatar Not Available. Upload One!</p>""" + \
                """<img src="static/default.jpg" height="400"  class="rounded" alt="Upload Image Below">"""
        xsrf_token = self.xsrf_from_html()
        params = {'name': self.email, 'time': self.time, 'image': imagetag, 'xsrf_token': xsrf_token}
        body = self.wrap_html('templates/user.html', params)
        return self.write(body)
