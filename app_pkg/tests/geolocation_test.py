# Environment Imports
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Library Imports
import unittest
import os

# Package Variables
from web_package.config import test_config
from web_package.models import Post

class GeolocationTestCase(unittest.TestCase):

    def setUp(self):
        # Eventually move this functionality up to prevent duplication
        app = Flask(__name__)
        app.config.from_object('web_package.config.test_config')
        db = SQLAlchemy(app)
        db.drop_all()
        db.create_all()
        self.app = app
        self.db = db
        print "Ran setUp"

    def tearDown(self):
        #os.unlink(self.app.config[''])            #Keep to inspect what happened on failure        
        print "Ran tearDown"

    def test_geolocation_creation(self):
        self.assertEqual(True, True, "aaaaahhhhh")
        self.assertEqual(True, True, "Didn't make it past the second test")

    def test_geolocation_validation(self):
        self.assertEqual(True, True, "argh")

    def get_suite(self):
        print self.__name__
        return unittest.TestLoader().loadTestsFromTestCase(GeolocationTestCase)

if __name__ == '__main__':
    # Create a test suite from test cases
    suite = PostTextCase.get_suite()
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    # Run the test suite and output human readable results
    runner.run(suite)

