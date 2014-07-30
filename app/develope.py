#!/usr/bin/python 
# -*- coding: utf-8 -*-
from werkzeug.serving import run_simple
from app import create_app

app = create_app()
run_simple('192.168.1.4',8888,app,use_reloader=True)
#run_simple('192.168.0.104',8888,app,use_reloader=True)
