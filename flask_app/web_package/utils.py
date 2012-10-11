import hashlib
import random
import string
import datetime
from web_package.models import User, Post, Geolocation
from flask import session
from web_package import db


SALT_LENGTH = 16
ALPHANUMERIC = string.letters + string.digits	# List of all characters that can be used to generate a salt

POST_DELTAS = {'3h': datetime.timedelta(hours=3),
		   '6h': datetime.timedelta(hours=6),
		   '12h': datetime.timedelta(hours=12),
		   '1d': datetime.timedelta(days=1),
		   '3d': datetime.timedelta(days=3),
		   'default': datetime.timedelta(hours=6)}

def hash_password(password, salt=None):
	"""
	Generate a sha256 hash for the given password plus a salt, and return both the hash and the salt.
	"""
	print "Salt: ", salt
	if not salt:
		salt = ''.join([random.choice(ALPHANUMERIC) for i in xrange(SALT_LENGTH)])
	hash = hashlib.sha256(password + salt)
	return (hash.hexdigest(), salt)


def check_password(username, password):
	# TODO: exception handling
	u = User.query.filter_by(username=username).first()
	password_guess = hash_password(password, u.salt)[0]
	if u.password_hash == password_guess:
		return True
	else:
		return False


def create_user(username, password):
	# Hash the password provided in the new user form. Store the hashed value and the salt used in the hash.
	hash, salt = hash_password(password)
	user = User(username, hash, salt)
	# Insert the user object into the database
	db.session.add(user)
	db.session.commit()
	# Set the session information for the new user
	do_login(username)


def do_login(username):
	session['username'] = username
	session['logged_in'] = True


def do_logout():
	session['username'] = None
	session['logged_in'] = False

def get_current_user():
	#Handle when session is not defined
	username = session['username']
	user = User.query.filter_by(username=username).first()
	print user
	if user == None:
		print "Bad, probably redirect to login here"
	return user

def create_post(title, text, user, duration):
	# Need to think about when to really create geolocation
	geolocation = Geolocation(42.355751, -71.099474, 40.0)
	db.session.add(geolocation)
	db.session.commit()
	post_geolocation = Geolocation.query.filter_by(id=1).first()
	# TODO take out hard coded geolocation

	creation_time = datetime.datetime.now()

	if duration in POST_DELTAS:
		tdelta = POST_DELTAS[duration]
	else:
		tdelta = POST_DELTAS['default']

	expiration_time = creation_time + tdelta

	# Create Post object belonging to current user and positioned at a specific geolocation.
	post = Post(title, text, creation_time, expiration_time, user.id, geolocation.id)
	db.session.add(post)
	db.session.commit()
	# Make return False upon error
	return True
	