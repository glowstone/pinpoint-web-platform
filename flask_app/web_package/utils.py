import hashlib
import random
import string


SALT_LENGTH = 16
ALPHANUMERIC = string.letters + string.digits	# List of all characters that can be used to generate a salt


def hash_password(password):
	"""
	Generate a sha256 hash for the given password plus a salt, and return both the hash and the salt.
	"""
	salt = ''.join([random.choice(ALPHANUMERIC) for i in xrange(SALT_LENGTH)])
	hash = hashlib.sha256(password + salt)
	return (hash.hexdigest(), salt)