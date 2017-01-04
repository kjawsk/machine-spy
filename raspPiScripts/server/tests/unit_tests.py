import unittest
import datetime
import sys
sys.path.append('../..')
from server import app
from server.models import db, Entry, Sensor, User
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

        data = {}
        data['sensor_name'] = sensor.name
        data['value'] = 15
        self.request = json.dumps(data)

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
        self.assertEqual(entry.value, 15)

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

class AddSensorTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()

    def config_environment(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = app.test_client()
        db.create_all()

        self.username = 'user1'
        self.password = 'password1'
        user = User(self.username, self.password)
        db.session.add(user)
        db.session.commit()
        rv = self.app.post(
            '/login',
            data=(dict(
                username=self.username,
                password=self.password)),
            follow_redirects=True)

    def test_add_sensor(self):
        sensor_name = 'ESP8266-1351177' # 15 charachters

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertIn('Sensor sucessfully added', rv.data.decode('utf-8'))
        sensor = Sensor.query.filter_by(name=sensor_name).first()
        self.assertEqual(sensor_name, sensor.name)

    def test_add_sensor_with_invalid_length(self):
        sensor_name = 'ESP8266-135117' # 14 charachters

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertIn(
            'Name must be 15 character long',
            rv.data.decode('utf-8'))

        sensor_name = 'ESP8266-13511777' # 16 charachters

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertIn(
            'Name must be 15 character long',
            rv.data.decode('utf-8'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()

    def config_environment(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = app.test_client()
        db.create_all()

        self.username = 'user1'
        self.password = 'password1'
        user = User(self.username, self.password)
        db.session.add(user)
        db.session.commit()

    def test_login_user(self):
        rv = self.app.post(
            '/login',
            data=(dict(
                username=self.username,
                password=self.password)),
            follow_redirects=True)

        self.assertIn('You were logged in', rv.data.decode('utf-8'))

    def test_login_user_with_invalid_password(self):
        rv = self.app.post(
            '/login',
            data=(dict(
                username=self.username,
                password=self.password + "x")),
            follow_redirects=True)

        self.assertIn('Invalid credentials', rv.data.decode('utf-8'))

    def test_login_user_with_invalid_username(self):
        rv = self.app.post(
            '/login',
            data=(dict(
                username=self.username + "x",
                password=self.password)),
            follow_redirects=True)

        self.assertIn('Invalid credentials', rv.data.decode('utf-8'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
