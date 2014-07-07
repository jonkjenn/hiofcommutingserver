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


# DOCTYPE
print "Content-type: text/plain;charset=utf-8"
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
starting_year = args.getfirst("starting_year", "")

""" Email table """
email = args.getfirst("email", "")
pw = args.getfirst("pw", "")
	
def insertEmailUser():
	sqlusr = "insert into user (study_id, firstname, surname, latlon, car, starting_year) values(" + sid + "," + "\"" + fname + "\"," + "\"" + sname + "\",point(" + lat + "," + lon + ")," + car + "," + starting_year +")"

	sqlemail = "insert into email_user values((select user_id from user where firstname=\"" + fname + "\" and surname=\""  + sname +  "\"), \"" + email + "\", \"" + pw + "\")"

	try:
		cursor.execute(sqlusr)
		cursor.execute(sqlemail)
		db.commit()
	except:
		db.rollback()	

insertEmailUser()
