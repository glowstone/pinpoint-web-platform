from flask import Blueprint

# Blueprint Applet
api = Blueprint('API Blueprint', __name__, url_prefix='/api')

import urls

