# API Interface URLs

# Package Variables
from web_package import app

# Package Modules
import api_controllers


# Pair API Routes with API Controller functions

# User Routes
###############################################################################

@app.route('/user/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def user_create_json():
	return jsonify(api_controllers.user_create_json())


@app.route('/user/verify_credentials.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def user_verify_credentials_json():
	return jsonify(api_controllers.user_verify_credentials_json())


# Posting Routes
###############################################################################

@app.route('/post/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def post_create_json():
	return jsonify(api_controllers.post_create_json())


# Just these for now