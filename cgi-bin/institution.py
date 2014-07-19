#!/usr/bin/python
#-*- coding: utf-8 -*-
"""# enable debugging"""

""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns json objects containing user credentials.
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


# Fetching users

def institution():
	rowarray = []
	cursor.execute("select * from institution")
	rows = cursor.fetchall()

	for row in rows:
		c = collections.OrderedDict()
		c['institution_id'] = row[0]
		c['institution_name'] = row[1]
		rowarray.append(c)

	if rowarray:
		j = json.dumps(rowarray, ensure_ascii=False)
		return j 

print institution()

"""
Example:
http://frigg.hiof.no/bo14-g23/py/institution.py
"""
