# Environment Modules
from flask import session, request

# Package Variables
from web_package import db_session

# Package Modules
from models import *
import util

# Libraries
import datetime

# May NOT have access to app
# TODO move form verification and other lengthy code into util. 


# API Account Resource Handlers
###############################################################################

def user_create_json():
    """Create a User from a web form or from Android"""
    response = {}

    # Right now assumes parameters passed as a form. Need to generalize
    form_names = ['username', 'password', 'password_repeat']
    # TODO - write a better functional style utility that returns which names are missing too.
    if not all(request.form.has_key(name) for name in form_names):
        return error_response("Temp message about needing correct names")   #TODO Generalize spec
    
    username = request.form['username']
    password = request.form['password']
    password_retry = request.form['password_repeat']

    # TODO real validation - return errors in json
    
    # TODO take optional latitude, longitude, elevation starting values
    location = Geolocation(0, 0, 0)
    db_session.add(location)
    db_session.commit()                          # Atomicity is somewhat desired here. TODO
    hash, salt = util.hash_password(password)
    user = User(username, hash, salt, location)
    db_session.add(user)
    db_session.commit()
    # Set the session information for the new user

    # Can Android store cookies?
    session['username'] = username

    response['success'] = True
    response['username'] = username
    return response


def user_verify_credentials_json():
    response = {}
    # Right now assumes parameters passed as a form. Need to generalize
    form_names = ['username', 'password']
    # TODO - write a better functional style utility that returns which names are missing too.
    if not all(request.form.has_key(name) for name in form_names):
        return error_response("Temp message about needing correct names")   #TODO Generalize spec
    
    username = request.form['username']
    password = request.form['password']

    if util.check_password(username, password):
        session['username'] = username
        response['success'] = True
    else:
        response['success'] = False
        response['error'] = "Invalid Login"
    return response


def user_current_json():
    """Queries for User corresponding to current session. Returns User object or None if no user found."""
    response = {}
    username = session.get('username', None)
    user = User.query.filter_by(username=username).first()
    print user.password_hash # TODO: Vulnerability, although at least its hashed. SQLAlchemy should support a mode where protected info is not returned.
    
    if user:
        response['success'] = True
        response['user'] = user     # TODO: Big issue. Figure out the cleanest way to serialize SQLAlchemy objects. pickle? dictionary serialize. This has lazy laoding implications for the model as well.
    else:
        response['success'] = False

    return response


def user_set_geolocation_json():
    """Update the user location"""
    response = {}
    form_names = ['latitude', 'longitude', 'elevation']
    # TODO - write a better functional style utility that returns which names are missing too.
    if not all(request.form.has_key(name) for name in form_names):
        return error_response("Temp message about needing correct names")   #TODO Generalize spec

    latitude = request.form['latitude']
    longitude = request.form['longitude']
    elevation = request.form['elevation']

    username = session.get('username', None)
    user = User.query.filter_by(username=username).first()

    geolocation = user.geolocation
    geolocation.latitude = latitude
    geolocation.longitude = longitude
    geolocation.elevation = elevation

    db_session.commit()
    response['success'] = True
    response['latitude'] = latitude
    response['longitude'] = longitude
    response['elevation'] = elevation

    return response


# API Posting Resource Handlers
###############################################################################

POSTING_DELTAS = {'3h': datetime.timedelta(hours=3),
                 '12h': datetime.timedelta(hours=12),
                 '1d': datetime.timedelta(days=1),
                 '3d': datetime.timedelta(days=3),
                 'default': datetime.timedelta(hours=6)}


def posting_create_json():
    user = util.get_current_user()                 # Determine current User
    response = {}

    form_names = ['form_delta']
    if not all(request.form.has_key(name) for name in form_names):
        print "Bad form. Validation error. Do something appropriate"
        return error_response('Invalid form names')

    form_delta = request.form['form_delta']
    if form_delta in POSTING_DELTAS:
        tdelta = POSTING_DELTAS[form_delta]
    else:
        tdelta = POSTING_DELTAS['default']

    # Copy user's location into a new geolocation object.
    user_loc = user.geolocation
    post_loc = Geolocation(user_loc.latitude, user_loc.longitude, user_loc.elevation)
    db_session.add(post_loc)
    db_session.commit()

    posting = Posting(tdelta, user, post_loc)    # Raw postings have no title or text. Won't actually be used.  
    # Need to check success status
    db_session.add(posting)
    db_session.commit()

    response['success'] = True
    response['error'] = None
    return response
    
    
def error_response(message):
    return {'success': False, \
            'error': message}

# Question
###############################################################################

def question_create_json():
    """Create a Question from a Form or from Android"""
    user = util.get_current_user()                 # Determine current User
    response = {}

    form_names = ['title', 'query', 'form_delta']
    if not all(request.form.has_key(name) for name in form_names):
        print "Bad form. Validation error. Do something appropriate"
        return error_response('Invalid form names')

    form_delta = request.form['form_delta']
    if form_delta in POSTING_DELTAS:
        tdelta = POSTING_DELTAS[form_delta]
    else:
        tdelta = POSTING_DELTAS['default']

    title = request.form['title']
    query = request.form['query']
    # Copy user's location into a new geolocation object.
    user_loc = user.geolocation
    question_loc = Geolocation(user_loc.latitude, user_loc.longitude, user_loc.elevation)
    db_session.add(question_loc)
    db_session.commit()

    question = Question(tdelta, user, question_loc, title, query)   
    # Need to check success status
    db_session.add(question)
    db_session.commit()

    response['success'] = True
    response['error'] = None
    return response

def question_list_json():
    questions = Question.query.filter_by().all()
    response = {}
    response['questions'] = questions
    response['success'] = True
    response['error'] = None
    return response

def question_list_json2():
    questions = Question.query.filter_by().all()
    return questions

def question_get_json(id, include_comments=False, include_answers=False):
    print id, type(id)
    print include_answers, type(include_answers)
    print include_comments, type(include_comments)
    question = Question.query.filter_by(question_id=id).first()
    return question


def question_view_json(id):
    # Maybe easier to just return object or None?
    response = {}
    question = Question.query.filter_by(question_id=id).first()
    if question:
        response['success'] = True
        response['question'] = question
    else:
        response['success'] = False
    return response


def question_view_json2(id):
    # Maybe easier to just return object or None?
    question = Question.query.filter_by(question_id=id).first()
    return question

# Answer
###############################################################################
    

def answer_create_json():
    """Create an Answer from a form or from Android"""
    user = util.get_current_user()                 # Determine current User
    response = {}

    form_names = ['question_id', 'text']

    if not all(request.form.has_key(name) for name in form_names):
        print "Bad form. Validation error. Do something appropriate"
        return error_response('Invalid form names')

    question_id = int(request.form['question_id'])
    question = Question.query.filter_by(question_id=question_id).first()
    # Use the question's tdelta
    tdelta = question.expiration_time - question.creation_time

    text = request.form['text']
    
    # Copy user's location into a new geolocation object.
    user_loc = user.geolocation
    answer_loc = Geolocation(user_loc.latitude, user_loc.longitude, user_loc.elevation)
    db_session.add(answer_loc)
    db_session.commit()

    answer = Answer(tdelta, user, answer_loc, question, text)    
    # Need to check success status
    db_session.add(answer)
    db_session.commit()

    response['success'] = True
    response['error'] = None
    return response


def comment_create_json():
    """Create a Comment from a form or from Android"""
    user = util.get_current_user()                 # Determine current User
    response = {}

    form_names = ['commentable_id', 'text']

    if not all(request.form.has_key(name) for name in form_names):
        print "Bad form. Validation error. Do something appropriate"
        return error_response('Invalid form names')

    commentable_id = int(request.form['commentable_id'])
    commentable = Commentable.query.filter_by(commentable_id=commentable_id).first()
    # Use the question's tdelta
    tdelta = commentable.expiration_time - commentable.creation_time

    text = request.form['text']
    
    # Copy user's location into a new geolocation object.
    user_loc = user.geolocation
    comment_loc = Geolocation(user_loc.latitude, user_loc.longitude, user_loc.elevation)
    db_session.add(comment_loc)
    db_session.commit()

    comment = Comment(tdelta, user, comment_loc, commentable, text)
    # Need to check success status
    db_session.add(comment)
    db_session.commit()

    response['success'] = True
    response['error'] = None
    return response



