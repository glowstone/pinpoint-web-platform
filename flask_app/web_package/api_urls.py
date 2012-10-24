# API Interface URLs
from flask import jsonify, redirect

# Package Variables
from web_package import app

# Package Modules
import api_controllers


# Pair API Routes with API Controller functions

# User Routes
###############################################################################

@app.route('/api/user/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def user_create_json():
	return jsonify(api_controllers.user_create_json())


@app.route('/api/user/verify_credentials.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def user_verify_credentials_json():
	return jsonify(api_controllers.user_verify_credentials_json())


@app.route('/api/user/current.json', methods=['GET'])
def user_current():
	return jsonify(api_controllers.user_current())	



# Posting Routes
###############################################################################

@app.route('/post/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def post_create_json():
	return jsonify(api_controllers.post_create_json())


# Just these for now