import site
site.addsitedir('/home/jon/code/hiofcommutingserver/app')
site.addsitedir('/usr/lib/python2.7/dist-packages/MySQLdb')
site.addsitedir('/home/jon/code/hiofcommutingserver/env/lib/python2.7/site-packages')
import app

application = app.create_app()
