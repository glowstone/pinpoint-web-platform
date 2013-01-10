from flask import Blueprint

# Blueprint Applet
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import the Routes for the Blueprint App
import urls

