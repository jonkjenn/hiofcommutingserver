from MySQLSessionStore import MySQLSessionStore
from werkzeug.wrappers import Response
import collections
import json

def is_logged_in(request):
    session_store = MySQLSessionStore()
    sid = request.cookies.get('hccook')
    print "sid"
    print sid
    if sid and session_store.session_valid(sid):
        request.session = session_store.get(sid)
        request.user_id = session_store.get_userid(sid)
        return True
    return False

def failed_login():
    print "Login failed"
    c = collections.OrderedDict()
    ar = []

    c['user_id'] = -200
    ar.append(c)
    return Response(json.dumps(ar), mimetype='text/plain', status=400)
