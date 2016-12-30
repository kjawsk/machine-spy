import unittest
import datetime
import sys
sys.path.append('..')
from server import app
from server.models import db, Entry
from server.utils import MyDate
from flask import json
from mock import MagicMock

class PostMessageTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = app.test_client()
        db.create_all()

        self.date = MyDate.now()
        self.machine_id = 'ESP-1'
        MyDate.now = MagicMock(return_value=self.date)
        self.request = json.dumps(dict(machine_id=self.machine_id))

    def test_post_message(self):
        rv = self.app.post(
            '/entries',
            data=self.request,
            content_type='application/json')

        self.assertIn('Entry added', rv.data.decode('utf-8'))
        self.assertNotIn('415 Unsupported Media Type', rv.data.decode('utf-8'))
        entries = db.session.query(Entry)
        self.assertEqual(entries[0].date, self.date)
        self.assertEqual(entries[0].machine_id, self.machine_id)

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

if __name__ == '__main__':
    unittest.main()
