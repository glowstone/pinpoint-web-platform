# Environment Imports
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Library Imports
import unittest
import os

# Package Variables
from web_package.config import test_config
from web_package.models import Post

class PostTestCase(unittest.TestCase):

    def setUp(self):
        # Eventually move this functionality up to prevent duplication
        app = Flask(__name__)
        app.config.from_object('web_package.config.test_config')
        print app.config['SQLALCHEMY_DATABASE_URI']
        app.test_client()                         # Setup a test client to be able to make requests
        db = SQLAlchemy(app)
        db.drop_all()
        db.create_all()
        self.app = app
        self.db = db
        print "Ran setUp"

    def tearDown(self):
        #os.unlink(self.app.config[''])            #Keep to inspect what happened on failure        
        print "Ran tearDown"

    def test_post_creation(self):
        self.assertEqual(True, True, "aaaaahhhhh")
        self.assertEqual(True, True, "Didn't make it past the second test")

    def test_post_validation(self):
        self.assertEqual(True, True, "argh")

    def test_post_blah(self):
        self.assertEqual(True, True, "darn")

    @staticmethod
    def get_suite():
        return unittest.TestLoader().loadTestsFromTestCase(PostTestCase)

if __name__ == '__main__':
    # Create a test suite from test cases
    suite = PostTextCase.get_suite()
    # Create a test suite runner
    runner = unittest.TextTestRunner(verbosity=2)
    # Run the test suite and output human readable results
    runner.run(suite)

