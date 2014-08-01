#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
        This module handles HTTP requests from the Hiof-commuting app and 
        inserts user credentials to the db.
"""

import MySQLdb
import json
import collections
import sys
sys.path.append("/home/jon/code/hiofcommutingserver/env/lib/python2.7/site-packages")
import bcrypt
import sql



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
    pw = request.form.get('pw').encode('utf-8')

    hpw = bcrypt.hashpw(pw,bcrypt.gensalt())

    db = sql.getdb()
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
    except MySQLdb.Error, e:
        print e
        db.rollback()       
    except Exception as ex:
        print ex
        db.rollback()       
