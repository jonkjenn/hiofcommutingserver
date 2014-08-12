#!/usr/bin/python
#-*- coding: UTF-8 -*-"
""" 
This module handles HTTP requests from the Hiof-commuting app and 
returns user ids
"""

import sql
import json
import collections
import validate_login
from werkzeug.wrappers import Response

def usr(request, **values):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    cursor = sql.getCursor()

    fname = request.args.get('fname')
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    rowarray = []
    cursor.execute("SELECT user_id FROM user where firstname=%s and latlon=point(%s,%s)",(fname,lat,lon))
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['user_id'] = row[0]
        rowarray.append(c)

    if rowarray:
        j = json.dumps(rowarray, ensure_ascii=False)
        return Response(j, mimetype='text/plain')

    return Response('{test:"test"}', mimetype='text/plain')
