#!/usr/bin/python
#-*- coding: UTF-8 -*-"
#site.addsitedir('/home/jon/code/hiofcommutingserver/app')
#site.addsitedir('/usr/lib/python2.7/dist-packages/MySQLdb')
#site.addsitedir('/usr/lib/python2.7/dist-packages/')
#site.addsitedir('/home/jon/code/hiofcommutingserver/env/lib/python2.7/site-packages')

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, NotFound
from httplib import HTTPException

import ConfigParser
import os
Config = ConfigParser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config'))
Config.read(path)
import logging
try:
    logging.basicConfig(filename=Config.get('debug','log'), level=logging.DEBUG)
except:
    pass


class App(object):

    def __init__(self):
        self.url_map = Map([
            Rule('/email.py', endpoint='email_login_ep'),
            Rule('/department.py', endpoint='department_ep'),
            Rule('/usr.py', endpoint='usr_ep'),
            Rule('/usrid.py', endpoint='usrid_ep'),
            Rule('/institution.py', endpoint='institution_ep'),
            Rule('/hcserv.py', endpoint='hcserv_ep'),
            Rule('/regusr.py', endpoint='regusr_ep'),
            Rule('/study.py', endpoint='study_ep'),
            Rule('/regfbusr.py', endpoint='regfbusr_ep'),
            Rule('/delusr.py', endpoint='delusr_ep'),
            Rule('/reggcm.py', endpoint='reggcm_ep'),
            Rule('/update_address.py', endpoint='updateaddress_ep')
            #Rule('/gcm_test', endpoint='gcm_test_ep')
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
        return login(request)
    
    def department_ep(self, request, **values):
        from department import department
        return department(request)

    def usr_ep(self, request, **values):
        from usr import usr,allusrs,fbUserId,emailUser
        q = request.args.get('q')
        if q == 'usr':
            return usr(request)
        elif q == 'allusrs':
            return allusrs(request)
        elif q == 'fbusrid':
            return fbUserId(request)
        elif q == 'emailUser':
            return emailUser(request)

    def usrid_ep(sel, request, **values):
        from usrid import usr
        return usr(request,**values)

    def institution_ep(self, request, **values):
        from institution import institution
        return institution(request,**values)

    def study_ep(self,request,**values):
        from study import study, getAllStudies
        q = request.args.get('q')
        if q == 'study':
            return study(request)
        elif q == 'getAllStudies':
            return getAllStudies(request)

    def hcserv_ep(self, request, **values):
        import hcserv
        q = request.values.get('q')

        if q == 'conversation':
            return hcserv.conversation(request)
        elif q == 'send':
            return hcserv.send(request)
        elif q == 'inbox':
            return hcserv.inbox(request)
        elif q == 'newMessages':
            return hcserv.newMessages(request)
        elif q == 'read':
            return hcserv.read(request)

    def regusr_ep(self, request, **values):
        from regusr import insertEmailUser
        return insertEmailUser(request)

    def regfbusr_ep(self, request, **values):
        from regfbusr import insertFacebookUser
        return insertFacebookUser(request)

    def delusr_ep(self, request, **values):
        from deleteuser import deleteuser
        deleteuser(request)
        return Response('{test:"test"}')

    def reggcm_ep(self, request, **values):
        from reggcm import reggcm
        reggcm(request)
        return Response('{test:"test"}')

    def gcm_test_ep(self, request, **values):
        from hcserv import test
        test()
        return Response('{test:"test"}')

    def updateaddress_ep(self, request, **values):
        from usr import updateAddress
        return updateAddress(request)

def create_app():
    return App()
