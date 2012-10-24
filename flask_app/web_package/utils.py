import hashlib
import random
import string
import datetime
from web_package.models import *            # To be removed
from flask import session

# Utilities should NOT have access to application specific models.

# from functools import wraps

SALT_LENGTH = 16
ALPHANUMERIC = string.letters + string.digits	# List of all characters that can be used to generate a salt
EARTH_RADIUS_METERS = 6371000	# Radius of the earth, in kilometers

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if get_current_user() is None:
			# TODO: This should probably redirect to a login page rather than index
			return redirect(url_for('index', next=request.url))
		return f(*args, **kwargs)
	return decorated_function


def hash_password(password, salt=None):
	"""
	Generate a sha256 hash for the given password plus a salt, and return both the hash and the salt.
	"""
	if not salt:
		salt = ''.join([random.choice(ALPHANUMERIC) for i in xrange(SALT_LENGTH)])
	hash = hashlib.sha256(password + salt)
	return (hash.hexdigest(), salt)

# TODO - change so that models are not used
def check_password(username, password):
	# TODO: exception handling
	u = User.query.filter_by(username=username).first()
	password_guess = hash_password(password, u.salt)[0]
	if u.password_hash == password_guess:
		return True
	else:
		return False

# Temporary
def get_current_user():
	"""Queries for User corresponding to current session. Returns User object or None if no user found."""
	username = session.get('username', None)
	user = User.query.filter_by(username=username).first()       
	return user






# def get_sql_distance_query(location, radius, num):
# 	"""
# 	Constructs the SQL query to get the num closest locations within the radius to the given location.
# 	Requires:None?
# 	Affects:None
# 	"""
# 	goal_latitude = location.latitude
# 	goal_longitude = location.longitude

# 	# Source: https://developers.google.com/maps/articles/phpsqlsearch_v3?hl=hu-HU
# 	# A query to find the closest posts to the goal, sorted by distance. Distance computed using haversine formula.
# 	query = """SELECT %s.id, ( %f * acos( cos( radians(%f) ) * cos( radians( %s.latitude ) ) * cos( radians( %s.longitude ) - 
# 			radians(%f) ) + sin( radians(%f) ) * sin( radians( %s.latitude ) ) ) ) 
# 		AS distance 
# 		FROM %s, %s 
# 		WHERE %s.geolocation_id = %s.id
# 		HAVING distance < %f
# 		ORDER BY distance LIMIT 0 , %d;"""

# 	# Add in the parameters to the query
# 	query = query % ('post', EARTH_RADIUS, location.latitude, 'geolocation', 'geolocation', location.longitude, location.latitude, 
# 					 'geolocation', 'geolocation', 'post', 'post', 'geolocation', radius, num)
# 	return query


# def closest_posts(location, radius, num=10):
# 	"""
# 	Gets the query and executes it to find the num closest geolocations within the radius to the location. Returns
# 	tuples of (geolocation, distance)
# 	Requires:
# 	Affects:
# 	"""
# 	# Get the query needed to find the closest locations
# 	query = get_sql_distance_query(location, radius, num)
# 	conn = db.session.connection()
# 	# Execute the query to get the post IDs and the distances to each
# 	result = conn.execute(query).fetchall()
# 	ids = [item[0] for item in result]
# 	distances = [item[1] for item in result]
# 	# Get the Post objects from the returned IDs
# 	# TODO: Is there a bulk select in SQLAlchemy? This does a query for each ID instead of a single query for all IDs.
# 	posts = [Post.query.get(id) for id in ids]
# 	# Return tuples of (Geolocation, distance)
# 	return zip(posts, distances)
# =======
# 	#Handle when session is not defined
# 	try:
# 		username = session['username']
# 		user = User.query.filter_by(username=username).first()
# 	except:
# 		user = None
# 	return user

# def get_sql_distance_query(location, radius, num):
# 	"""
# 	Constructs the SQL query to get the num closest locations within the radius to the given location.
# 	Requires:None?
# 	Affects:None
# 	"""
# 	goal_latitude = location.latitude
# 	goal_longitude = location.longitude

# 	# Source: https://developers.google.com/maps/articles/phpsqlsearch_v3?hl=hu-HU
# 	# A query to find the closest posts to the goal, sorted by distance. Distance computed using haversine formula.
# 	query = """SELECT %s.id, ( %f * acos( cos( radians(%f) ) * cos( radians( %s.latitude ) ) * cos( radians( %s.longitude ) - 
# 			radians(%f) ) + sin( radians(%f) ) * sin( radians( %s.latitude ) ) ) ) 
# 		AS distance 
# 		FROM %s, %s 
# 		WHERE %s.geolocation_id = %s.id
# 		HAVING distance < %f
# 		ORDER BY distance LIMIT 0 , %d;"""

# 	# Add in the parameters to the query
# 	query = query % (Post.__tablename__, EARTH_RADIUS_METERS, location.latitude, Geolocation.__tablename__,
# 					 Geolocation.__tablename__, location.longitude, location.latitude, Geolocation.__tablename__,
# 					 Geolocation.__tablename__, Post.__tablename__, Post.__tablename__, Geolocation.__tablename__,
# 					 radius, num)
# 	return query


# def closest_posts(location, radius, num=10):
# 	"""
# 	Gets the query and executes it to find the num closest geolocations within the radius to the location. Returns
# 	list of dictionaries with 'post', 'latitude', 'longitude', and 'distance' keys
# 	Requires:
# 	Affects:
# 	"""
# 	# Get the query needed to find the closest locations
# 	query = get_sql_distance_query(location, radius, num)
# 	conn = db.session.connection()
# 	# Execute the query to get the post IDs and the distances to each
# 	result = conn.execute(query).fetchall()
# 	ids = [item[0] for item in result]
# 	distances = [item[1] for item in result]
# 	# Get the Post objects from the returned IDs
# 	# TODO: Is there a bulk select in SQLAlchemy? This does a query for each ID instead of a single query for all IDs.
# 	posts = [Post.query.get(id) for id in ids]
	
# 	# Construct a list of dictionaries to represent the post objects
# 	post_dicts = []
# 	for i in xrange(len(posts)):
# 		post = posts[i]
# 		latitude = post.geolocation.latitude
# 		longitude = post.geolocation.longitude
# 		distance = distances[i]
# 		post_dicts.append(dict(post = post, latitude = latitude, longitude = longitude, distance = distance))
# 	return post_dicts

