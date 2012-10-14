from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Create the Flask Application
app = Flask(__name__)
# Configure the app
# First load configuration from 
app.config.from_object('web_package.config.dev_config')
# Override configuration with values within the file pointed to in Deployment Environment
app.config.from_envvar('DEPLOYMENT_CONFIG', silent=True)

# Setup the SQLAlchemy db object
db = SQLAlchemy(app)




# Import routes and models at the bottom to prevent circular dependency problems.
from web_package import models
from web_package import routes