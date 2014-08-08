import ConfigParser
import os
import site
import sys

Config = ConfigParser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config'))

p = os.path.dirname(__file__)
if p not in sys.path:
    sys.path.append(p)

Config.read(path)

sites = Config.options('sites')

for s in sites:
    site.addsitedir(Config.get('sites',s))

import app

application = app.create_app()
