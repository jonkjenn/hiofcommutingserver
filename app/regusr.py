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
    sid = args.getfirst("sid", "")
    fname = args.getfirst("fname", "")
    sname = args.getfirst("sname", "")
    lon = args.getfirst("lon", "")
    lat = args.getfirst("lat", "")
    car = args.getfirst("car", "")
    if car == 'true':
    car = True
    else:
    car = False
    starting_year = args.getfirst("starting_year", "")

    #Email table 
    email = args.getfirst("email", "")
    pw = args.getfirst("pw", "")"""

    sid = request.args.get('sid')
    fname = request.args.get('fname')
    sname = request.args.get('sname')
    lon = request.args.get('lon')
    lat = request.args.get('lat')
    car = request.args.get('car')
    if car == 'true':
        car = True
    else:
        car = False

    starting_year = request.args.get('starting_year')
    email = request.args.get('email')
    pw = request.args.get('pw').encode('utf-8')

    hpw = bcrypt.hashpw(pw,bcrypt.gensalt())

    db = sql.getdb()
    cursor = db.cursor()
    #sqlusr = "insert into user (study_id, firstname, surname, latlon, car, starting_year) values(" + sid + "," + "\"" + fname + "\"," + "\"" + sname + "\",point(" + lat + "," + lon + ")," + car + "," + starting_year +")"
    sqlusr = "insert into user (study_id, firstname, surname, latlon, car, starting_year) values( %s, %s, %s, point(%s, %s), %s, %s)"

    #sqlemail = "insert into email_user values((select user_id from user where firstname=\"" + fname + "\" and surname=\""  + sname +  "\"), \"" + email + "\", \"" + pw + "\")"
    sqlemail = "insert into email_user values((select user_id from user where firstname=%s and surname=%s), %s, %s)"

    try:
        cursor.execute(sqlusr, (sid,fname,sname,lat,lon,car,starting_year))
        cursor.execute(sqlemail, (fname, sname,email, hpw))
        db.commit()
    except MySQLdb.Error, e:
        print e
        db.rollback()       
    except Exception as ex:
        print ex
        db.rollback()       
