from flask import Flask

#App configuration will go here.

app = Flask(__name__)


# To prevent circular dependency problems, import views at the end and do not use the views inside __init__.py.
import flask_app.views