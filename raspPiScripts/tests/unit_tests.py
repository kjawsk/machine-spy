import unittest
import datetime
import sys
sys.path.append('..')
from server import app
from server.models import db, Entry, Sensor
from server.utils import MyDate
from flask import json
from mock import MagicMock

class PostEntryTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()

        self.date = MyDate.now()
        MyDate.now = MagicMock(return_value=self.date)

        sensor = Sensor('ESP-1')
        db.session.add(sensor)
        db.session.commit()
        self.sensor_id = sensor.id

        self.request = json.dumps(dict(sensor_name=sensor.name))

    def config_environment(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = app.test_client()
        db.create_all()

    def test_post_message(self):
        rv = self.app.post(
            '/entries',
            data=self.request,
            content_type='application/json')

        self.assertIn('Entry added', rv.data.decode('utf-8'))
        self.assertNotIn('415 Unsupported Media Type', rv.data.decode('utf-8'))

        entry = Entry.query.filter_by(date=self.date).first()
        self.assertEqual(entry.date, self.date)
        self.assertEqual(entry.sensor_id, self.sensor_id)

    def test_post_message_with_invalid_header(self):
        rv = self.app.post(
            '/entries',
            data=self.request,
            content_type='INVALID HEADER')

        self.assertNotIn('Entry added', rv.data.decode('utf-8'))
        self.assertIn('415 Unsupported Media Type', rv.data.decode('utf-8'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
