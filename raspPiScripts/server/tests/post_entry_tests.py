import unittest
import os
from server import app
from server.models import db, Entry, Sensor, User
from server.util.mydate import MyDate
from flask import json
from mock import MagicMock

class PostEntryTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp.db"
        db.create_all()
        cls.date = MyDate.now()
        cls.sensor_name = 'ESP8266-1122332'
        cls.value = 3
        MyDate.now = MagicMock(return_value=cls.date)
        cls.add_sensor()
        cls.request = cls.create_request(cls.sensor_name, cls.value)

    @classmethod
    def add_sensor(cls):
        sensor = Sensor(cls.sensor_name)
        db.session.add(sensor)
        db.session.commit()
        cls.sensor_id = sensor.id

    @classmethod
    def create_request(self, sensor_name, value):
        data = {}
        data['sensor_name'] = sensor_name
        data['value'] = value
        return json.dumps(data)

    def test_01_post_message(self):
        rv = self.app.post(
            '/entries',
            data=self.request,
            content_type='application/json')

        self.assertIn('Entry added', rv.data.decode('utf-8'))
        self.assertNotIn('415 Unsupported Media Type', rv.data.decode('utf-8'))

        entry = Entry.query.filter_by(date=self.date).first()
        self.assertEqual(entry.date, self.date)
        self.assertEqual(entry.sensor_id, self.sensor_id)
        self.assertEqual(entry.value, self.value)

    def test_02_post_message_with_invalid_header(self):
        rv = self.app.post(
            '/entries',
            data=self.request,
            content_type='INVALID HEADER')

        self.assertNotIn('Entry added', rv.data.decode('utf-8'))
        self.assertIn('415 Unsupported Media Type', rv.data.decode('utf-8'))

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        os.remove('server/tmp.db')

if __name__ == '__main__':
    unittest.main()
