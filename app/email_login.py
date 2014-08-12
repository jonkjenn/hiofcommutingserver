
#!/usr/bin/python
#-*- coding: UTF-8 -*-"
"""# enable debugging"""

"""
This module handles HTTP requests from the Hiof-commuting app and
returns json objects containing user credentials.
Using -100 as error code for wrong/misspelled/missing email address.
Using -200 as error code for wrong/misspelled/missing password.
"""

import json
import collections
import bcrypt
import sql
from werkzeug.wrappers import Response
from MySQLSessionStore import MySQLSessionStore

import logging
log = logging.getLogger(__name__)

cursor = sql.getCursor()
session_store = MySQLSessionStore()


def email_exists(email):
    cursor.execute("select COUNT(1) from email_user where email=%s", (email))
    if cursor.fetchone()[0]:
        return True
    return False

def check_login(email, password):
    cursor.execute("select user_id,password from email_user where email=%s", (email))
    row = cursor.fetchone()
    #log.debug("Row:")
    #log.debug(row)
    hashpw = row[1]
    #log.debug("Hashpw: " + hashpw)
    h = bcrypt.hashpw(password,hashpw)
    #log.debug("h: " + h)
    if row[0] and h == hashpw:
        return row[0]
    return None

def login(request, **values):

    sid = request.cookies.get('hccook')

    if sid:
        log.debug("Found session cookie sid: " + sid)
        if session_store.session_valid(sid):
            log.debug("Trying session login")
            user_id = session_store.get_userid(sid)
            return login_success(user_id,sid = sid, send_cookie = False)

    if 'email' in request.args and 'pass' in request.args:
        log.debug("Trying credentials login:")
        log.debug(request.args)
        email = request.args.get('email')
        password = request.args.get('pass').encode('utf-8')

        if email_exists(email):
            #log.debug("Email exists")
            user_id = check_login(email, password)
            if user_id:
                #log.debug("Found user id")
                request.session = session_store.session_new("",user_id)
                return login_success(user_id, sid = request.session.sid, send_cookie = True)
    return login_fail()

def login_fail():
    #log.debug("Login failed")
    c = collections.OrderedDict()
    ar = []

    c['user_id'] = -200
    ar.append(c)
    return Response(json.dumps(ar), mimetype='text/plain', status=400)

def login_success(user_id,sid=None,send_cookie=False):
    #log.debug("Login success")
    c = collections.OrderedDict()
    ar = []

    c['user_id'] = user_id
    ar.append(c)
    response = Response(json.dumps(ar), mimetype='text/plain')
    if send_cookie:
        import datetime
        response.set_cookie('hccook', value=sid, max_age=3600*24*4, expires=datetime.datetime.utcnow() + datetime.timedelta(days=4))
    return response

