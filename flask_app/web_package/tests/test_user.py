from web_package import user, utils, connect_db
import unittest
import web_package


class UserTestCase(unittest.TestCase):
	def setUp(self):
		web_package.app.config['DATABASE'] = 'db/test.db'
		web_package.app.config['TESTING'] = True
		self.app = web_package.app.test_client()
		web_package.init_db()
		self.db = connect_db()
		
		self.username = 'test'
		self.password = 'test'

	def test_create_user(self):
		# The database should contain zero users because it was just initialized
		number_of_users = len(self.db.execute('select * from users').fetchall())
		unittest.TestCase.assertEqual(self, number_of_users, 0)

		# Now create a new user
		u = user.User.create(self.username, self.password)
		unittest.TestCase.assertEqual(self, u.username, self.username)

		# Now there should be one user in the database
		number_of_users = len(self.db.execute('select * from users').fetchall())
		unittest.TestCase.assertEqual(self, number_of_users, 1)