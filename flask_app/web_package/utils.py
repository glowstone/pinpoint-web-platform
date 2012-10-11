import hashlib
import random
import string
from web_package.models import User
from flask import session
from web_package import db


SALT_LENGTH = 16
ALPHANUMERIC = string.letters + string.digits	# List of all characters that can be used to generate a salt


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