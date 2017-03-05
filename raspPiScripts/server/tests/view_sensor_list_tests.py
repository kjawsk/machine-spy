import unittest
import os
from server import app
from server.models import db, Sensor, User

class EditSensorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp.db"
        db.create_all()
        cls.username = 'username'
        cls.password = 'password'
        cls.add_user()
        cls.login_user()

    @classmethod
    def add_user(cls):
        user = User(cls.username, cls.password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def login_user(cls):
        return cls.app.post('/login',
            data=(dict(
                username=cls.username,
                password=cls.password)),
            follow_redirects=True)

    def add_sensor(self, sensor_name):
        sensor = Sensor(sensor_name)
        db.session.add(sensor)
        db.session.commit()

    def test_01_view_without_sensors(self):
        rv = self.app.get(
            '/sensor/view/',
            follow_redirects=True)

        self.assertIn("There is no sensors", rv.data.decode('utf-8'))

    def test_02_view_with_sensors(self):
        sensor_name1 = "ESP8266-1234567"
        self.add_sensor(sensor_name1)

        rv = self.app.get(
            '/sensor/view/',
            follow_redirects=True)

        self.assertIn(sensor_name1, rv.data.decode('utf-8'))

        sensor_name2 = "ESP8266-7654321"
        self.add_sensor(sensor_name2)

        rv = self.app.get(
            '/sensor/view/',
            follow_redirects=True)

        self.assertIn(sensor_name1, rv.data.decode('utf-8'))
        self.assertIn(sensor_name2, rv.data.decode('utf-8'))

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        os.remove('server/tmp.db')

if __name__ == '__main__':
    unittest.main()
