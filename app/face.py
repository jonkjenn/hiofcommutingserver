#!/usr/bin/python
#-*- coding: UTF-8 -*-"
import urllib2
import json
def valid_face(token):
    handler = urllib2.urlopen('https://graph.facebook.com/me?fields=id&access_token=' + token)
    if handler.getcode() == 200:
        j = json.loads(handler.read())
        return j.get('id')
    else:
        return None
