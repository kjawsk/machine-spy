from flask_sqlalchemy import SQLAlchemy
from server.utils import MyDate

db = SQLAlchemy()

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    date = db.Column(db.DateTime(30))

    def __init__(self, sensor_name):
        sensor = Sensor.query.filter_by(name=sensor_name).first()
        self.sensor_id = sensor.id
        self.date = MyDate.now()

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    entries = db.relationship('Entry', backref='sensor', lazy='dynamic')

    def __init__(self, sensor_name):
        self.name = sensor_name
