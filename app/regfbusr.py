#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
	This module handles HTTP requests from the Hiof-commuting app and 
	inserts user credentials to the db.
"""

import sql
import json
import collections
import validate_login
from werkzeug.wrappers import Response
import face

# form
""" User table 
sid = form.getfirst("sid", "")
fname = form.getfirst("fname", "")
sname = form.getfirst("sname", "")
lon = form.getfirst("lon", "")
lat = form.getfirst("lat", "")
starting_year = form.getfirst("starting_year", "")
car = form.getfirst("car", "")
"""

""" facebook table """
#fbid = form.getfirst("fbid", "")


def insertFacebookUser(request):
    from MySQLSessionStore import MySQLSessionStore
    session_store = MySQLSessionStore()

    token = request.form.get('token')

    print request.form

    fid = face.valid_face(token)
    if not fid:
        return

    sid = request.form.get('sid')
    fname = request.form.get('fname')
    sname = request.form.get('sname')
    lon = request.form.get('lon')
    lat = request.form.get('lat')
    starting_year = request.form.get('starting_year')
    car = request.form.get('car')
    if car == 'true':
        car = True
    else:
        car = False

    #sqlusr = "insert into user (study_id, firstname, surname, latlon,starting_year, car) values(" + sid + "," + "\"" + fname + "\"," + "\"" + sname + "\",point(" + lat + "," + lon + ")," + starting_year + "," + car + ")"
    sqlusr = "insert into user (study_id, firstname, surname, latlon,starting_year, car) values(%s,%s,%s, point(%s,%s), %s, %s)"

    #sqlfb = "insert into facebook_user values((select user_id from user where firstname=\"" + fname + "\" and surname=\""  + sname +  "\"), \"" + fbid + "\")"
    sqlfb = "insert into facebook_user values(%s, %s)"

    db = sql.getdb()

    success = False

    try:
        cursor = db.cursor()
        cursor.execute(sqlusr, (sid, fname, sname, lat, lon, starting_year,car ))
        user_id = cursor.lastrowid
        print user_id
        print fid
        cursor.execute(sqlfb, (user_id, fid))
        db.commit()
        success = True
    except Exception as ex:
        print ex
        db.rollback()       
        success = False

    if success:
        user_id = session_store.get_userid_from_face(fid)

        import datetime
        request.session = session_store.session_new("",user_id)
        response = Response("",mimetype='text/plain')
        response.set_cookie('hccook', value=request.session.sid, max_age=3600*24*4, expires=datetime.datetime.utcnow() + datetime.timedelta(days=4))
        return response
    else:
        return Response('{test:"test"}')
