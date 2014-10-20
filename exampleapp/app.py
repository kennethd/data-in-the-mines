#!/usr/bin/env python2.7

import argparse
import logging
import os
import sys

from flask import Flask, render_template

from ditm.flask.blueprint import ditm

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(ditm, url_prefix='/datamines')

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='example data-in-the-mines app')
    parser.add_argument('--config', help="config file.  if not set, will look for EXAMPLEAPP_CONFIG")
    parser.add_argument('--debug', action="store_true", help="put app into debug mode")
    parser.add_argument('--port', type=int, default=9919, help="port number.  default 9919")
    args = parser.parse_args()

    if args.config:
        app.config.from_file(app.config)
    else:
        app.config.from_envvar('EXAMPLEAPP_CONFIG', silent=True)

    if args.debug:
        app.debug = True

    app.run(port=args.port)

