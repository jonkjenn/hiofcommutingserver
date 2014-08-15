#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
        This module handles HTTP requests from the Hiof-commuting app and 
        inserts user credentials to the db.
"""

import json
import collections
import bcrypt
import sql
from werkzeug.wrappers import Response

import logging
log = logging.getLogger(__name__)


def insertEmailUser(request):
    """ User table 
    sid = form.getfirst("sid", "")
    fname = form.getfirst("fname", "")
    sname = form.getfirst("sname", "")
    lon = form.getfirst("lon", "")
    lat = form.getfirst("lat", "")
    car = form.getfirst("car", "")
    if car == 'true':
    car = True
    else:
    car = False
    starting_year = form.getfirst("starting_year", "")

    #Email table 
    email = form.getfirst("email", "")
    pw = form.getfirst("pw", "")"""

    sid = request.form.get('sid')
    fname = request.form.get('fname')
    sname = request.form.get('sname')
    lon = request.form.get('lon')
    lat = request.form.get('lat')
    car = request.form.get('car')
    if car == 'true':
        car = True
    else:
        car = False

    starting_year = request.form.get('starting_year')
    email = request.form.get('email')

    if not email.endswith('@hiof.no'):
        ##log.debug("Wrong email")
        return Response('{test:"test"}', status=400)

    ##log.debug("Args:")
    ##log.debug(request.form)

    pw = request.form.get('pw').encode('utf-8')

    try:
        hpw = bcrypt.hashpw(pw,bcrypt.gensalt())
    except Exception as e:
        #log.exception("Exception: ")
        return Response('{test:"test"}', status=400)

    ##log.debug("Hash: " + hpw)

    db = sql.getdb()
    db.autocommit(False)
    cursor = db.cursor()
    #sqlusr = "insert into user (study_id, firstname, surname, latlon, car, starting_year) values(" + sid + "," + "\"" + fname + "\"," + "\"" + sname + "\",point(" + lat + "," + lon + ")," + car + "," + starting_year +")"
    sqlusr = "insert into user (study_id, firstname, surname, latlon, car, starting_year) values( %s, %s, %s, point(%s, %s), %s, %s)"

    #sqlemail = "insert into email_user values((select user_id from user where firstname=\"" + fname + "\" and surname=\""  + sname +  "\"), \"" + email + "\", \"" + pw + "\")"
    sqlemail = "insert into email_user values(%s, %s, %s)"

    try:
        cursor.execute(sqlusr, (sid,fname,sname,lat,lon,car,starting_year))
        user_id = cursor.lastrowid
        cursor.execute(sqlemail, (user_id,email, hpw))
        db.commit()
        #log.debug("Registration success")
        return Response('{test:"test"}',status=200)
    except Exception as ex:
        #log.exception("Registration failed")
        db.rollback()
        return Response('{test:"test"}',status=400)
