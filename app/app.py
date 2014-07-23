#!/usr/bin/python
#-*- coding: UTF-8 -*-"
import site
site.addsitedir('/home/jon/code/hiofcommutingserver/app')
site.addsitedir('/usr/lib/python2.7/dist-packages/MySQLdb')
site.addsitedir('/usr/lib/python2.7/dist-packages/')
site.addsitedir('/home/jon/code/hiofcommutingserver/env/lib/python2.7/site-packages')

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, NotFound
from httplib import HTTPException

class App(object):

    def __init__(self):
        self.url_map = Map([
            Rule('/email.py', endpoint='email_login_ep'),
            Rule('/department.py', endpoint='department_ep'),
            Rule('/usr.py', endpoint='usr_ep')
            ])
    
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)
        """text = 'Hello %s!' %request.args.get('name', 'World')
        response = Response(text, mimetype='text/plain')
        return response(environ, start_response)"""

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException, e:
            return e

    def __call__(self,environ, start_response):
        return self.wsgi_app(environ,start_response)

    def email_login_ep(self, request, **values):
        from email_login import login
        return login(request, **values)
    
    def department_ep(self, request, **values):
        from department import department
        return department(request, **values)

    def usr_ep(self, request, **values):
        from usr import get_user
        return get_user(request, **values)

def create_app():
    return App()
