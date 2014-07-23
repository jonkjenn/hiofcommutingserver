#!/usr/bin/python 
# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from app import create_app

app = create_app()
run_simple('localhost',8888,app,use_reloader=True)
