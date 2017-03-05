import unittest
from unittest import TestSuite, TextTestRunner
from .add_sensor_tests import AddSensorTestCase
from .edit_sensor_tests import EditSensorTestCase
from .login_logout_tests import LoginTestCase
from .post_entry_tests import PostEntryTestCase
from .view_sensor_list_tests import ViewSensorListTestCase

if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(unittest.makeSuite(AddSensorTestCase))
    suite.addTest(unittest.makeSuite(EditSensorTestCase))
    suite.addTest(unittest.makeSuite(LoginTestCase))
    suite.addTest(unittest.makeSuite(PostEntryTestCase))
    suite.addTest(unittest.makeSuite(ViewSensorListTestCase))
    runner = unittest.TextTestRunner()
    runner.run(suite)
