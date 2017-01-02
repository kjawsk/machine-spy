from flask import request, json, render_template, flash, url_for, redirect
from server import app
from server.models import db, Entry, Sensor
from server.forms import AddSensorForm
import datetime
import os

def add_to_db(item):
    db.session.add(item)
    db.session.commit()

@app.route('/')
def index():
    return 'Main page!'

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables"""
    db.create_all()
    print('Initialized the database.')

@app.route('/entries', methods = ['POST'])
def add_entry():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json(silent=True)
        new_entry = Entry(content['sensor_name'])
        add_to_db(new_entry)
        return 'Entry added: ' + str(content)
    else:
        return '415 Unsupported Media Type'
