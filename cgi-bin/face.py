#!/usr/bin/python
#-*- coding: UTF-8 -*-"
"""# enable debugging"""

"""
  This module handles HTTP requests from the Hiof-commuting app and
  returns json objects containing user credentials.
  
  Using -300 as error code for wrong facebook_id.
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
fid = args.getfirst("fid", "")

# Facebook ID check

ar = []
c = collections.OrderedDict()
if query == "face":
	if cursor.execute("select user_id from facebook_user where facebook_id=" + "\"" + fid + "\""):
		row = cursor.fetchall()
		c['user_id'] = row[0]
		ar.append(c)
		print json.dumps(ar).replace("[", "").replace("]", "")
	else:
		c['user_id'] = -300
		ar.append(c)
		print json.dumps(ar).replace("[", "").replace("]", "")

