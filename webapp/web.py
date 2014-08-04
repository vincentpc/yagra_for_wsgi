#!/usr/bin/env python
# coding=utf-8

import sys
import os
import cgi
import Cookie
import re
import httplib
import datetime
import calendar
import email.utils
import urlparse
import binascii
import uuid

import webapp.utils as tool
import webapp.session as session
import config


class HttpRequest(object):

    def __init__(self, environ, wsgiinput, meth, uri,
                 query_str, host, headers, cookies=""):
        self.meth = meth
        self.uri = uri
        self.cookies_str = cookies
        self.host = host
        self.headers = headers

        self.path = uri.split("?", 1)[0]
        self.args = {}
        self.files = {}

        form = cgi.FieldStorage(
            fp=wsgiinput,
            environ=environ,
            keep_blank_values=True)
        for key in form.keys():
            item = form[key]
            if item.file:
                self.files[key] = item

            self.args[key] = form.getlist(key)

    def write(self, text):
        sys.stdout.write(text)

    def get_cookies(self):
        if not hasattr(self, "_cookies"):
            self._cookies = Cookie.SimpleCookie()
            if self.cookies_str:
                self._cookies.load(self.cookies_str)
        return self._cookies


class HttpResponse(object):

    def __init__(self, status, header, body):
        self.status = status
        self.header = header
        self.body = body


class TemplateWrapper(object):

    def __init__(self):
        pass

    @staticmethod
    def wrap_html(path, params):
        path = os.path.join(os.path.dirname(__file__), "..", path)
        body = open(path, 'r').read()
        if params:
            body = body % params
        return body


class BaseHandler(object):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__()
        self.app = application
        self.request = request

        self.clear()

    def clear(self):
        self._headers = {
            "Content-Type": "text/html; charset=UTF-8"
        }
        self._status_code = 200

    def set_status(self, status):
        assert status in httplib.responses
        self._status_code = status

    def set_header(self, name, value):
        self._headers[name] = str(value)

    def clear_header(self, name):
        if name in self._headers:
            del self._headers[name]

    def xsrf_token(self):
        if not hasattr(self, "_xsrf_token"):
            token = self.get_cookie("_xsrf")
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                self.set_cookie(name="_xsrf", value=token)
            self._xsrf_token = token
        return self._xsrf_token

    def xsrf_from_html(self):
        return (
            '<input type="hidden" name="_xsrf" value="' +
            self.xsrf_token() + '"/>'
        )

    def check_xsrf_cookie(self):

        token = self.get_arg("_xsrf", None)
        if token == "":
            return False
        if self.xsrf_token() != token:
            return False
        else:
            return True

    def get_cookies(self):
        return self.request.get_cookies()

    def get_cookie(self, name):
        cookies = self.get_cookies()
        if cookies is not None and name in cookies:
            return cookies[name].value
        else:
            return None

    def set_cookie(self, name, value, expires=None,
                   expires_days=None, max_age=None, path="/"):
        if not hasattr(self, "_new_cookie"):
            self._new_cookie = Cookie.SimpleCookie()
        self._new_cookie[name] = value
        if path:
            self._new_cookie[name]["path"] = path
        if max_age:
            self._new_cookie[name]["max_age"] = max_age
        if expires_days is not None and not expires:
            expires = datetime.datetime.utcnow() + datetime.timedelta(
                days=expires_days)
        if expires:
            timestamp = calendar.timegm(expires.utctimetuple())
            format_timestamp = email.utils.formatdate(
                timestamp, localtime=False, usegmt=True)
            self._new_cookie[name]["expires"] = format_timestamp

    def set_secure_cookie(self, name, value, expires_days=7, **kwargs):
        self.set_cookie(
            name, tool.create_signed_value(config.COOKIE_SECRET, name, value),
            expires_days=expires_days, **kwargs)

    def get_secure_cookie(self, name, value=None, max_age=7):
        if value is None:
            value = self.get_cookie(name)
        return (
            tool.decode_signed_value(
                config.COOKIE_SECRET,
                name,
                value,
                max_age=max_age)
        )

    def clear_cookie(self, name):
        # 100 days for expires
        expires = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        self.set_cookie(name, value="", expires=expires)

    def clear_cookies(self):
        all_cookies = self.get_cookies()
        for name in all_cookies:
            self.clear_cookie(name)

    @property
    def session(self):
        if not hasattr(self, "_session"):
            table_name = "session"
            self._session = session.Session(session.Store(table_name), self)
            session_id = self.get_secure_cookie("sid")
            if session_id:
                self._session._load(session_id)
            else:
                self._session._load()
        return self._session

    def session_finalize(self):
        if hasattr(self, "_session"):
            self._session._save()
            self._session.cleanup(86400 * 1)

    def gen_headers(self):
        status_expr = httplib.responses[self._status_code]
        header_line = [
            ("Status", "".join(str(self._status_code) + " " + status_expr))]
        for name, value in self._headers.iteritems():
            header_line.append((name, value))

        if hasattr(self, "_new_cookie"):
            for cookie in self._new_cookie.values():
                header_line.append(("Set-Cookie", cookie.OutputString(None)))

        return header_line

    def get_args(self, name, default=[]):
        args = []
        for arg in self.request.args.get(name, []):
            args.append(arg)
        return args

    def get_arg(self, name, default=[]):
        args = []
        for arg in self.request.args.get(name, []):
            args.append(arg)
        if len(args) >= 1:
            return args[0]
        else:
            return ""

    def redirect(self, url, permanent=False):
        self.set_status(301)
        self.set_header("Location", urlparse.urljoin(self.request.uri, url))
        self.set_header("Cache-Control", "no-cache")
        return self.write()

    def write(self, text=""):
        if isinstance(text, dict):
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        status_expr = httplib.responses[self._status_code]
        resp_status = "".join(str(self._status_code)) + " " + status_expr
        resp_body = text
        resp_header = self.gen_headers()
        resp = HttpResponse(resp_status, resp_header, resp_body)
        #save session here
        self.session_finalize()
        return resp

    def wrap_html(self, path, params=None):
        return TemplateWrapper.wrap_html(path, params)


class ErrorHandler(BaseHandler):

    def get(self):
        self.set_status(404)
        body = "Page Not Found"
        return self.write(body)


class Application(object):

    """web framework for the application"""

    def __init__(self, vars, urls=(), config=()):
        self._urls = urls
        self._config = config
        self._vars = vars

    def get_request(self, environ):

        headers = []

        request = HttpRequest(
            environ,
            environ["wsgi.input"],
            unicode(environ["REQUEST_METHOD"], encoding="utf-8"),
            unicode(environ["REQUEST_URI"], encoding="utf-8"),
            unicode(environ.get("QUERY_STRING"), encoding="utf-8"),
            unicode(environ.get("HTTP_HOST"), encoding="utf-8"),
            headers,
            environ.get("HTTP_COOKIE")

        )

        return request

    def __call__(self, environ, start_response):

        self._request = self.get_request(environ)
        resp = self.delegate(environ)
        start_response(resp.status, resp.header)

        if isinstance(resp.body, basestring):
            return iter([resp.body])
        else:
            return iter(resp.body)

    def delegate(self, environ):
        path = self._request.path
        method = self._request.meth

        for pattern, name in self._urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                args = m.groups()
                func = method.lower()
                cls = self._vars.get(name)
                if hasattr(cls, func):
                    handler = cls(self, self._request)
                    meth = getattr(cls, func)
                    return meth(handler, *args)

        handler = ErrorHandler(self, self._request)
        return handler.get()
