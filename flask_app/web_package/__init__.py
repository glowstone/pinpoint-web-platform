from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy

# Create the Flask Application
app = Flask(__name__)
# Configure the app
app.config.from_object('web_package.config')
db = SQLAlchemy(app)

# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])

# @app.before_request
# def before_request():
#     g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
#     if hasattr(g, 'db'):
#         g.db.close()

# Import routes and models at the bottom to prevent circular dependency problems.
from web_package import models
from web_package import routes