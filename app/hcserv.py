#!/usr/bin/python
#-*- coding: UTF-8 -*-
"""# enable debugging"""

"""
This module handles HTTP requests from the Hiof-commuting app and
returns json objects containing messages sendt between users.
"""

import MySQLdb
import json
import collections
import sql
import validate_login
from werkzeug.wrappers import Response

# Args
#args = cgi.FieldStorage()
#query = args.getfirst("q", "")
#user_id_sender = args.getfirst("user_id_sender", "")
#user_id_receiver = args.getfirst("user_id_receiver", "")
#message = args.getfirst("message", "")


# To use in the conversation activity where both senderID and receiverID is known


#if query == "conversation":
def conversation(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    cursor = sql.getCursor()

    rowarrayc = []
    cursor.execute("select * from message where user_id_sender IN(%s, %s) and user_id_receiver IN(%s, %s) order by sent ASC", (request.user_id, user_id_receiver, request.user_id, user_id_receiver))
    
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
        return Response(rowarrayc, mimetype='text/plain')
    return Response("", mimetype='text/plain')


"""
Example:
http://frigg.hiof.no/bo14-g23/hcserv.py?q=conversation&user_id_sender=3&user_id_receiver=4
"""


# To use in inbox activity where only receiverID is known


#if query == "inbox":
def inbox(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    cursor = sql.getCursor()

    rowarrayi = []
    cursor.execute("SELECT * FROM message inner join (select * from message WHERE `user_id_receiver` = %s order by sent desc) a on (message.user_id_sender=a.user_id_sender) group by message.user_id_sender order by a.sent desc", (request.user_id))
    rows = cursor.fetchall()

    for row in rows:
            c = collections.OrderedDict()
            c['user_id_sender'] = row[5]
            c['message'] = str(row[7])
            c['sent'] = str(row[8])
            rowarrayi.append(c)

    if rowarrayi:
        j = json.dumps(rowarrayi, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    return Response("", mimetype='text/plain')

"""
Example:
http://frigg.hiof.no/bo14-g23/hcserv.py?q=inbox&user_id_receiver=4
"""

# To use when sending message

#if query == "send":
def send(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()
    cursor = sql.getCursor()

    #cursor.execute("insert into message(user_id_sender, user_id_receiver, message, sent) values(" + user_id_sender + "," + user_id_receiver + "," + "\"" + message + "\"" + ", current_timestamp)" )
    cursor.execute("insert into message(user_id_sender, user_id_receiver, message, sent) values(%s,%s,%s,current_timestamp)",(request.user_id, user_id_receiver, message))
    cursor.close()
    db.commit()
    db.close()

    return Response(message, mimetype='text/plain')

"""
Example:
http://localhost/cgi-bin/server.cgi?q=send&user_id_sender=3&user_id_receiver=4&message=Hei%20du
"""


#To use when message is read (inserting datetime)

#if query == "read":
#def read(request):
    #cursor.execute("update message set `read`=current_timestamp where user_id_sender=" + user_id_sender + " and user_id_receiver=" + user_id_receiver + " and `read` is NULL")
#    cursor.execute("update message set `read`=current_timestamp where user_id_sender=%s and user_id_receiver=%s and `read` is NULL", ()
#    cursor.close()
#    db.commit()
#    db.close()

"""
Example: 
http://localhost/cgi-bin/server.cgi?q=read&user_id_sender=3&user_id_receiver=4
"""

#To use when looking for new messages

#if query == "newMessages":
def newMessages(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    rowarrayi = []
    #cursor.execute("select * from message where user_id_receiver = " + user_id_receiver + " AND `read` is NULL;")
    cursor.execute("select * from message where user_id_receiver = %s AND `read` is NULL;", (request.user_id))
    rows = cursor.fetchall()

    for row in rows:
        c = collections.OrderedDict()
        c['user_id_sender'] = row[0]
        c['user_id_receiver'] = row[1]
        c['message'] = str(row[2])
        c['sent'] = str(row[3])
        rowarrayi.append(c)

    if rowarrayi:
        j= json.dumps(rowarrayi, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    return Response("", mimetype='text/plain')

"""
Example:
http://localhost/cgi-bin/server.cgi?q=read&user_id_sender=3&user_id_receiver=4
"""

