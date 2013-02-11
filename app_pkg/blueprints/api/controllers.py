# Environment Modules
from flask import session, request
from flask.ext.restless import APIManager, ProcessingException
from flask.ext.restless.views import jsonpify

from app_pkg.database import db_session
from app_pkg.blueprints.api.models import User, Question, Answer

from app_pkg import app
import util

# Libraries
import datetime


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


def question_delete_preprocessor(instid):
    """Accepts a single argument, `instid`, which is the primary key of
    the instance which will be deleted. Return value is ignored.
    Checks that the authenticated user is also the Question author since
    only that User may delete a Question. 
    """
    print "Got here"
    question = Question.query.get(instid)
    if question:
        if session.get('user').id == question.author.id:
            return
        else:
            raise ProcessingException(message='Not Authorized',
                                  status_code=401)
    else:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)


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
    methods=['GET', 'PUT'],
    url_prefix='/api',
    include_columns = ['id', 'username', 'latitude', 'longitude', 'profile_img_url', 'questions', 'questions.id', 'answers', 'answers.id', 'gcm_registration_id'],
    results_per_page = -1,        # Disable pagination
)


question_rest_app = manager.create_api_blueprint(
    model = Question,
    methods=['GET', 'POST', 'DELETE'],
    url_prefix='/api',
    include_columns = ['id', 'title', 'text', 'latitude', 'longitude', 'author', 'author.id', 'author.username', 'author.profile_img_url', 'answers', 'answers.id'],
    preprocessors = {
        'POST': [question_post_preprocessor],
        'DELETE': [question_delete_preprocessor],
    },
    results_per_page = -1,        # Disable pagination
)


answer_rest_app = manager.create_api_blueprint(
    Answer,
    methods=['GET', 'POST', 'PUT', 'DELETE'], 
    url_prefix='/api',
    include_columns = ['id', 'text', 'latitude', 'longitude', 'author', 'author.id', 'author.username', 'author.profile_img_url'],
    preprocessors = {
        'POST': [answer_post_preprocessor],
    },
    results_per_page = -1,       # Disable pagination
)      




