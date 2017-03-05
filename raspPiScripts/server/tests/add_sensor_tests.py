import unittest
import os
from .. import app
from ..models import db, Sensor, User

class AddSensorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp.db"
        db.create_all()
        cls.username = 'meaningless1'
        cls.password = 'meaningless2'
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

    @classmethod
    def logout_user(cls):
        return cls.app.get('/logout', follow_redirects=True)

    def test_01_add_sensor(self):
        sensor_name = 'ESP8266-1351177' # 15 charachters

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertIn('Sensor sucessfully added', rv.data.decode('utf-8'))
        sensor = Sensor.query.filter_by(name=sensor_name).first()
        self.assertEqual(sensor_name, sensor.name)

    def test_02_add_sensor_with_not_unique_name(self):
        sensor_name = 'ESP8266-1351177'

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertIn('Sensor sucessfully added', rv.data.decode('utf-8'))

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertIn('Sensor already exist, name is not unique', rv.data.decode('utf-8'))

    def test_03_add_sensor_with_invalid_name_length(self):
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

    def test_04_add_sensor_with_not_logged_user(self):
        self.logout_user()
        sensor_name = 'ESP8266-1351177' # 15 charachters

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertNotIn('Sensor sucessfully added', rv.data.decode('utf-8'))
        self.login_user() #restore

    def tearDown(self):
        Sensor.query.delete()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        os.remove('server/tmp.db')

if __name__ == '__main__':
    unittest.main()
