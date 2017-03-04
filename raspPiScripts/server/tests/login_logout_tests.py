import unittest
import sys
from server import app
from server.models import db, User

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.config_environment()
        self.username = 'user12345'
        self.password = 'topsecret'
        self.add_user(self.username, self.password)

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
