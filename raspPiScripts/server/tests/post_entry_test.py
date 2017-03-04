import unittest
import sys
from server import app
from server.models import db, Entry, Sensor, User
from server.util.mydate import MyDate
from flask import json
from mock import MagicMock

class PostEntryTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()

        self.date = MyDate.now()
        MyDate.now = MagicMock(return_value=self.date)

    def config_environment(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = app.test_client()
        db.create_all()

    def add_sensor(self, name):
        sensor = Sensor(name)
        db.session.add(sensor)
        db.session.commit()
        self.sensor_id = sensor.id

    def create_request(self, sensor_name, value):
        data = {}
        data['sensor_name'] = sensor_name
        data['value'] = value
        return json.dumps(data)

    def test_post_message(self):
        sensor_name = 'ESP8266-1122334'
        self.add_sensor(sensor_name)

        value = 14
        request = self.create_request(sensor_name, value)

        rv = self.app.post(
            '/entries',
            data=request,
            content_type='application/json')

        self.assertIn('Entry added', rv.data.decode('utf-8'))
        self.assertNotIn('415 Unsupported Media Type', rv.data.decode('utf-8'))

        entry = Entry.query.filter_by(date=self.date).first()
        self.assertEqual(entry.date, self.date)
        self.assertEqual(entry.sensor_id, self.sensor_id)
        self.assertEqual(entry.value, value)

    def test_post_message_with_invalid_header(self):
        sensor_name = 'ESP8266-1122334'
        self.add_sensor(sensor_name)

        value = 14
        request = self.create_request(sensor_name, value)

        rv = self.app.post(
            '/entries',
            data=request,
            content_type='INVALID HEADER')

        self.assertNotIn('Entry added', rv.data.decode('utf-8'))
        self.assertIn('415 Unsupported Media Type', rv.data.decode('utf-8'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
