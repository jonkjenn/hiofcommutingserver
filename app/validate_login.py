from MySQLSessionStore import MySQLSessionStore
from werkzeug.wrappers import Response
import collections
import json

def is_logged_in(request):
    session_store = MySQLSessionStore()
    sid = request.cookies.get('hccook')
    if sid and session_store.session_valid(sid):
        return True
    return False

def failed_login():
    c = collections.OrderedDict()
    ar = []

    c['user_id'] = -200
    ar.append(c)
    return Response(json.dumps(ar), mimetype='text/plain')
