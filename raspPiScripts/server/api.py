from flask import request, json, render_template, flash, url_for
from server import app
from server.models import db, Entry
import datetime
import os

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/entries', methods = ['POST'])
def api_entry():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json(silent=True)
        new_entry = Entry(content['machine_id'])
        db.session.add(new_entry)
        db.session.commit()
        return 'Entry added: ' + str(content)
    else:
        return '415 Unsupported Media Type'
