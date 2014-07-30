#!/usr/bin/python
#-*- coding: utf-8 -*-
"""# enable debugging"""

""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns json objects containing user credentials.
"""

import json
import collections
import sql
import validate_login
from werkzeug.wrappers import Response

cursor = sql.getCursor()

# Fetching departments

def department(request):

    rowarray = []
    cursor.execute("select * from department")
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['department_id'] = row[0]
        c['institution_id'] = row[1]
        c['department_name'] = row[2]
        rowarray.append(c)

    if rowarray:
        return Response(json.dumps(rowarray, ensure_ascii=False), mimetype='text/plain')
    return Response("{}",mimetype='text/plain')

"""
Example:
http://frigg.hiof.no/bo14-g23/py/department.py
"""
