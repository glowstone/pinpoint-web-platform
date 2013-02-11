from flask import jsonify, redirect, abort, request, Response
# Provides an API call for session authentication.
from flask import session
from app_pkg.blueprints.api import custom_api_bp as api

import json

# Package Modules
import custom

import util

# Custom API Routes
###############################################################################

@api.route('/user_create', methods=['GET', 'POST'])     # GET for testing only
def user_create_wrapper():
	"""
	Wrapper around the custom API user_create method.
	Expects 'username', 'email', and 'password' feilds to be POSTed.
	Returns a JSON representation of the custom API success or error response.
	Affects: Attempts to create a new User, setup his/her profile image.
	"""
	required_arguments = ['username', 'email', 'password']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = custom.user_create(**arguments)
		return jsonify(api_response=api_response)
	else:
		return abort(400)     # Bad Request


@api.route('/user_authenticate', methods=['GET', 'POST'])    # GEt for testing only
def user_authenticate_wrapper():
	"""
	Wrapper around the custom API user_authenticate method.
	Expects 'user_identifier'(username or email) and 'password' fields to be POSTed
	Note: POSTed not because they modify server data, but so that arguments (plaintext
	password) do not appear in any client visible representations.
	Returns a JSON representation of the custom API success or error response.
	"""
	required_arguments = ['user_identifier', 'password']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = custom.user_authenticate(**arguments)
		if api_response.get('success', False):
			# data field will contain a User object
			user = api_response.get('data')
			session['user'] = user       # Log in the authenticated user
			# Serialize the User object before sending to API client.
			api_response['data'] = api_response.get('data').serialize()
			return jsonify(api_response)
		else:
			return jsonify(api_response)
	else:
		return abort(400)        # Bad Request


@api.route('/user_show', methods=['GET'])
def user_show_wrapper():
	"""
	Wrapper around the custom API user_show method.
	Expects 'username' field to be passed via GET
	Returns a JSON representation of the custom API success or error response.
	"""
	required_arguments = ['username']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = custom.user_show(**arguments)
		if api_response.get('success', False):
			# data field will contain a User object
			api_response['data'] = api_response.get('data').serialize()
			return jsonify(api_response)
		else:
			return jsonify(api_response)
	else:
		return abort(400)      # Bad Request





# Pair API Routes with API Controller functions

# User Routes
###############################################################################

# @api.route('/user/create.json', methods=['POST'])     
# def user_create_json():
# 	required_arguments = ['username', 'email', 'password']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if arguments:
# 		status = api_controllers.user_create_json(**arguments)
# 		return jsonify(status=status)
# 	else:
# 		return abort(402)     # Bad argument


# @api.route('/user/verify_credentials.json', methods=['POST'])
# def user_verify_credentials_json():
# 	required_arguments = ['username', 'password']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if arguments:
# 		status = api_controllers.user_verify_credentials_json(**arguments)
# 		return jsonify(status=status)
# 	else:
# 		return abort(402)


# @api.route('/user/show.json', methods=['GET'])
# def user_show_json():
# 	required_arguments = ['username']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if arguments:
# 		api_response = api_controllers.user_show_json(**arguments)
# 		return jsonify(api_response = api_response)
# 	else:
# 		return abort(402)


# @api.route('/user/set_location.json', methods=['GET', 'PUT'])      #Temporarily allow GET for debug
# def user_set_location():
# 	required_arguments = ['latitude', 'longitude']
# 	arguments = util.unpack_arguments(required_arguments)
# 	print arguments
# 	if not arguments == None:
# 		status = api_controllers.user_set_geolocation_json(**arguments)
# 		return jsonify(status=status)
# 	else:
# 		return abort(402)


# # Question Resources
# ###############################################################################

# @api.route('/question/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
# def question_create_json():
# 	return jsonify(api_controllers.question_create_json())


# @api.route('/questions', methods=['GET'])     #Temporarily allow GET for debug
# def questions_wrapper():
# 	required_arguments = []
# 	print request
# 	print request.args
# 	print request.values

# 	result = controllers.questions()
# 	print "jsonified result"
# 	answer = json.dumps(result)
# 	print answer
# 	resp = Response(response=answer, status=200, mimetype="application/json")
# 	print resp
# 	return resp


	



# 	# arguments = util.unpack_arguments(required_arguments)
# 	# if not arguments == None:
# 	# 	question_list = api_controllers.question_list_json(**arguments)
# 	# 	return jsonify(question_list = [question.serialize() for question in question_list])
# 	# else:
# 	# 	abort(402)    # TODO change to whatever bad argument error number is 
# 	return "things"

# @api.route('/question/get.json', methods=['GET'])
# def question_get_json():
# 	required_arguments = ['question_id']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if not arguments == None:
# 		question = api_controllers.question_get_json(**arguments)
# 		return jsonify(question = question.serialize())
# 	else:
# 		abort(402)



# # Answer Routes
# ###############################################################################

# @api.route('/answer/create.json', methods=['GET', 'POST'])        #Temporarily allow GET for debug
# def answer_create_json():
# 	return jsonify(api_controllers.answer_create_json())

# @api.route('/answer/list.json', methods=['GET'])
# def answer_list_json():
# 	required_arguments = ['question_id']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if not arguments == None:
# 		answer_list = api_controllers.answer_list_json(**arguments)
# 		return jsonify(answer_list = [answer.serialize() for answer in answer_list])
# 	else:
# 		abort(402)


# @api.route('/answer/get.json', methods=['GET'])
# def answer_get_json():
# 	required_arguments = ['answer_id']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if not arguments == None:
# 		answer = api_controllers.answer_get_json(**arguments)
# 		return jsonify(answer = answer.serialize())
# 	else:
# 		abort(402)   # TODO change to whatever the bad argument error number is
	

# # Comment Routes
# ###############################################################################
# @api.route('/comment/create.json', methods=['GET', 'POST'])       # Temporarily allow GET
# def comment_create_json():
# 	return jsonify(api_controllers.comment_create_json())


# @api.route('/comment/list.json', methods=['GET'])
# def comment_list_json():
# 	required_arguments = ['commentable_id']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if not arguments == None:
# 		comment_list = api_controllers.comment_list_json(**arguments)
# 		return jsonify(comment_list = [comment.serialize() for comment in comment_list])
# 	else:
# 		abort(402)


# @api.route('/comment/get.json', methods=['GET'])
# def comment_get_json():
# 	required_arguments = ['comment_id']
# 	arguments = util.unpack_arguments(required_arguments)
# 	if not arguments == None:
# 		comment = api_controllers.comment_get_json(**arguments)
# 		return jsonify(comment = comment.serialize())
# 	else:
# 		abort(402)   # TODO change to whatever the bad argument error number is



