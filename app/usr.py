#!/usr/bin/python
#-*- coding: UTF-8 -*-"
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
import facebook

def usr(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    cursor = sql.getCursor()
    rowarray = []
    cursor.execute("SELECT user_id, study_id, firstname, surname, AsText(latlon), car, starting_year FROM user")
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['user_id'] = row[0]
        c['study_id'] = row[1]
        c['firstname'] = str(row[2])
        c['surname'] = str(row[3])
        c['latlon'] = str(row[4])
        c['car'] = row[5]
        c['starting_year'] = row[6]
        rowarray.append(c)

    if rowarray:
        j = json.dumps(rowarray, ensure_ascii=False)
        return Response(j,mimetype='text/plain')
    return Response("{}")


# Fetching all users with studies

def allusrs(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    cursor = sql.getCursor()

    rowarray = []
    cursor.execute("SELECT user.user_id, user.study_id, firstname, surname, AsText(latlon), car, starting_year, institution_name, campus_name, department_name, name_of_study, facebook_id FROM user INNER JOIN study ON user.study_id = study.study_id INNER JOIN department ON study.department_id = department.department_id INNER JOIN campus ON study.campus_id = campus.campus_id INNER JOIN institution ON department.institution_id = institution.institution_id LEFT JOIN facebook_user ON user.user_id = facebook_user.user_id")
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['user_id'] = row[0]
        c['study_id'] = row[1]
        c['firstname'] = str(row[2])
        c['surname'] = str(row[3])
        c['latlon'] = str(row[4])
        c['car'] = row[5]
        c['starting_year'] = row[6]
        c['institution_name'] = str(row[7])
        c['campus_name'] = str(row[8])
        c['department_name'] = str(row[9])
        c['name_of_study'] = str(row[10])
        c['facebook_id'] = str(row[11])
        rowarray.append(c)

    if rowarray:
        j = json.dumps(rowarray, ensure_ascii=False)
        return Response(j, mimetype='text/plain')

def fbUserId(request):
    import urllib2
    #if not validate_login.is_logged_in(request):
    #    return validate_login.failed_login()

    cursor = sql.getCursor()
    fid = request.args.get('fbid')
    token = request.args.get('token')

    print request.args

    handler = urllib2.urlopen('https://graph.facebook.com/me?fields=id&access_token=' + token)

    print "graph:"
    print handler.getcode()
    print handler.read()

    rowarray = []
    cursor.execute("SELECT user_id, user.study_id, firstname, surname, AsText(latlon) as latlon, institution.institution_name, campus.campus_name, department.department_name, name_of_study, starting_year, car FROM user INNER JOIN study ON user.study_id = study.study_id INNER JOIN campus ON study.campus_id = campus.campus_id ""INNER JOIN department ON study.department_id = department.department_id INNER JOIN institution ON department.institution_id = institution.institution_id WHERE user_id = (SELECT user_id FROM facebook_user WHERE facebook_id=%s)",(fid))
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['user_id'] = row[0]
        c['study_id'] = row[1]
        c['firstname'] = str(row[2])
        c['surname'] = str(row[3])
        c['latlon'] = str(row[4])
        c['institution_name'] = str(row[5])
        c['campus_name'] = str(row[6])
        c['department_name'] = str(row[7])
        c['name_of_study'] = str(row[8])
        c['starting_year'] = row[9]
        c['car'] = row[10]
        rowarray.append(c)

    if rowarray:
        j = json.dumps(rowarray, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    else:
        return Response('[{"user_id": -100, "study_id": null, "firstname": "null", "surname": "null", "latlon": "null", "institution_name": "null", "campus_name": "null", "department_name": "null", "name_of_study": "null", "starting_year": null, "car": null}]',mimetype='text/plain')
	
def emailUser(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    cursor = sql.getCursor()

    email = request.args.get('email')

    rowarray = []
    #cursor.execute("SELECT user_id, user.study_id, firstname, surname, AsText(latlon) as latlon, institution.institution_name, campus.campus_name, department.department_name, name_of_study, starting_year, car FROM user INNER JOIN study ON user.study_id = study.study_id INNER JOIN campus ON study.campus_id = campus.campus_id ""INNER JOIN department ON study.department_id = department.department_id INNER JOIN institution ON department.institution_id = institution.institution_id WHERE user_id = (SELECT user_id FROM email_user WHERE email=%s)",(email))
    cursor.execute("SELECT user_id, user.study_id, firstname, surname, AsText(latlon) as latlon, institution.institution_name, campus.campus_name, department.department_name, name_of_study, starting_year, car FROM user INNER JOIN study ON user.study_id = study.study_id INNER JOIN campus ON study.campus_id = campus.campus_id ""INNER JOIN department ON study.department_id = department.department_id INNER JOIN institution ON department.institution_id = institution.institution_id WHERE user_id = (SELECT user_id FROM session WHERE user_id=%s LIMIT 1)",(request.user_id))
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['user_id'] = row[0]
        c['study_id'] = row[1]
        c['firstname'] = str(row[2])
        c['surname'] = str(row[3])
        c['latlon'] = str(row[4])
        c['institution_name'] = str(row[5])
        c['campus_name'] = str(row[6])
        c['department_name'] = str(row[7])
        c['name_of_study'] = str(row[8])
        c['starting_year'] = row[9]
        c['car'] = row[10]
        rowarray.append(c)

    if rowarray:
        j = json.dumps(rowarray, ensure_ascii=False)
        return Response(j, mimetype='text/plain')

    return Response("{}", mimetype='text/plain')

"""
Example:
http://frigg.hiof.no/bo14-g23/py/reg.py?q=dep&institution_id=1

http://frigg.hiof.no/bo14-g23/py/usr.py?q=usr
"""
