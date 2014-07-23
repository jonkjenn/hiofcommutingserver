#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
        This module handles HTTP requests from the Hiof-commuting app and 
        inserts user credentials to the db.
"""

import cgi
import cgitb; cgitb.enable()
import MySQLdb
import json
import collections
import sys
sys.path.append("/home/jon/code/hiofcommutingserver/env/lib/python2.7/site-packages")
import bcrypt
import logging


logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


# DOCTYPE
print "Content-type: text/html;charset=utf-8"
print 

# SQL connection and cursor
db = MySQLdb.connect("localhost", "bo14g23", "bo14g23MySqL", "bo14g23")
db.set_character_set('utf8')
cursor = db.cursor()


# Args
args = cgi.FieldStorage()

""" User table """
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
logger.debug(car)
starting_year = args.getfirst("starting_year", "")

""" Email table """
email = args.getfirst("email", "")
pw = args.getfirst("pw", "")
logger.debug("Hashing password")
hpw = bcrypt.hashpw(pw,bcrypt.gensalt())
logger.debug("Hash: " + hpw)

def insertEmailUser():
    logger.debug("insertEmailUser")
    #sqlusr = "insert into user (study_id, firstname, surname, latlon, car, starting_year) values(" + sid + "," + "\"" + fname + "\"," + "\"" + sname + "\",point(" + lat + "," + lon + ")," + car + "," + starting_year +")"
    sqlusr = "insert into user (study_id, firstname, surname, latlon, car, starting_year) values( %s, %s, %s, point(%s, %s), %s, %s)"

    #sqlemail = "insert into email_user values((select user_id from user where firstname=\"" + fname + "\" and surname=\""  + sname +  "\"), \"" + email + "\", \"" + pw + "\")"
    sqlemail = "insert into email_user values((select user_id from user where firstname=%s and surname=%s), %s, %s)"

    try:
        logger.debug("sqlusr")
        cursor.execute(sqlusr, (sid,fname,sname,lat,lon,car,starting_year))
        logger.debug("sqlemail")
        cursor.execute(sqlemail, (fname, sname,email, hpw))
        logger.debug("committing")
        db.commit()
        logger.debug("Comitted")
        logger.debug(cursor._executed)
    except MySQLdb.Error, e:
        logger.debug("MYSQL Error")
        logger.debug("MySQL Error %d: %s" % (e.args[0], e.args[1]))
        db.rollback()       
    except Exception:
        logger.debug("exception", exc_info=True)
        logger.debug("Unknown error")
        logger.debug(ee)
        db.rollback()       

insertEmailUser()
