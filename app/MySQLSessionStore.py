import werkzeug.contrib.sessions
from werkzeug.contrib.sessions import SessionStore
import sql

class MySQLSessionStore(SessionStore):

    def __init__(self):
        SessionStore.__init__(self, None)

    #def get(self, sid, user_id = None):
     #   if not self.is_valid_key(sid) or not self.session_valid(sid):
      #      session = self.new()
       #     self.save(session.sid,user_id)
        #else:
        #    session =  self.session_class({},sid,False)
        #return session

    def session_new(self, sid, user_id):
        session = self.new()
        self.delete_old_sessions(user_id)
        self.save(session.sid,user_id)
        return session

    def session_valid(self,sid):
        cursor = sql.getCursor()
        cursor.execute("select user_id, created from session where session_id = %s and datediff(now(),created)<5 ",(sid))
        rows = cursor.fetchone()
        if rows != None:
            return True
        return False

    def get_userid(self, sid):
        cursor = sql.getCursor()
        cursor.execute("select user_id, created from session where session_id = %s and datediff(now(),created)<5 ",(sid))
        return cursor.fetchone()[0]

    def get_userid_from_face(self, face):
        cursor = sql.getCursor()
        cursor.execute("select user_id from facebook_user where facebook_id = %s", (face))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def save(self, sid, user_id):
        db = sql.getdb()
        cursor = db.cursor()
        cursor.execute("insert into session (session_id, user_id, created) values(%s,%s,now())",(sid, user_id))
        db.commit()

    def delete_old_sessions(self, user_id):
        db = sql.getdb()
        cursor = db.cursor()
        cursor.execute("delete from session where user_id = %s", (user_id))
        db.commit()
