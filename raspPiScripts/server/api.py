from flask import request, json, render_template, flash, url_for
from server import app
from server.models import db, Entry, Sensor
import datetime
import os

def add_to_db(item):
    db.session.add(item)
    db.session.commit()

@app.route('/')
def index():
    return 'Main page!'

@app.route('/entries', methods = ['POST'])
def add_entry():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json(silent=True)
        new_entry = Entry(content['sensor_name'])
        add_to_db(new_entry)
        return 'Entry added: ' + str(content)
    else:
        return '415 Unsupported Media Type'
