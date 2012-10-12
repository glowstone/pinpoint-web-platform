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
	# Create a new location for the User
	location = create_geolocation(None, None, None)
	db.session.add(location)
	db.session.commit()
	# Hash the password provided in the new user form. Store the hashed value and the salt used in the hash.
	hash, salt = hash_password(password)
	user = User(username, hash, salt, location.id)
	# Insert the user object into the database
	db.session.add(user)
	db.session.commit()
	# Set the session information for the new user
	do_login(username)


def do_login(username):
	session['username'] = username
	session['logged_in'] = True          


def do_logout():
	session.pop('username', None)        #Remove username from session, if its defined.
	session['logged_in'] = False


def get_current_user():
	"""Queries for User corresponding to current session. Returns User object or None if no user found."""
	#Handle when session is not defined
	username = session['username']
	user = User.query.filter_by(username=username).first()
	return user

def create_post(title, text, form_tdelta, user, geolocation):
	"""
	Attempts to create Post object belonging to a user and pinned to a geolocation. Returns the newly 
	created Post or None upon failure.
	Requires: user, geolocation objects already exist in db
	Affects: Post object table
	""" 
	creation_time = datetime.datetime.now()

	# TODO: Do Browser datetime to Python datetime conversion instead maybe
	if form_tdelta in POST_DELTAS:
		tdelta = POST_DELTAS[form_tdelta]
	else:
		tdelta = POST_DELTAS['default']

	expiration_time = creation_time + tdelta

	# Create Post object belonging to current user and positioned at a specific geolocation.
	post = Post(title, text, creation_time, expiration_time, user.id, geolocation.id)
	db.session.add(post)
	db.session.commit()
	return post


def create_geolocation(latitude, longitude, elevation):
	"""
	Attempts to create and return a new Geolocation obj. Returns None upon failure
	Requires: 
	Affects: Geolocation object table
	""" 
	gloc = Geolocation(latitude, longitude, elevation)
	db.session.add(gloc)
	db.session.commit()
	return gloc
	