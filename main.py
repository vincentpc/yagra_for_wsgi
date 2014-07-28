#!/usr/bin/env python
# coding=utf-8

from webapp.web import Application
from handlers.index import IndexHandler
from handlers.register import RegisterHandler
from handlers.user import UserHandler
from handlers.signin import SigninHandler
from handlers.signout import SignoutHandler
from handlers.upload import UploadHandler
from handlers.avatar import AvatarHandler
from handlers.error import ErrorHandler
from handlers.password import PasswordHandler
from handlers.ftypeerror import FiletypeErrorHandler


URLS = (
    ("/", "IndexHandler"),
    ("/register?", "RegisterHandler"),
    ("/user", "UserHandler"),
    ("/signin", "SigninHandler"),
    ("/signout", "SignoutHandler"),
    ("/upload", "UploadHandler"),
    ("/avatar/(.*)", "AvatarHandler"),
    ("/error", "ErrorHandler"),
    ("/pwdchange", "PasswordHandler"),
    ("/ftypeerror", "FiletypeErrorHandler")
)


if __name__ == '__main__':
    app = Application(globals(), URLS)
    app.run()
