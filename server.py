#!/usr/bin/env python2.7
"""
This is the gateway to handle all requests from the frontend.
Pretty much just boilerplate to get the wsgiserver up and running
"""

import argparse
import os
import sys
from importlib import import_module

if __name__ == '__main__':
    from gevent import monkey; monkey.patch_all()
    from gevent.pywsgi import WSGIServer

import web
import mako
from mako.lookup import TemplateLookup
from web.httpserver import StaticMiddleware
from wsgilog import WsgiLog

from dogpile.cache import make_region
from dogpile.cache.util import sha1_mangle_key

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

def key_generator(namespace, fn):
    def generate_key(*arg):
        return "{0}:{1}:{2}|{3}".format('dnd_manager', namespace or '' + fn.__module__,
                                        fn.__name__, ", ".join(str(s) for s in arg))
    return generate_key

LONG_TERM_CACHE = make_region(function_key_generator=key_generator,
                              key_mangler=sha1_mangle_key).configure(
    'dogpile.cache.dbm',
    expiration_time=1800,    # 30 Minutes
    arguments = {
        'filename': '/tmp/dogpile_dnd_manager_cache.dbm'
    }
)

urls = ("/", "Index",
        "/gateway", "Gateway",
        "/.*", "RenderTemplate")

app = web.application(urls, globals())

webpy_db = web.database(dbn='mysql', user='dnd_root', passwd='dnd_root', host='localhost', db='dnd_manager')

session = web.session.Session(app, web.session.DBStore(webpy_db, 'sessions'),
                              initializer={
                                  'uinfo': {
                                      'isGod': False,
                                      'whichSite': 'login',
                                      'username': 'system'
                                  }
                              })

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

class Log(WsgiLog):
    """Child class for WsgiLog, define log format and file log location."""
    def __init__(self, application):
        """Initialize the WsgiLog parent class with configuration options."""
        WsgiLog.__init__(
            self,
            application,
            logformat='%(asctime)s - %(levelname)s - %(message)s',
            tofile=True,
            toprint=True,
            file=os.path.join(os.path.dirname(__file__), 'log', 'debug.log')
        )

class TemplateHandler(object):
    """This class contains all pertinent information about rendering a
    mako template. The TemplateHandler contains the query string arguments, and a
    Mako Template lookup instance. It also has member methods that can be
    evaluated from file contents before being written to the client."""
    def __init__(self, *args, **kwargs):
        """Initialize query_data and a template lookup."""
        self.query_data = web.input()

        if hasattr(web.ctx, 'session'):
            self.uinfo  = web.ctx.session.uinfo
        else:
            self.uinfo = {'isGod': False,
                          'whichSite': 'login',
                          'username': 'system'}

        self.template_lookup = TemplateLookup(directories=[os.path.join(ROOT_PATH, 'templates')],
                                              output_encoding='utf-8', encoding_errors='replace',
                                              cache_impl='dogpile.cache',
                                              cache_args={'regions': {'long_term': LONG_TERM_CACHE}})

    def render(self, path, extension='.html'):
        """This method reads in the contents of the path and renders
        out the contents of the file parsed through mako.lookup.TemplateLookup.

        @param path: The path requested inside the user's web browser.
        @param extension: The extension to append to the given path when rendering the file.
        @return: The actual contents generated for the path."""
        allowed_functions = {k: getattr(self, k) for k in dir(self)}
        if path.endswith('/'):
            path = path[:-1]
        return self.template_lookup.get_template(path + extension).render(**allowed_functions)

    def get_value(self, name):
        """Simple method that returns the value from self.query_data if the
        parameter 'name' is a key in the dictionary.

        @param name: String query string parameter.
        @return: String value of the passed query string parameter."""
        return self.query_data.get(name, '')


class Gateway(BaseResponse):
    """Gateway to the python libraries"""

    def handler(self):

        self.query_data.json = web.data()

        try:
            try:
                module = import_module(self.query_data.file)
            except ValueError:
                print 'Unable to import %s' % self.query_data.file

            meth, args = self.query_data.method, []

            if getattr(self.query_data, 'json', None):
                args.append(self.query_data.json)

            self._return = ('application/json/', getattr(module, meth)(*args))
        except web.HTTPError:
            raise
        except UserWarning as warn:
            self._return = ('text/plain', unicode(warn))
        except:
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
        except mako.exceptions.TemplateLookupException:
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

interface = ''
application = app.wsgifunc(StaticMiddleware)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Starts serving up the dnd_manager stuff.')
    parser.add_argument("--port", "-p", dest='port', help='Port number to run on', type=int, default=8050)
    args = parser.parse_args()

    print 'Server running at %d...' % args.port

    WSGIServer((interface, args.port), application).serve_forever()
