import pymysql
import config
address='localhost'
charset='utf8'
c = config.sql()
user=c['user']
passwd=c['passwd']
database=c['database']

def getCursor():
    # SQL connection and cursor
    db = pymysql.connect(host=address, user=user, passwd=passwd, db=database, charset=charset)
    cursor = db.cursor()
    return cursor

def getdb():
    # SQL connection and cursor
    db = pymysql.connect(host=address, user=user, passwd=passwd, db=database, charset=charset)
    return db
