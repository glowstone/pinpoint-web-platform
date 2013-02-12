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

def user_put_single_preprocessor(instid, data):
    """Accepts two arguments, `instid`, the primary key of the
    instance of the model to put, and `data`, the dictionary of fields
    to change on the instance.

    This function must return a dictionary representing the fields to
    change in the specified instance of the model (that is, a modified
    version of `data`).

    Ensures that only an authenticated User may edit his/her User entry. Further
    ensures that only the latitude, longitude, or gcm_registraion_id fields may
    be edited.
    """
    user = session.get('user', False)
    user_object = User.query.get(instid)
    if user.id == user_object.id:
        include_fields = ['latitude' , 'longitude', 'gcm_registration_id']
        changed = {}
        for field in include_fields:
            if field in data:
                changed[field] = data[field]
        return changed
    else:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)


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


def question_post_postprocessor(data):
    """Accepts a single argument, `data`, which is the dictionary
    representation of the created instance of the model.
    This function must return a dictionary representing the JSON to
    return to the client.

    Execution reaches this point when a new question has been successfully
    created. An Android GCM Push notification is made to users to 
    notify them of the new Question
    """
    user = session.get('user', False)
    # Send a GCM message
    users = User.query.filter(User.id != user.id).all()
    util.send_gcm_message(users, {'data': 'New message'})

    return data


def question_delete_preprocessor(instid):
    """Accepts a single argument, `instid`, which is the primary key of
    the instance which will be deleted. Return value is ignored.
    Checks that the authenticated user is also the Question author since
    only that User may delete a Question. 
    """
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


def answer_delete_preprocessor(instid):
    """Accepts a single argument, `instid`, which is the primary key of
    the instance which will be deleted. Return value is ignored.
    Checks that the authenticated user is also the Answer author or that
    the authenticated User is the author of the answer's associated Question
    (since deleting a Question removes the Answers).
    """
    answer = Answer.query.get(instid)
    if answer:
        user_id = session.get('user').id
        if user_id == answer.author.id or user_id == answer.question.author.id:
            return
        else:
            raise ProcessingException(message='Not Authorized',
                                  status_code=401)
    else:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)




# RESTless API
###############################################################################

# Restless API Bleuprints
manager = APIManager(app, session=db_session)

user_rest_app = manager.create_api_blueprint(
    model=User, 
    methods=['GET', 'PUT'],
    url_prefix='/api',
    include_columns = ['id', 'username', 'latitude', 'longitude', 'profile_img_url', 'questions', 'questions.id', 'answers', 'answers.id', 'gcm_registration_id'],
    preprocessors = {
        'PATCH_SINGLE': [user_put_single_preprocessor],    # PATCH is alias for PUT
    },
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
    postprocessors = {
        'POST': [question_post_postprocessor],
    },
    results_per_page = -1,        # Disable pagination
)


answer_rest_app = manager.create_api_blueprint(
    Answer,
    methods=['GET', 'POST', 'DELETE'], 
    url_prefix='/api',
    include_columns = ['id', 'text', 'latitude', 'longitude', 'author', 'author.id', 'author.username', 'author.profile_img_url'],
    preprocessors = {
        'POST': [answer_post_preprocessor],
        'DELETE': [answer_delete_preprocessor],
    },
    results_per_page = -1,       # Disable pagination
)      




