from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from .util.mydate import MyDate

db = SQLAlchemy()

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    date = db.Column(db.DateTime(30))
    value = db.Column(db.Integer)

    def __init__(self, sensor_name, value):
        sensor = Sensor.query.filter_by(name=sensor_name).first()
        self.sensor_id = sensor.id
        self.date = MyDate.now()
        self.value = value

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    entries = db.relationship('Entry', backref='sensor', lazy='dynamic')

    def __init__(self, sensor_name):
        self.name = sensor_name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, plain_password):
        self.username = username
        self.password = sha256_crypt.hash(plain_password)

    def check_password(self, plain_password):
        return sha256_crypt.verify(plain_password, self.password)

    """Functions below are required by Flask-Login"""

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
