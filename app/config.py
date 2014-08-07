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
    database = Config.get('sql','database')
    user = Config.get('sql','user')
    passwd = Config.get('sql','passwd')

    return {"database":database, "user":user,"passwd":passwd}
