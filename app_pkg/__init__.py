from flask import Flask

# Create the Flask Application
app = Flask(__name__)

# Configure the app with default settings 
app.config.from_object('app_pkg.config.default')
# Override default settings with values from environment-pointed-to config file.
app.config.from_envvar('APP_CONFIG_FILE')


# Default Request Before / Teardown Behavior 
from app_pkg.database import db_session

@app.before_request
def before_request():
	pass

@app.teardown_request
def teardown_request(exception):
	db_session.remove()                    #Shutdown SQLAlchemy db session.


# Import urls at the bottom to prevent cyclic dependencies
from app_pkg import urls
from app_pkg import api_urls