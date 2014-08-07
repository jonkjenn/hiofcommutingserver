import config
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
import app

application = app.create_app()
