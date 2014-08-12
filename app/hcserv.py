#!/usr/bin/python
#-*- coding: UTF-8 -*-
"""# enable debugging"""

"""
This module handles HTTP requests from the Hiof-commuting app and
returns json objects containing messages sendt between users.
"""

import json
import collections
import sql
import validate_login
from werkzeug.wrappers import Response

import logging
log = logging.getLogger(__name__)

# Args
#args = cgi.FieldStorage()
#query = args.getfirst("q", "")
#user_id_sender = args.getfirst("user_id_sender", "")
#user_id_receiver = args.getfirst("user_id_receiver", "")
#message = args.getfirst("message", "")


# To use in the conversation activity where both senderID and receiverID is known

import config

gcm_key = config.gcm_key()

#if query == "conversation":
def conversation(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    cursor = sql.getCursor()

    user_id_receiver = request.args.get('user_id_receiver')

    rowarrayc = []
    cursor.execute("select * from message where user_id_sender IN(%s, %s) and user_id_receiver IN(%s, %s) order by sent ASC", (request.user_id, user_id_receiver, request.user_id, user_id_receiver))
    
    rows = cursor.fetchall()
    
    for row in rows:
        c = collections.OrderedDict()
        c['user_id_sender'] = row[0]
        c['user_id_receiver'] = row[1]
        c['message'] = row[2]
        c['sent'] = str(row[3])
        c['read'] = str(row[4])
        rowarrayc.append(c)

    if rowarrayc:
        j = json.dumps(rowarrayc, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    return Response('{test:"test"}', mimetype='text/plain')


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
    #cursor.execute("SELECT * FROM message inner join (select * from message WHERE `user_id_receiver` = %s order by sent desc) a on (message.user_id_sender=a.user_id_sender) group by message.user_id_sender order by a.sent desc", (request.user_id))
    cursor.execute("SELECT m.user_id_sender, m.message, m.sent FROM (select user_id_sender, max(sent) msent from message WHERE `user_id_receiver` = %s group by user_id_sender) a inner join message m on (m.user_id_sender=a.user_id_sender and m.sent = a.msent) order by m.sent desc", (request.user_id))
    rows = cursor.fetchall()

    for row in rows:
            c = collections.OrderedDict()
            c['user_id_sender'] = row[0]
            c['message'] = row[1]
            c['sent'] = str(row[2])
            rowarrayi.append(c)

    if rowarrayi:
        j = json.dumps(rowarrayi, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    return Response('{test:"test"}', mimetype='text/plain')

"""
Example:
http://frigg.hiof.no/bo14-g23/hcserv.py?q=inbox&user_id_receiver=4
"""

# To use when sending message

#if query == "send":
def send(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    try:
        db = sql.getdb()
        cursor = db.cursor()

        user_id_receiver = request.form.get('user_id_receiver')
        message = request.form.get('message')

        #log.debug(request.form)

        #cursor.execute("insert into message(user_id_sender, user_id_receiver, message, sent) values(" + user_id_sender + "," + user_id_receiver + "," + "\"" + message + "\"" + ", current_timestamp)" )
        cursor.execute("insert into message(user_id_sender, user_id_receiver, message, sent) values(%s,%s,%s,current_timestamp)",(request.user_id, user_id_receiver, message))
        db.commit()

        #cursor.execute("select gcm_id from user where user_id = %s", (user_id_receiver))
        cursor.execute("select firstname, surname from user where user_id = %s", (request.user_id))
        row = cursor.fetchone()
        firstname = row[0]
        surname = row[1]

        cursor.execute("select gcm_id from user where user_id = %s", (user_id_receiver))
        row = cursor.fetchone()
        receiver = row[0]

        db.close()

        send_gcm(firstname, surname, receiver, message, request.user_id)
        return Response(message, mimetype='text/plain', status=200)
    except Exception as e:
        #log.exception("Send exception: ")
        return Response('{test:test}',status=400)

def test():
    db = sql.getdb()
    cursor = db.cursor()

    user_id_receiver = 36
    message = "test message"

    #cursor.execute("insert into message(user_id_sender, user_id_receiver, message, sent) values(" + user_id_sender + "," + user_id_receiver + "," + "\"" + message + "\"" + ", current_timestamp)" )
    cursor.execute("insert into message(user_id_sender, user_id_receiver, message, sent) values(%s,%s,%s,current_timestamp)",(35, user_id_receiver, message))
    db.commit()

    import os
    send_gcm("test", "test", "APA91bGisBzMoj-n6cy7TKkyK-smGuR0N_mX3rFBYsEOqaS5beam0UMcsaFbscdfdICfar1tb8YjcrX9ZBg2goxaYtDHigxK6LTOuaLO2dNUGo29fq_H7yR-_59GOm4R3IySsDDax5VFTcDxv-n7hENHaO1pIsFsWA","test message",35)

def send_gcm(firstname, surname, receiver, message, sender_id):
    import gcm
    from gcm import GCM
    g = GCM(gcm_key)
    log.debug("Gcm_key: " + gcm_key)
    data = {'message':message, 'sender_firstname':firstname,'sender_surname':surname, 'sender_id':str(sender_id)}

    try:
        log.debug("Sending: ")
        log.debug(data)
        log.debug("Receiver: " + receiver)
        g.plaintext_request(registration_id=receiver,data=data)
    except gcm.gcm.GCMInvalidRegistrationException:
        log.exception("Gcm failed: ")
        db = sql.getdb()
        cursor = db.cursor()
        cursor.execute("update user set gcm_id = null where gcm_id = %s", (receiver))
        db.commit()
        db.close()


def get_gcm_id(user_id):
    cursor = sql.getCursor()
    cursor.execute("select gcm_id from user where user_id = %s",(user_id))


"""
Example:
http://localhost/cgi-bin/server.cgi?q=send&user_id_sender=3&user_id_receiver=4&message=Hei%20du
"""


#To use when message is read (inserting datetime)

#if query == "read":
def read(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    db = sql.getdb()
    cursor = db.cursor()

    user_id_sender = request.form.get('user_id_sender')

    #cursor.execute("update message set `read`=current_timestamp where user_id_sender=" + user_id_sender + " and user_id_receiver=" + user_id_receiver + " and `read` is NULL")
    cursor.execute("update message set `read`=current_timestamp where user_id_sender=%s and user_id_receiver=%s and `read` is NULL", (user_id_sender, request.user_id))
    cursor.close()
    db.commit()
    db.close()

    return Response('{test:"test"}')

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
        c['message'] = row[2]
        c['sent'] = str(row[3])
        rowarrayi.append(c)

    if rowarrayi:
        j= json.dumps(rowarrayi, ensure_ascii=False)
        return Response(j, mimetype='text/plain')
    return Response('{test:"test"}', mimetype='text/plain')

"""
Example:
http://localhost/cgi-bin/server.cgi?q=read&user_id_sender=3&user_id_receiver=4
"""

