from utils import hash_password
from web_package import connect_db


class User(object):
	def __init__(self, username, password_hash, salt):
		self.username = username
		self.password_hash = password_hash
		self.salt = salt

	@staticmethod
	def create(username, password):
		"""
		Used when a new User is created, which is used differently from the class constructor (which isn't
		necessarily used for creating a new User in the database, so they're separated into different functions).
		"""
		password_hash, salt = hash_password(password)
		u = User(username, password_hash, salt)
		u.save()
		return u

	def set_password(self, password):
		"""
		Set the user's password hash, and get a salt for them. password is a string
		"""
		self.password_hash, self.salt = hash_password(password)

	def save(self):
		"""
		Wrapper around the database upsert for the User. You need to call save if you want to insert the 
		object into the database or save changes to it.
		"""
		object_dict = self.__dict__
		print object_dict
		query = "insert or replace into users (username, hash, salt) values (?, ?, ?)"

		db = connect_db()
		db.execute(query, [object_dict['username'], object_dict['password_hash'], object_dict['salt']])
		db.commit()
		db.close()

	@staticmethod
	def get_from_username(username):
		"""
		Wrapper around the query to get a User object from the database.
		"""
		query = "select * from users where username = ?"
		db = connect_db()
		result = db.execute(query, [username]).fetchone()
		db.close()
		return User(result[0], result[1], result[2], result[3], result[4])
