#!/usr/bin/python
#-*- coding: UTF-8 -*-"
# enable debugging

""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns json objects containing user credentials.
"""

import json
import collections
import sql
import validate_login
from werkzeug.wrappers import Response

# Fetching studies

def study(request):
    #if not validate_login.is_logged_in(request):
    #    return validate_login.failed_login()

    cursor = sql.getCursor()

    rowarray = []
    cursor.execute("SELECT study_id, institution_name, campus_name, department_name, name_of_study FROM study INNER JOIN department ON study.department_id = department.department_id INNER JOIN campus ON study.campus_id = campus.campus_id INNER JOIN institution ON department.institution_id = institution.institution_id")
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['study_id'] = row[0]
        c['institution_name'] = row[1]
        c['campus_name'] = row[2]
        c['department_name'] = row[3]
        c['name_of_study'] = row[4]
        rowarray.append(c)

    if rowarray:
        j = json.dumps(rowarray, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    return Response("{}", mimetype='text/plain')
		
def getAllStudies(request):
    #if not validate_login.is_logged_in(request):
    #    return validate_login.failed_login()

    cursor = sql.getCursor()

    rowarray = []
    cursor.execute("SELECT * FROM study")
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['study_id'] = row[0]
        c['department_id'] = row[1]
        c['campus_id'] = row[2]
        c['name_of_study'] = row[3]
        rowarray.append(c)

    if rowarray:
        j = json.dumps(rowarray, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    return Response("{}", mimetype='text/plain')

"""
Example:
frigg.hiof.no/bo14-g23/py/study.py?q=study&study_id=1
"""


