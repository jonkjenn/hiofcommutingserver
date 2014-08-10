import ConfigParser
import os
import site

Config = ConfigParser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config'))

Config.read(path)

def sites():
    sites = Config.options('sites')

    for s in sites:
        site.addsitedir(Config.get('sites',s))

def sql():
    address = Config.get('sql', 'address')
    database = Config.get('sql','database')
    user = Config.get('sql','user')
    passwd = Config.get('sql','passwd')

    return {"address": address, "database":database, "user":user,"passwd":passwd}

def gcm_key():
    return Config.get('gcm_key','gcm_key')
