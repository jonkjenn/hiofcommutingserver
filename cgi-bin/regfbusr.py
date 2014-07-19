#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
	This module handles HTTP requests from the Hiof-commuting app and 
	inserts user credentials to the db.
"""

import cgi
"""import cgitb; cgitb.enable()"""
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
query = args.getfirst("q", "")

""" User table """
sid = args.getfirst("sid", "")
fname = args.getfirst("fname", "")
sname = args.getfirst("sname", "")
lon = args.getfirst("lon", "")
lat = args.getfirst("lat", "")
starting_year = args.getfirst("starting_year", "")
car = args.getfirst("car", "")

""" facebook table """
fbid = args.getfirst("fbid", "")


def insertFacebookUser():
	sqlusr = "insert into user (study_id, firstname, surname, latlon,starting_year, car) values(" + sid + "," + "\"" + fname + "\"," + "\"" + sname + "\",point(" + lat + "," + lon + ")," + starting_year + "," + car + ")"

	sqlfb = "insert into facebook_user values((select user_id from user where firstname=\"" + fname + "\" and surname=\""  + sname +  "\"), \"" + fbid + "\")"
	
	try:
		cursor.execute(sqlusr)
		cursor.execute(sqlfb)
		db.commit()
	except:
		db.rollback()	

		
if query == "facebookUser":	
	insertFacebookUser()
	

	
