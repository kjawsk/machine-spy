import unittest
import sys
from server import app
from server.models import db, Sensor, User

class EditSensorTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()
        username = 'meaningless'
        password = 'meaningless'
        self.add_user(username, password)
        self.login_user(username, password)
        self.sensor_name = 'ESP8266-999999'
        self.add_sensor(self.sensor_name)

    def config_environment(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = app.test_client()
        db.create_all()

    def add_user(self, username, password):
        user = User(username, password)
        db.session.add(user)
        db.session.commit()

    def add_sensor(self, name):
        sensor = Sensor(name)
        db.session.add(sensor)
        db.session.commit()
        self.sensor_id = sensor.id

    def login_user(self, username, password):
        return self.app.post('/login',
            data=(dict(
                username=username,
                password=password)),
            follow_redirects=True)

    def test_name_field_contains_sensor_name(self):
        rv = self.app.get(
            '/sensor/edit/%s' % self.sensor_id,
            follow_redirects=True)

        self.assertIn(self.sensor_name, rv.data.decode('utf-8'))

    def test_edit_sensor_name(self):
        new_name = 'ESP8266-1111111' # 15 characters

        rv = self.app.post(
            '/sensor/edit/%s' % self.sensor_id,
            data=dict(name=new_name),
            follow_redirects=True)

        self.assertIn('Sensor has been changed', rv.data.decode('utf-8'))
        sensor = Sensor.query.filter_by(name=new_name).first()
        self.assertEqual(new_name, sensor.name)

    def test_edit_sensor_with_invalid_name_length(self):
        new_name = 'ESP8266-111111' #14 characters

        rv = self.app.post(
            '/sensor/edit/%s' % self.sensor_id,
            data=dict(name=new_name),
            follow_redirects=True)

        self.assertIn('Name must be 15 character long', rv.data.decode('utf-8'))

        new_name = 'ESP8266-11111111' #16 characters

        rv = self.app.post(
            '/sensor/edit/%s' % self.sensor_id,
            data=dict(name=new_name),
            follow_redirects=True)

        self.assertIn('Name must be 15 character long', rv.data.decode('utf-8'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
