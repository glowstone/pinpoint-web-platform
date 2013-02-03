from flask import Flask
import os

# Create the Flask Application
app = Flask(__name__)

# Configure the app with default settings 
app.config.from_object('app_pkg.config.default')
# Override default settings with values from environment-pointed-to config file.
app_config = os.environ['APP_CONFIG']
if app_config == 'development':
	app.config.from_object('app_pkg.config.development')
elif app_config == 'production':
	app.config.from_object('app_pkg.config.production')


# Default Request Before / Teardown Behavior 
from app_pkg.database import db_session

@app.before_request
def before_request():
	pass

@app.teardown_request
def teardown_request(exception):
	db_session.remove()                    #Shutdown SQLAlchemy db session.


# Custom Context Processors
from app_pkg.blueprints.web.context_processors import external_keys
from app_pkg.blueprints.web.context_processors import server_info


# Import Blueprint Apps
from app_pkg.blueprints.web import web_bp

# REST API Blueprints
from app_pkg.blueprints.api import user_rest_app
from app_pkg.blueprints.api import geolocation_rest_app
from app_pkg.blueprints.api import question_rest_app
from app_pkg.blueprints.api import answer_rest_app

# Register the Blueprint Apps
app.register_blueprint(web_bp)
app.register_blueprint(user_rest_app)
app.register_blueprint(geolocation_rest_app)
app.register_blueprint(question_rest_app)
app.register_blueprint(answer_rest_app)






