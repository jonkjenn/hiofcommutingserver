import json
import collections
import sql
import validate_login
from werkzeug.wrappers import Response
import facebook

def reggcm(request):
    if not validate_login.is_logged_in(request):
        return validate_login.failed_login()

    gcmId = request.form.get('gcmId')
    gcmVersion = request.form.get('gcmVersion')

    if not (gcmId and gcmVersion):
        return

    db = sql.getdb()
    cursor = db.cursor()

    cursor.execute("update user set gcm_id = %s, gcm_version = %s where user_id = %s", (gcmId,gcmVersion, request.user_id))

    db.commit()
