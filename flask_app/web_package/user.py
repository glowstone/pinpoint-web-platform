from utils import hash_password
from web_package import connect_db


class User(object):
	def __init__(self, username, password, hash=None, latitude=None, longitude=None):
		self.username = username
		self.set_password(password)
		self.set_location(latitude, longitude)

	def set_password(self, password):
		"""
		Set the user's password hash, and get a salt for them. password is a string
		"""
		self.password_hash, self.salt = hash_password(password)

	def set_location(self, latitude, longitude):
		"""
		Set the user's location, latitude and longitude are ints.
		"""
		self.latitude = latitude
		self.longitude = longitude

	def get_location(self):
		return (self.latitude, self.longitude)

	def save(self):
		"""
		Wrapper around the database insert for the User
		"""
		object_dict = self.__dict__
		print object_dict
		query = "insert or replace into users (username, hash, salt, latitude, longitude) values (?, ?, ?, ?, ?)"

		db = connect_db()
		db.execute(query, [object_dict['username'], object_dict['password_hash'], object_dict['salt'], 
						   object_dict['latitude'], object_dict['longitude']])
		db.commit()
		db.close()

	@staticmethod
	def get(username):
		"""
		Wrapper around the query to get a User object from the database.
		"""
		query = "select * from users where username = ?"
		db = connect_db()
		result = db.execute(query, [username]).fetchone()
		db.close()
		return User(result[0], result[1], result[2], result[3], result[4])
