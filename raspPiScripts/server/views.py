from flask import request, json, render_template, flash, url_for, redirect
from server import app
from server.models import db, Entry, Sensor
from server.forms import AddSensorForm
import datetime
import os

def add_to_db(item):
    db.session.add(item)
    db.session.commit()

@app.route('/sensor/add', methods = ['POST', 'GET'])
def add_sensor():
    form = AddSensorForm(request.form)
    if request.method == 'POST' and form.validate():
        new_sensor = Sensor(form.name.data)
        add_to_db(new_sensor)
        flash('Sensor sucessfully added')
        return redirect(url_for('add_sensor'))
    return render_template('add_sensor.html', form=form)
