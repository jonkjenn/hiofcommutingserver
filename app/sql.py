import MySQLdb

def getCursor(address='localhost', user='bo14g23', password='bo14g23MySql', database='bo14g23'):
    # SQL connection and cursor
    db = MySQLdb.connect(address, user, password, database)
    db.set_character_set('utf8')
    cursor = db.cursor()
    return cursor

def getdb(address='localhost', user='bo14g23', password='bo14g23MySql', database='bo14g23'):
    # SQL connection and cursor
    db = MySQLdb.connect(address, user, password, database)
    db.set_character_set('utf8')
    return db
