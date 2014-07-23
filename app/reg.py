#!/usr/bin/python
#-*- coding: UTF-8 -*-"
"""# enable debugging"""

""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns json objects containing dynamic data during the manual registration process. 
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
institution_id = args.getfirst("institution_id", "")
department_id = args.getfirst("department_id", "")


# Fetching departments

rowarray = []

if query == "dep":
	cursor.execute("select department_id,department_name from department where institution_id=" + institution_id)

	rows = cursor.fetchall()

	for row in rows:
		c = collections.OrderedDict()
		c['department_id'] = row[0]
		c['department_name'] = str(row[1])
		rowarray.append(c)

	if rowarray:
		j = json.dumps(rowarray, ensure_ascii=False)
		clean = j.replace("[", "").replace("]","")
		print clean 

"""
Example:
http://frigg.hiof.no/bo14-g23/py/reg.py?q=dep&institution_id=1
"""


# Fetching study

if query == "study":
	cursor.execute("select study_id,name_of_study from study where department_id=" + department_id)

	rows = cursor.fetchall()

	for row in rows:
		c = collections.OrderedDict()
		c['study_id'] = row[0]
		c['name_of_study'] = str(row[1])
		rowarray.append(c)

	if rowarray:
		j = json.dumps(rowarray, ensure_ascii=False)
		clean = j.replace("[", "").replace("]","")
		print clean 

"""
Example:
http://frigg.hiof.no/bo14-g23/py/reg.py?q=study&department_id=2 
"""


