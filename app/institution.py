#!/usr/bin/python
#-*- coding: utf-8 -*-
"""# enable debugging"""

""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns json objects containing user credentials.
"""

import sql
import json
import collections
import validate_login
from werkzeug.wrappers import Response

# Fetching users

def institution(request):

    cursor = sql.getCursor()

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
        return Response(j, mimetype='text/plain')
    return Response("{}", mimetype='text/plain')

"""
Example:
http://frigg.hiof.no/bo14-g23/py/institution.py
"""

