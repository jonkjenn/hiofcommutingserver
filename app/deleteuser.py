import sql
import validate_login
from werkzeug.wrappers import Response

def deleteuser(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    print "Deleting user"

    uid = request.args.get('uid')

    print uid
    print request.user_id

    if uid and int(uid) == request.user_id:
        print "Starting delete"
        db = sql.getdb()

        try:
            cursor = db.cursor()
            cursor.execute("delete from message where user_id_sender = %s or user_id_receiver = %s", (request.user_id, request.user_id))
            cursor.execute("delete from facebook_user where user_id = %s", (request.user_id))
            cursor.execute("delete from email_user where user_id = %s", (request.user_id))
            cursor.execute("delete from user where user_id = %s", (request.user_id))
            cursor.execute("delete from session where user_id = %s", (request.user_id))
            db.commit()
        except:
            print "Delete failed"
            db.rollback()
