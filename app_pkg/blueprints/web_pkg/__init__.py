from flask import Blueprint

# Blueprint Applet
web = Blueprint('web', __name__, template_folder='templates')

# Import the Routes for the Blueprint App
import urls