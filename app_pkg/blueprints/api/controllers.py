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
    include_columns = ['id', 'username', 'profile_img_url', 'questions', 'questions.id', 'answers', 'answers.id', 'gcm_registration_id'],
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




