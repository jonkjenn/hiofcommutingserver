#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns user ids
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
email = args.getfirst("email", "")

# Fetching id

def usr():
	rowarray = []
	cursor.execute("SELECT user_id FROM email_user where email=\"" + email + "\"" )
	rows = cursor.fetchall()

	for row in rows:
		c = collections.OrderedDict()
		c['user_id'] = row[0]
		rowarray.append(c)

	if rowarray:
		j = json.dumps(rowarray, ensure_ascii=False)
		return j 

print usr()

