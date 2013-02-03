from flask.ext.restless import APIManager

from app_pkg import app
from app_pkg.database import db_session
from app_pkg.blueprints.api.models import Moduser, Profile


manager = APIManager(app, session=db_session)

moduser_rest_app = manager.create_api_blueprint(Moduser)
profile_rest_app = manager.create_api_blueprint(Profile)