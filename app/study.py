#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns json objects containing user credentials.
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
query = args.getfirst("q", "")


# Fetching studies

def study():
	rowarray = []
	cursor.execute("SELECT study_id, institution_name, campus_name, department_name, name_of_study FROM study INNER JOIN department ON study.department_id = department.department_id INNER JOIN campus ON study.campus_id = campus.campus_id INNER JOIN institution ON department.institution_id = institution.institution_id")
	rows = cursor.fetchall()

	for row in rows:
		c = collections.OrderedDict()
		c['study_id'] = row[0]
		c['institution_name'] = row[1]
		c['campus_name'] = str(row[2])
		c['department_name'] = str(row[3])
		c['name_of_study'] = str(row[4])
		rowarray.append(c)

	if rowarray:
		j = json.dumps(rowarray, ensure_ascii=False)
		return j 
		
def getAllStudies():
	rowarray = []
	cursor.execute("SELECT * FROM study")
	rows = cursor.fetchall()

	for row in rows:
		c = collections.OrderedDict()
		c['study_id'] = row[0]
		c['department_id'] = row[1]
		c['campus_id'] = str(row[2])
		c['name_of_study'] = str(row[3])
		rowarray.append(c)

	if rowarray:
		j = json.dumps(rowarray, ensure_ascii=False)
		return j 		


if query == "study":
	print study()

if query == "getAllStudies":
	print getAllStudies()
"""
Example:
frigg.hiof.no/bo14-g23/py/study.py?q=study&study_id=1
"""


