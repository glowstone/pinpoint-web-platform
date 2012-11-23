import hashlib
import random
import string
import datetime
from web_package.models import *
from flask import session, request

# Utilities should NOT have access to application specific models.

# from functools import wraps

SALT_LENGTH = 16
ALPHANUMERIC = string.letters + string.digits   # List of all characters that can be used to generate a salt
EARTH_RADIUS_METERS = 6371000   # Radius of the earth, in kilometers

POST_DELTAS = {'3h': datetime.timedelta(hours=3),
               '6h': datetime.timedelta(hours=6),
               '12h': datetime.timedelta(hours=12),
               '1d': datetime.timedelta(days=1),
               '3d': datetime.timedelta(days=3),
               'default': datetime.timedelta(hours=6)}


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


def check_password(username, password):
    u = User.query.filter_by(username=username).first()
    if u == None:
        return False
    else:
        password_guess = hash_password(password, u.salt)[0]
        if u.password_hash == password_guess:
            return True
        else:
            return False


def unpack_arguments(required_arg_names=[]):
    arguments = {}
    for key in request.values.keys(): # Combined MultiDict of request.form and request.args
        arguments[key] = request.values[key]
    # Check for required arguments  
    for arg in required_arg_names:
        if arg not in arguments:
            return None
    return arguments

def success_response(data, warning=None):
    return {"success": True, \
            "data": data, \
            "warning": warning, \
            "error": None \
            }

def error_response(error_msg, warning=None):
    result = {"success": False, \
              "data": None, \
              "warning": None, \
              "error": error_msg \
             }
    print 'HERE', result
    return result

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


# def create_user(username, password):
#   # Create a new location for the User
#   location = create_geolocation(None, None, None)
#   db.session.add(location)
#   db.session.commit()
#   # Hash the password provided in the new user form. Store the hashed value and the salt used in the hash.
#   hash, salt = hash_password(password)
#   user = User(username, hash, salt, location.id)
#   # Insert the user object into the database
#   db.session.add(user)
#   db.session.commit()
#   # Set the session information for the new user
#   do_login(username)


# def do_login(username):
#   session['username'] = username
#   session['logged_in'] = True          


# def do_logout():
#   session.pop('username', None)        #Remove username from session, if its defined.
#   session['logged_in'] = False


def get_current_user():
    """Queries for User corresponding to current session. Returns User object or None if no user found."""
    username = session.get('username', None)
    user = User.query.filter_by(username=username).first()       
    return user

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

