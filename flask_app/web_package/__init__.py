from flask import Flask

# Create the Flask Application
app = Flask(__name__)


# Configure the app
# First load configuration from 
app.config.from_object('web_package.config.dev_config')
# Override configuration with values within the file pointed to in Deployment Environment
app.config.from_envvar('DEPLOYMENT_CONFIG', silent=True)

from web_package.database import db_session


# Default Request Before / Teardown Behavior 
@app.before_request
def before_request():
	pass

@app.teardown_request
def teardown_request(exception):
	db_session.remove()                    #Shutdown SQLAlchemy db session.


# Import urls at the bottom to prevent cyclic dependencies
from web_package import urls
from web_package import api_urls