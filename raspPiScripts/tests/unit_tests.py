import unittest
import sys
sys.path.append('..')
from server import app as serverApp


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        serverApp.config['TESTING'] = True
        serverApp.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///tmp.db"
        self.app = serverApp.test_client()

    def test_main_page(self):
        rv = self.app.get('/', follow_redirects=True)

        self.assertIn('Hello World!', rv.data.decode('utf-8'))

    def test_post_message(self):
        request = json.dumps(dict(
            machine_id='ESP-1',
            date=datetime.datetime.now()))

        rv = self.app.post('/messages', data=request, follow_redirects=True)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
