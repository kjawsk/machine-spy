from flask import abort, request, json, render_template, flash, url_for, redirect
from flask_login import login_required, logout_user, login_user
from urllib.parse import urljoin, urlparse
from server import app, login_manager
from server.models import db, Entry, Sensor, User
from server.forms import AddSensorForm, LoginForm
import datetime
import os

def add_to_db(item):
    db.session.add(item)
    db.session.commit()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.route('/sensor/add', methods = ['POST', 'GET'])
@login_required
def add_sensor():
    form = AddSensorForm(request.form)
    if request.method == 'POST' and form.validate():
        new_sensor = Sensor(form.name.data)
        add_to_db(new_sensor)
        flash('Sensor sucessfully added')

        next = request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)

        return redirect(url_for('add_sensor'))
    return render_template('add_sensor.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            form.username.errors.append('Invalid credentials')
        else:
            login_user(user, remember=True)
            flash('You were logged in')

            next = request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)

            return redirect(url_for('add_sensor'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))
