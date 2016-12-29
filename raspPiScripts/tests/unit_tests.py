import unittest
import datetime
import sys
sys.path.append('..')
from server import app
from server.models import db
from flask import json


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = app.test_client()
        db.create_all()

    def test_main_page(self):
        rv = self.app.get('/', follow_redirects=True)

        self.assertIn('Hello World!', rv.data.decode('utf-8'))

    def test_post_message(self):
        request = json.dumps(dict(
            machine_id='ESP-1',
            date=datetime.datetime.now()))

        rv = self.app.post(
            '/entries',
            data=request,
            content_type='application/json')

        self.assertNotIn('415 Unsupported Media Type', rv.data.decode('utf-8'))
        self.assertIn('Entry added', rv.data.decode('utf-8'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
