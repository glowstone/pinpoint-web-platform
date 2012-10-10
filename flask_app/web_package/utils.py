import hashlib
import random
import string
from web_package.models import User


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