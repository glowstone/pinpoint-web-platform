from flask.ext.restless import APIManager

from app_pkg import app
from app_pkg.database import db_session
from app_pkg.blueprints.api.models import User, Question #Geolocation, Answer


manager = APIManager(app, session=db_session)

user_rest_app = manager.create_api_blueprint(User)
question_rest_app = manager.create_api_blueprint(Question)
