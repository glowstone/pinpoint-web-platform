import os
import hashlib
import string
import random
import datetime
#from web_package.models import *
from flask import session, request, redirect, url_for
from functools import wraps
from gcm import GCM


#Characters used to generate a hash
ALPHANUMERIC = string.ascii_letters + string.digits
# Default salt length (in bytes) equal to 512 bit output of sha512 hash 
SALT_LENGTH = 64
EARTH_RADIUS_METERS = 6371000   # Radius of the earth, in kilometers

# Crypto
###############################################################################


def login_required(f):
    """Checks that the user has an authenticated session. Otherwise redirect
    to the index page to login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('web.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def random_salt(salt_length=SALT_LENGTH):
    """Return a salt_length string of cryptographically random bytes."""
    return ''.join([random.choice(ALPHANUMERIC) for i in xrange(salt_length)])


def hash_w_salt(password, salt):
    """Return a hashlib sha512 hash of the combined input password and input salt."""
    return hashlib.sha512(password + salt).hexdigest()

def is_authenticated(attempt, salt, hash):
    """Returns True if hash of the password attempt and salt 
    is equal to the provided hash value."""
    return hashlib.sha512(attempt + salt).hexdigest() == hash


def unpack_arguments(required_arg_names=[]):
    arguments = {}
    for key in request.values.keys(): # Combined MultiDict of request.form and request.args
        arguments[key] = request.values[key]
    # Check for required arguments  
    for arg in required_arg_names:
        if arg not in arguments:
            return None
    return arguments

def success_response(data):
    """
    Returns a dictionary representing a successful API that returns some data.
    Accepts: data that should be send in the 'data' field.
    """
    response = {'success': True, 'error': None}
    response['data'] = data
    return response


def error_response(error):
    """
    Returns a dictionary representing a failed internal API call.
    Accepts: an error message that should be included in the dictionary response.
    """
    response = {'success': False, 'data': None}
    response['error'] = error
    return response


class AAM(object):
    """The API Argument Manager
    An API Argument Manager which is an abstract representation of the arguments an API
    function takes, how those unicode passed values should be converted, and which arguments
    are required/optional""" 

    def __init__(self):
        self.arguments = []

    def add_argument(self, external_name, internal_name, python_type, optional):
        api_argument = APIArgument(external_name, internal_name, python_type, optional)
        self.arguments.append(api_argument)

    def cast_args_to_python(self):
        """Cast unicode arguments (possibly from URL get parameters) to Python"""
        for argument in self.arguments:
            success = argument.unicode_to_python()
            if not success:             # API call should fail bc an argument is invalid
                return None
        return self.arguments

# TODO 'warning' for errors in optional argument which does not cause total failure of the api call

# TODO add custom error messages or maybe custom requirements (integer has to be in a particular range)

class APIArgument(object):
    def __init__(self, external_name, internal_name, python_type, optional):
        """
        Represents an API argument object
        Expects: Name of argument in public API, name of argument in internal functions,
            Python type passed unicode values should be converted to, whether argument is 
            optional"""  
        self.external_name = external_name 
        self.internal_name = internal_name
        self.python_type = python_type           # number, string, or boolean
        # TODO currently assumes you choose a valid python type. Need to enforce.
        self.optional = optional
        # TODO - enforce that this is a boolean                 
        self.arg_value = None

    def unicode_to_python(self):
        pass
        # Whoa, Python has no switch
        # switch (self.python_type):
        #     case 'number':
        #         #Allow int or float or have separate?
        #         pass
        #         break
        #     case 'string':
        #         pass
        #         break
        #     case 'boolean':
        #         pass
        #         break
        #     case 'default':
        #         print 'Bad APIArgument type'
        #         break


def send_gcm_message(users, data):
    """
    Sends a push notification consisting of the JSON object data to each user in users.
    """
    API_KEY = "AIzaSyBdPfe8aggpF5PyiClufQt62gjjLbbVyeY"
    gcm = GCM(API_KEY)
    reg_ids = [user.gcm_registration_id for user in users]
    response = gcm.json_request(registration_ids=reg_ids, data=data)


# def get_sql_distance_query(location, radius, num):
#   """
#   Constructs the SQL query to get the num closest locations within the radius to the given location.
#   Requires:None?
#   Affects:None
#   """
#   goal_latitude = location.latitude
#   goal_longitude = location.longitude

#   # Source: https://developers.google.com/maps/articles/phpsqlsearch_v3?hl=hu-HU
#   # A query to find the closest posts to the goal, sorted by distance. Distance computed using haversine formula.
#   query = """SELECT %s.id, ( %f * acos( cos( radians(%f) ) * cos( radians( %s.latitude ) ) * cos( radians( %s.longitude ) - 
#           radians(%f) ) + sin( radians(%f) ) * sin( radians( %s.latitude ) ) ) ) 
#       AS distance 
#       FROM %s, %s 
#       WHERE %s.geolocation_id = %s.id
#       HAVING distance < %f
#       ORDER BY distance LIMIT 0 , %d;"""

#   # Add in the parameters to the query
#   query = query % ('post', EARTH_RADIUS, location.latitude, 'geolocation', 'geolocation', location.longitude, location.latitude, 
#                    'geolocation', 'geolocation', 'post', 'post', 'geolocation', radius, num)
#   return query


# def closest_posts(location, radius, num=10):
#   """
#   Gets the query and executes it to find the num closest geolocations within the radius to the location. Returns
#   tuples of (geolocation, distance)
#   Requires:
#   Affects:
#   """
#   # Get the query needed to find the closest locations
#   query = get_sql_distance_query(location, radius, num)
#   conn = db.session.connection()
#   # Execute the query to get the post IDs and the distances to each
#   result = conn.execute(query).fetchall()
#   ids = [item[0] for item in result]
#   distances = [item[1] for item in result]
#   # Get the Post objects from the returned IDs
#   # TODO: Is there a bulk select in SQLAlchemy? This does a query for each ID instead of a single query for all IDs.
#   posts = [Post.query.get(id) for id in ids]
#   # Return tuples of (Geolocation, distance)
#   return zip(posts, distances)
# =======
#   #Handle when session is not defined
#   try:
#       username = session['username']
#       user = User.query.filter_by(username=username).first()
#   except:
#       user = None
#   return user

# def create_post(title, text, form_tdelta, user, geolocation):
#   """
#   Attempts to create Post object belonging to a user and pinned to a geolocation. Returns the newly 
#   created Post or None upon failure.
#   Requires: user, geolocation objects already exist in db
#   Affects: Post object table
#   """ 
#   creation_time = datetime.datetime.now()

#   # TODO: Do Browser datetime to Python datetime conversion instead maybe
#   if form_tdelta in POST_DELTAS:
#       tdelta = POST_DELTAS[form_tdelta]
#   else:
#       tdelta = POST_DELTAS['default']

#   expiration_time = creation_time + tdelta

#   # Create Post object belonging to current user and positioned at a specific geolocation.
#   post = Post(title, text, creation_time, expiration_time, user.id, geolocation.id)
#   db.session.add(post)
#   db.session.commit()
#   return post


# def create_geolocation(latitude, longitude, elevation):
#   """
#   Attempts to create and return a new Geolocation obj. Returns None upon failure
#   Requires: 
#   Affects: Geolocation object table
#   """ 
#   gloc = Geolocation(latitude, longitude, elevation)
#   db.session.add(gloc)
#   db.session.commit()
#   return gloc


# def get_sql_distance_query(location, radius, num):
#   """
#   Constructs the SQL query to get the num closest locations within the radius to the given location.
#   Requires:None?
#   Affects:None
#   """
#   goal_latitude = location.latitude
#   goal_longitude = location.longitude

#   # Source: https://developers.google.com/maps/articles/phpsqlsearch_v3?hl=hu-HU
#   # A query to find the closest posts to the goal, sorted by distance. Distance computed using haversine formula.
#   query = """SELECT %s.id, ( %f * acos( cos( radians(%f) ) * cos( radians( %s.latitude ) ) * cos( radians( %s.longitude ) - 
#           radians(%f) ) + sin( radians(%f) ) * sin( radians( %s.latitude ) ) ) ) 
#       AS distance 
#       FROM %s, %s 
#       WHERE %s.geolocation_id = %s.id
#       HAVING distance < %f
#       ORDER BY distance LIMIT 0 , %d;"""

#   # Add in the parameters to the query
#   query = query % (Post.__tablename__, EARTH_RADIUS_METERS, location.latitude, Geolocation.__tablename__,
#                    Geolocation.__tablename__, location.longitude, location.latitude, Geolocation.__tablename__,
#                    Geolocation.__tablename__, Post.__tablename__, Post.__tablename__, Geolocation.__tablename__,
#                    radius, num)
#   return query


# def closest_posts(location, radius, num=10):
#   """
#   Gets the query and executes it to find the num closest geolocations within the radius to the location. Returns
#   list of dictionaries with 'post', 'latitude', 'longitude', and 'distance' keys
#   Requires:
#   Affects:
#   """
#   # Get the query needed to find the closest locations
#   query = get_sql_distance_query(location, radius, num)
#   conn = db.session.connection()
#   # Execute the query to get the post IDs and the distances to each
#   result = conn.execute(query).fetchall()
#   ids = [item[0] for item in result]
#   distances = [item[1] for item in result]
#   # Get the Post objects from the returned IDs
#   # TODO: Is there a bulk select in SQLAlchemy? This does a query for each ID instead of a single query for all IDs.
#   posts = [Post.query.get(id) for id in ids]
    
#   # Construct a list of dictionaries to represent the post objects
#   post_dicts = []
#   for i in xrange(len(posts)):
#       post = posts[i]
#       latitude = post.geolocation.latitude
#       longitude = post.geolocation.longitude
#       distance = distances[i]
#       post_dicts.append(dict(post = post, latitude = latitude, longitude = longitude, distance = distance))
#   return post_dicts

