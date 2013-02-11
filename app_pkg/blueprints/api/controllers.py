# Environment Modules
from flask import session, request
from flask.ext.restless import APIManager, ProcessingException
from flask.ext.restless.views import jsonpify

from app_pkg.database import db_session
from app_pkg.blueprints.api.models import User, Question, Geolocation, Answer

from app_pkg import app
import util

# Libraries
import datetime

# May NOT have access to app
# TODO move form verification and other lengthy code into util. 

# REST API Preprocessors and PostProcessors
###############################################################################

def question_post_preprocessor(data):
    """Accepts a single argument, 'data', which is the dictionary of
    fields to set on the new instance of the model.
    This function must return a dictionary representing the fields to
    set on the new instance of the model.
    """
    user = session.get('user', False)
    if user:
        data['user_id'] = user.id
    else:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)
    return data

def answer_post_preprocessor(data):
    """Accepts a single argument, 'data', which is the dictionary of
    fields to set on the new instance of the model.
    This function must return a dictionary representing the fields to
    set on the new instance of the model.
    """
    user = session.get('user', False)
    if user:
        data['user_id'] = user.id
    else:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)
    return data


# RESTless API
###############################################################################

# Restless API Bleuprints
manager = APIManager(app, session=db_session)

user_rest_app = manager.create_api_blueprint(
    model=User, 
    methods=['GET'],
    url_prefix='/api',
    include_columns = ['id', 'username', 'profile_img_url', 'questions', 'questions.id', 'answers', 'answers.id'],
    results_per_page = -1,        # Disable pagination
)


question_rest_app = manager.create_api_blueprint(
    model = Question,
    methods=['GET', 'POST', 'PUT', 'DELETE'],
    url_prefix='/api',
    include_columns = ['id', 'title', 'text', 'latitude', 'longitude', 'author', 'author.username', 'author.profile_img_url', 'answers', 'answers.id'],
    preprocessors = {
        'POST': [question_post_preprocessor],
    },
    results_per_page = -1,        # Disable pagination
)


answer_rest_app = manager.create_api_blueprint(
    Answer,
    methods=['GET', 'POST', 'PUT', 'DELETE'], 
    url_prefix='/api',
    include_columns = ['id', 'text', 'latitude', 'longitude', 'author', 'author.username', 'author.profile_img_url'],
    preprocessors = {
        'POST': [answer_post_preprocessor],
    },
    results_per_page = -1,       # Disable pagination
)      






# API Account Resource Handlers
###############################################################################

def user_create(username, email, password):
    """Create a new User"""
    # TODO real validation - return errors in json
    # TODO take optional latitude, longitude, elevation starting values
    # Crude validation checks
    if len(username) < 3:
        return util.error_response("Username too short")
    
    location = Geolocation(0, 0, 0)
    db_session.add(location)
    db_session.commit()                          # Atomicity is somewhat desired here. TODO
        
    salt = util.random_salt()
    password_hash = util.hash_w_salt(password, salt)
    user = User(username, email, password_hash, salt, location)
    db_session.add(user)
    try:
        db_session.commit()
    except Exception:               # SQLAlchemyError would be better, but not sure how to import it.
        db_session.rollback()       # TODO: Does not rollback geolocation creation as we would like
        return util.error_response("Database error creating User")
        
    return util.success_response(data=user)


def user_authenticate(user_identifier, password):
    """Authenticate the user with either email or password"""
    # Try to authenticate with Username
    user = User.query.filter_by(username=user_identifier).first()
    if user is not None:
        if util.is_authenticated(password, user.salt, user.password_hash):
            return util.success_response(data=user)
        else:
            return util.error_response('Invalid password')
    # Try to authenticate with Email
    else:
        user = User.query.filter_by(email=user_identifier).first()
        if user is not None:
            if util.is_authenticated(password, user.salt, user.password_hash):
                return util.success_response(data=user)
            else:
                return util.error_response('Invalid password')
        else:
            return util.error_response('No User with that username or email')



def user_show_json(username):
    """Queries for the given user. Check whether that is the current user"""
    user = User.query.filter_by(username=username).first()
    authenticated_user_id = session.get("user_id", None)
    if user:
        if user.user_id == authenticated_user_id:       # Authenticated User
            return util.success_response({"user": user, "authenticated": True})
        else:                                           # Unauthenticated User (public profile will be shown)
            return util.success_response({"user": user, "authenticated": False})
    else:
        return util.error_response("No user with username " + username)


def current_session_user():
    """Internal Method for finding the User object corresponding to the current authenticated request session"""
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return util.success_response(user)
        else:
            return util.error_response("No user found with Session's user_id")
    else:
        return util.error_response("Session does not contain a user_id")


def user_set_geolocation_json(latitude, longitude, elevation=None):
    """Update's the authenticated user's Geolocation"""
    user = current_session_user()['data']
    if user:
        latitude = float(latitude)        # Take out when argument manager is created
        longitude = float(longitude)      # Take out when argument manager is created
        # Update Geolocation
        geolocation = user.geolocation
        geolocation.latitude = latitude
        geolocation.longitude = longitude
        if elevation:
            geolocation.elevation = elevation
        db_session.commit()
        return util.success_response()
    else:
        return util.error_response("Session user was not found.")



POSTING_DELTAS = {'3h': datetime.timedelta(hours=3),
                 '12h': datetime.timedelta(hours=12),
                 '1d': datetime.timedelta(days=1),
                 '3d': datetime.timedelta(days=3),
                 'default': datetime.timedelta(hours=6)}

# Question
###############################################################################

def question_create_json():
    """Create a Question from a Form or from Android"""
    user = util.get_current_user()                 # Determine current User
    response = {}

    form_names = ['title', 'query', 'form_delta']
    if not all(request.form.has_key(name) for name in form_names):
        print "Bad form. Validation error. Do something appropriate"
        return util.error_response('Invalid form names')

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


class TestQuestion():
    def __init__(self):
        self.title = 'server title'
        self.text = 'server text'


def questions():
    """Retrieve all questions, possibly filtered by some selectors"""
    questions = Question.query.filter_by().all()
    questions = [TestQuestion(), TestQuestion()]
    questions = [{'title': 'thing', 'text': 'that'}]
    print "Got the questions"
    print questions
    return questions


def question_list_json(order_by="radius", include_comments=False, include_answers=False):
    # TODO - make readius work again.
    questions = Question.query.filter_by().all()
    return questions

def question_get_json(question_id, include_comments=False, include_answers=False):
    """Retrieve the Question with question_id 'id'."""
    print id, type(id)
    print include_answers, type(include_answers)
    print include_comments, type(include_comments)
    question = Question.query.filter_by(question_id=question_id).first()
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

def answer_list_json(question_id, include_comments=False):
    """Retrieve all answers for a Question with question_id 'question_id'"""
    answers = Answer.query.filter_by(question_id=question_id).all()
    return answers


def answer_get_json(answer_id, include_comments=False):
    print answer_id
    """Retrieve the Answer with a particular answer_id"""
    print answer_id, type(id)
    print include_comments, type(include_comments)
    answer = Answer.query.filter_by(answer_id=answer_id).first()
    return answer


# Comments
###############################################################################


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


def comment_list_json(commentable_id):
    """Retrieve all comments for the Commentable with commentable_id 'commentable_id''"""
    comments = Comment.query.filter_by(commentable_id=commentable_id).all()
    return comments


def comment_get_json(comment_id):
    """Retrieve a comment with a particular comment_id"""
    print comment_id, type(id)
    comment = Comment.query.filter_by(comment_id=comment_id).first()
    return comment



