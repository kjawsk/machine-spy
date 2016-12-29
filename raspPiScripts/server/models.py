from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = 'Entries'
    machine_id = db.Column(db.String(40), primary_key=True)
    date = db.Column(db.DateTime(30))

    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.date = datetime.datetime.now()
