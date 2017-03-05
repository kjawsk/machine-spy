import unittest
import os
from server import app
from server.models import db, User

class LoginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp.db"
        db.create_all()
        cls.username = 'user12345'
        cls.password = 'topsecret'
        cls.add_user()

    @classmethod
    def add_user(cls):
        user = User(cls.username, cls.password)
        db.session.add(user)
        db.session.commit()

    def test_01_login_user(self):
        rv = self.app.post(
            '/login',
            data=(dict(
                username=self.username,
                password=self.password)),
            follow_redirects=True)

        self.assertIn('You were logged in', rv.data.decode('utf-8'))

    def test_02_login_user_with_invalid_password(self):
        rv = self.app.post(
            '/login',
            data=(dict(
                username=self.username,
                password=self.password + "x")),
            follow_redirects=True)

        self.assertIn('Invalid credentials', rv.data.decode('utf-8'))

    def test_03_login_user_with_invalid_username(self):
        rv = self.app.post(
            '/login',
            data=(dict(
                username=self.username + "x",
                password=self.password)),
            follow_redirects=True)

        self.assertIn('Invalid credentials', rv.data.decode('utf-8'))

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        os.remove('server/tmp.db')

if __name__ == '__main__':
    unittest.main()
