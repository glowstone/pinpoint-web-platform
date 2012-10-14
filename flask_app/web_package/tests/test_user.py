from flask import Flask
import flask
from flask.ext.sqlalchemy import SQLAlchemy
import web_package
import unittest
import os
from web_package import db
from web_package.models import User


class UserTestCase(unittest.TestCase):
	def setUp(self):
		dialect = "sqlite:////"
		web_package.app.config['TESTING'] = True
		web_package.app.config['SQLALCHEMY_DATABASE_URI'] = dialect + os.path.join(os.path.dirname(__file__), "db", "testing.sqlite")
		self.app = web_package.app.test_client()
		
		self.test_db = db
		self.test_db.create_all()

	def tearDown(self):
		self.test_db.session.remove()
		self.test_db.drop_all()

	def create_user(self, username, password):
		return self.app.post('/user/create', data=dict(
	        username=username,
	        password=password
	    ), follow_redirects=True)

	def test_create_user(self):
		response = self.create_user('test', 'test')
		assert response.status_code == 200
		count = len(User.query.all())
		assert count == 1
