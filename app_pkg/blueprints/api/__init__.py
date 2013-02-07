from flask import Blueprint         # For creation of custom Blueprints

from app_pkg.blueprints.api.controllers import user_rest_app, geolocation_rest_app, question_rest_app, answer_rest_app

# Custom API Blueprints
#custom_api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import the Routes for the Blueprint App
#import urls

