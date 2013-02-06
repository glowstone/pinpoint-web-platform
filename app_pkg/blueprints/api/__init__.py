from flask.ext.restless import APIManager
from app_pkg import app
from app_pkg.database import db_session
from app_pkg.blueprints.api.models import User, Question, Geolocation, Answer

from flask import Blueprint         # For creation of custom Blueprints


# Restless API Bleuprints
manager = APIManager(app, session=db_session)
user_rest_app = manager.create_api_blueprint(User, methods=['GET'], url_prefix='/api')
geolocation_rest_app = manager.create_api_blueprint(Geolocation, methods=['GET'], url_prefix='/api')
question_rest_app = manager.create_api_blueprint(Question, methods=['GET', 'POST', 'PUT', 'DELETE'], url_prefix='/api')
answer_rest_app = manager.create_api_blueprint(Answer, methods=['GET', 'POST', 'PUT', 'DELETE'], url_prefix='/api')


# Custom API Blueprints
#custom_api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import the Routes for the Blueprint App
#import urls

