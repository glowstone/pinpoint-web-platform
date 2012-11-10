# API Interface URLs
from flask import jsonify, redirect, abort
import json

# Package Variables
from web_package import app

# Package Modules
import api_controllers

import util


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
	return jsonify(api_controllers.user_current_json())


@app.route('/api/user/set_location.json', methods=['GET'])         #Temporarily allow GET for debug
def user_set_location():
	return jsonify(api_controllers.user_set_geolocation_json())


# Question Routes
###############################################################################

@app.route('/api/question/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def question_create_json():
	return jsonify(api_controllers.question_create_json())


@app.route('/api/question/list.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def question_list_json():
	required_arguments = []
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		question_list = api_controllers.question_list_json(**arguments)
		return jsonify(question_list = [question.serialize() for question in question_list])
	else:
		abort(402)    # TODO change to whatever bad argument error number is 


@app.route('/api/question/get.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def question_view_json():
	required_arguments = ['id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		question = api_controllers.question_get_json(**arguments)
		return jsonify(question = question.serialize())
	else:
		abort(402)



# Answer Routes
###############################################################################

@app.route('/api/answer/create.json', methods=['GET', 'POST'])        #Temporarily allow GET for debug
def answer_create_json():
	return jsonify(api_controllers.answer_create_json())

@app.route('/api/answer/list.json', methods=['GET', 'POST'])
def answer_list_json():
	required_arguments = ['question_id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		answer_list = api_controllers.answer_list_json(**arguments)
		return jsonify(answer_list = [answer.serialize() for answer in answer_list])
	else:
		abort(402)


@app.route('/api/answer/get.json', methods=['GET', 'POST'])
def answer_get_json():
	required_arguments = ['id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		answer = api_controllers.answer_get_json(**arguments)
		return jsonify(answer = answer.serialize())
	else:
		abort(402)   # TODO change to whatever the bad argument error number is
	

# Comment Routes
###############################################################################
@app.route('/api/comment/create.json', methods=['GET', 'POST'])       # Temporarily allow GET
def comment_create_json():
	return jsonify(api_controllers.comment_create_json())



