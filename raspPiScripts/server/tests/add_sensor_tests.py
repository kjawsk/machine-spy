import unittest
import sys
sys.path.append('../..')
from server import app
from server.models import db, Sensor, User

class AddSensorTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()
        username = 'meaningless'
        password = 'meaningless'
        self.add_user(username, password)
        self.login_user(username, password)

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

    def login_user(self, username, password):
        return self.app.post('/login',
            data=(dict(
                username=username,
                password=password)),
            follow_redirects=True)

    def logout_user(self):
        return self.app.get('/logout', follow_redirects=True)


    def test_add_sensor(self):
        sensor_name = 'ESP8266-1351177' # 15 charachters

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertIn('Sensor sucessfully added', rv.data.decode('utf-8'))
        sensor = Sensor.query.filter_by(name=sensor_name).first()
        self.assertEqual(sensor_name, sensor.name)

    def test_add_sensor_with_not_unique_name(self):
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

    def test_add_sensor_with_invalid_name_length(self):
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

    def test_add_sensor_with_not_logged_user(self):
        self.logout_user()
        sensor_name = 'ESP8266-1351177' # 15 charachters

        rv = self.app.post(
            '/sensor/add',
            data=dict(name=sensor_name),
            follow_redirects=True)

        self.assertNotIn('Sensor sucessfully added', rv.data.decode('utf-8'))
        self.assertIn('Please log in to access this page', rv.data.decode('utf-8'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
