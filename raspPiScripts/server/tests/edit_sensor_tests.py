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
        cls.sensor_name = 'ESP8266-999999'
        cls.add_user()
        cls.login_user()
        cls.add_sensor()

    @classmethod
    def add_user(cls):
        user = User(cls.username, cls.password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def add_sensor(cls):
        sensor = Sensor(cls.sensor_name)
        db.session.add(sensor)
        db.session.commit()
        cls.sensor_id = sensor.id

    @classmethod
    def login_user(cls):
        return cls.app.post('/login',
            data=(dict(
                username=cls.username,
                password=cls.password)),
            follow_redirects=True)

    def test_01_name_field_contains_sensor_name(self):
        rv = self.app.get(
            '/sensor/edit/%s' % self.sensor_id,
            follow_redirects=True)

        self.assertIn(self.sensor_name, rv.data.decode('utf-8'))

    def test_02_edit_sensor_name(self):
        new_name = 'ESP8266-1111111' # 15 characters

        rv = self.app.post(
            '/sensor/edit/%s' % self.sensor_id,
            data=dict(name=new_name),
            follow_redirects=True)

        self.assertIn('Sensor has been changed', rv.data.decode('utf-8'))
        sensor = Sensor.query.filter_by(name=new_name).first()
        self.assertEqual(new_name, sensor.name)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        os.remove('server/tmp.db')

if __name__ == '__main__':
    unittest.main()
