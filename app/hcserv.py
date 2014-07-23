#!/usr/bin/python
#-*- coding: UTF-8 -*-
"""# enable debugging"""

"""
This module handles HTTP requests from the Hiof-commuting app and
returns json objects containing messages sendt between users.
"""

import cgi
"""import cgitb; cgitb.enable()"""
import MySQLdb
import json
import collections


# Doctype
print "Content-type: text/plain;charset=utf-8"
print

# SQL connection and cursor
db = MySQLdb.connect("localhost", "bo14g23", "bo14g23MySqL", "bo14g23")
db.set_character_set('utf8')
cursor = db.cursor()

# Args
args = cgi.FieldStorage()
query = args.getfirst("q", "")
user_id_sender = args.getfirst("user_id_sender", "")
user_id_receiver = args.getfirst("user_id_receiver", "")
message = args.getfirst("message", "")


# To use in the conversation activity where both senderID and receiverID is known

rowarrayc = []

if query == "conversation":
	#cursor.execute("select * from message where user_id_sender IN(" + user_id_sender + "," +  user_id_receiver + ") and user_id_receiver IN(" + user_id_sender + "," + user_id_receiver + ") order by sent ASC")
	cursor.execute("select * from message where user_id_sender IN(%s, %s) and user_id_receiver IN(%s, %s) order by sent ASC", (user_id_sender, user_id_receiver, user_id_sender, user_id_receiver))
	
	rows = cursor.fetchall()
	
	for row in rows:
		c = collections.OrderedDict()
		c['user_id_sender'] = row[0]
		c['user_id_receiver'] = row[1]
		c['message'] = str(row[2])
		c['sent'] = str(row[3])
		c['read'] = str(row[4])
		rowarrayc.append(c)

if rowarrayc:
	print json.dumps(rowarrayc, ensure_ascii=False)

"""
Example:
http://frigg.hiof.no/bo14-g23/hcserv.py?q=conversation&user_id_sender=3&user_id_receiver=4
"""


# To use in inbox activity where only receiverID is known

rowarrayi = []

if query == "inbox":
	cursor.execute("SELECT * FROM message inner join (select * from message WHERE `user_id_receiver` = "+ user_id_receiver +" order by sent desc) a on (message.user_id_sender=a.user_id_sender) group by message.user_id_sender order by a.sent desc")
	rows = cursor.fetchall()

	for row in rows:
		c = collections.OrderedDict()
		c['user_id_sender'] = row[5]
		c['message'] = str(row[7])
		c['sent'] = str(row[8])
		rowarrayi.append(c)

	if rowarrayi:
		print json.dumps(rowarrayi, ensure_ascii=False)

"""
Example:
http://frigg.hiof.no/bo14-g23/hcserv.py?q=inbox&user_id_receiver=4
"""


# To use when sending message

if query == "send":
	print message
	cursor.execute("insert into message(user_id_sender, user_id_receiver, message, sent) values(" + user_id_sender + "," + user_id_receiver + "," + "\"" + message + "\"" + ", current_timestamp)" )
	cursor.close()
	db.commit()
	db.close()

"""
Example:
http://localhost/cgi-bin/server.cgi?q=send&user_id_sender=3&user_id_receiver=4&message=Hei%20du
"""


#To use when message is read (inserting datetime)

if query == "read":
    cursor.execute("update message set `read`=current_timestamp where user_id_sender=" + user_id_sender + " and user_id_receiver=" + user_id_receiver + " and `read` is NULL")
    cursor.close()
    db.commit()
    db.close()

"""
Example:
http://localhost/cgi-bin/server.cgi?q=read&user_id_sender=3&user_id_receiver=4
"""

#To use when looking for new messages
rowarrayi = []

if query == "newMessages":
    #cursor.execute("select * from message where user_id_receiver = " + user_id_receiver + " AND `read` is NULL;")
    cursor.execute("select * from message where user_id_receiver = %s AND `read` is NULL;", (user_id_receiver))
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['user_id_sender'] = row[0]
        c['user_id_receiver'] = row[1]
        c['message'] = str(row[2])
        c['sent'] = str(row[3])
        rowarrayi.append(c)

    if rowarrayi:
		print json.dumps(rowarrayi, ensure_ascii=False)

"""
Example:
http://localhost/cgi-bin/server.cgi?q=read&user_id_sender=3&user_id_receiver=4
"""

