#!/usr/bin/env python
# coding=utf-8

import os
import imghdr
import mimetypes

from webapp.web import BaseHandler


class AvatarHandler(BaseHandler):

    def get(self, name):
        fullpath = "images/" + name
        filetype = "jpeg"
        if os.path.isfile("images/" + name):
            with open(fullpath, "rb") as f:
                image = f.read()
                length = len(image)
                self.set_header("Content-Length", length)
                filetype = imghdr.what(fullpath)
            mtype = mimetypes.types_map.get("." + filetype, "image/jpeg")
            self.set_header("Content-Type", mtype)
            self.write(image)
        else:
            self.redirect("/error")

    def post(self, name):
        self.get(name)
        
