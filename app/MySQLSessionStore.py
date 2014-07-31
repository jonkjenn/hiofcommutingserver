import werkzeug.contrib.sessions
from werkzeug.contrib.sessions import SessionStore
import MySQLdb
import sql

class MySQLSessionStore(SessionStore):

    def __init__(self, address='localhost', user='bo14g23', password='bo14g23MySql', database='bo14g23'):
        SessionStore.__init__(self, None)
        self.db = sql.getdb(address,user,password,database)
        self.cursor = self.db.cursor()

    #def get(self, sid, user_id = None):
     #   if not self.is_valid_key(sid) or not self.session_valid(sid):
      #      session = self.new()
       #     self.save(session.sid,user_id)
        #else:
        #    session =  self.session_class({},sid,False)
        #return session

    def session_new(self, sid, user_id):
        session = self.new()
        self.save(session.sid,user_id)
        return session

    def session_valid(self,sid):
        self.cursor.execute("select user_id, created from session where session_id = %s and datediff(now(),created)<5 ",(sid))
        rows = self.cursor.fetchone()
        if rows != None:
            return True
        return False

    def get_userid(self, sid):
        self.cursor.execute("select user_id, created from session where session_id = %s and datediff(now(),created)<5 ",(sid))
        return self.cursor.fetchone()[0]

    def get_userid_from_face(self, face):
        self.cursor.execute("select user_id from facebook_user where facebook_id = %s", (face))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def save(self, sid, user_id):
        self.cursor.execute("insert into session (session_id, user_id, created) values(%s,%s,now())",(sid, user_id))
        self.db.commit()
