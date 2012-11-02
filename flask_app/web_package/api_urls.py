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


@app.route('/api/user/set_location.json', methods=['GET'])         #Temporarily allow GET for debug
def user_set_location():
	return jsonify(api_controllers.user_set_controllers())


# Posting Routes
###############################################################################

@app.route('/api/post/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def post_create_json():
	return jsonify(api_controllers.post_create_json())



# Question Routes
###############################################################################

@app.route('/api/question/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def question_create_json():
	return jsonify(api_controllers.question_create_json())


@app.route('/api/question/list.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def question_list_json():
	return jsonify(api_controllers.question_list_json())


@app.route('/api/question/view.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def question_view_json():
	return jsonify(api_controllers.question_view_json())



# Answer Routes
###############################################################################

@app.route('/api/answer/create.json', methods=['GET', 'POST'])        #Temporarily allow GET for debug
def answer_create_json():
	return jsonify(api_controllers.answer_create_json())


# Comment Routes
###############################################################################
@app.route('/api/comment/create.json', methods=['GET', 'POST'])       # Temporarily allow GET
def comment_create_json():
	return jsonify(api_controllers.comment_create_json())