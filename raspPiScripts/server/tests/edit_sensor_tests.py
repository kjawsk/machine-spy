import unittest
import sys
sys.path.append('../..')
from server import app
from server.models import db, Sensor, User

class EditSensorTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()
        username = 'meaningless'
        password = 'meaningless'
        self.add_user(username, password)
        self.login_user(username, password)
        self.sensor_name = 'ESP8266-1351177'
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
