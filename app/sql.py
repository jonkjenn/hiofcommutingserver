import pymysql
import config
charset='utf8'
c = config.sql()
address=c['address']
user=c['user']
passwd=c['passwd']
database=c['database']

def getCursor():
    # SQL connection and cursor
    db = pymysql.connect(host=address, user=user, passwd=passwd, db=database, charset=charset, use_unicode=False)
    db.autocommit(True)
    cursor = db.cursor()
    return cursor

def getdb():
    # SQL connection and cursor
    db = pymysql.connect(host=address, user=user, passwd=passwd, db=database, charset=charset, use_unicode=False)
    db.autocommit(True)
    return db
