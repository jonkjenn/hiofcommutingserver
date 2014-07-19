#!/usr/bin/python
#-*- coding: UTF-8 -*-"
"""# enable debugging"""

"""
  This module handles HTTP requests from the Hiof-commuting app and
  returns json objects containing user credentials.
  
  Using -100 as error code for wrong/misspelled/missing email address.
  Using -200 as error code for wrong/misspelled/missing password.
"""

import cgi
"""import cgitb; cgitb.enable()"""
import MySQLdb
import json
import collections
import sys
sys.path.append("/home/jon/code/hiofcommutingserver/env/lib/python2.7/site-packages")
import bcrypt
import logging


logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


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
email = args.getfirst("email", "")
password = args.getfirst("pass", "")

# Email validity check

ar = []
c = collections.OrderedDict()
if query == "login":
	#if cursor.execute("select email from email_user where email=" + "\"" + email + "\""):
        cursor.execute("select email from email_user where email=%s", (email))
        row1 = cursor.fetchone()
        logger.debug("Checking if email exists")
        logger.debug(row1)
        if row1 is not None:
                logger.debug("Checking if password is correct")
		#if cursor.execute("select user_id from email_user where email=" + "\"" + email + "\" and password=" + "\"" + password + "\""):
	        cursor.execute("select user_id,password from email_user where email=%s", (email))
                row = cursor.fetchone()
                logger.debug(row)
                if row is not None and bcrypt.hashpw(password,row[1]) == row[1]:
			c['user_id'] = row[0]
			ar.append(c)
			print json.dumps(ar)
		else:
			c['user_id'] = -200
			ar.append(c)
			print json.dumps(ar)
	else:
		c['user_id'] = -100
		ar.append(c)
		print json.dumps(ar)
cursor.close()
db.close()
