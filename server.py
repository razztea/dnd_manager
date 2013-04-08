#!/usr/bin/env python2.7
"""
This is the gateway to handle all requests from the frontend.
"""

import argparse
import locale
import os
import sys
import traceback
from importlib import import_module
import web

urls = ("/", "Index",
        "/gateway", "Gateway")

app = web.application(urls, globals())

webpy_db = web.database(dbn='mysql', user='dnd_root', passwd='dnd_root', host='localhost', db='dnd_manager')

class BaseResponse(object):
    """Base Response class for returning content to client."""

    def __init__(self):
        self._return = None
        self.is_auth = False
        self.query_data = web.input()

    def return_to_client(self):

        web.header('Content-type', self._return[0] + '; charset=UFT-8', unique=True)

        try:
            return self._return[1].encode('utf-8')
        except (AttributeError, UnicodeDecodeError, UnicodeEncodeError):
            return self._return[1]

class Gateway(BaseResponse):
    """Gateway to the python libraries"""

    def handler(self):

        response_is = ''
        self.query_data.json = web.data()

        try:
            try:
                module = import_module(self.query_data.file)
            except ValueError:
                print 'Unable to import %s' % query_data.file

            meth, args = self.query_data.method, []

            if getattr(self.query_data, 'json', None):
                args.append(self.query_data.json)

            self._return = ('application/json/', gettatr(module, meth)(*args))
            response_is = 'json'
        except web.HTTPError:
            raise
        except UserWarning as warn:
            self._return = ('text/plain', unicode(warn))
            response_is = 'user warning'
        except:
            response_is = 'Other Error'
            raise

        return self.return_to_client()

    def GET(self):
        return self.handler()

    def POST(self):
        return self.handler()

class RenderTemplate(BaseResponse):
    """Renders HTML stuffs"""

    def handler(self):
        """Return rendered HTML to client"""
        try:
            self._return = ('text/html', TemplateHandler().render(web.ctx.path))
        except mako.exceptions.TemplaceLookupException:
            raise

        return self.return_to_client()

    def GET(self):
        return self.handler()

    def POST(self):
        return self.handler()

class Index(BaseResponse):
    def handler(self):
        self._return = ('text/html', TemplateHandler().render('/home'))
        return self.return_to_client()

    def GET(self):
        return self.handler()

    def POST(self):
        return self.handler()

interface = '127.0.0.1'
application = app.wsgifunc(Log)

if __name__ == 'main':

    parser = argparse.ArguementParser(description='Starts serving up the dnd_manager stuff.')
    parser.add_argument("--port", "-p", dest='port', help='Port number to run on', type=int, default=8000)
    args = parser.parse_args()

    print 'Server running at %d...' % args.port

    WSGIServer((interface, args.port), application).serve_forever()
