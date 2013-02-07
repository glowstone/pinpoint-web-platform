from flask.ext.restless import APIManager
from app_pkg import app
from app_pkg.database import db_session
from app_pkg.blueprints.api.models import User, Question, Geolocation, Answer

from flask import Blueprint         # For creation of custom Blueprints

from controllers import *


# Restless API Bleuprints
manager = APIManager(app, session=db_session)


user_rest_app = manager.create_api_blueprint(
	model=User, 
	# Allow GET requests only.
	methods=['GET'], 
	url_prefix='/api'
)


geolocation_rest_app = manager.create_api_blueprint(
	Geolocation, 
	# Allow GET requests only.
	methods=['GET'], 
	url_prefix='/api'
)


question_rest_app = manager.create_api_blueprint(
	Question,
	# Allow GET, POST, PUT, and DELETE requests.
	methods=['GET', 'POST', 'PUT', 'DELETE'],
	url_prefix='/api',
	preprocessors = {
		'POST': [question_post_preprocessor],
	},
)


answer_rest_app = manager.create_api_blueprint(
	Answer,
	# Allow GET, POST, PUT, and DELETE requests.
	methods=['GET', 'POST', 'PUT', 'DELETE'], 
	url_prefix='/api')


# Custom API Blueprints
#custom_api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import the Routes for the Blueprint App
#import urls

