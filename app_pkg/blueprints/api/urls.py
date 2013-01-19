from flask import jsonify, redirect, abort, request, Response
from app_pkg.blueprints.api import api_bp as api

import json

# Package Modules
import controllers

import util


# Pair API Routes with API Controller functions

# User Routes
###############################################################################

@api.route('/user/create.json', methods=['POST'])     
def user_create_json():
	required_arguments = ['username', 'email', 'password']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		status = api_controllers.user_create_json(**arguments)
		return jsonify(status=status)
	else:
		return abort(402)     # Bad argument


@api.route('/user/verify_credentials.json', methods=['POST'])
def user_verify_credentials_json():
	required_arguments = ['username', 'password']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		status = api_controllers.user_verify_credentials_json(**arguments)
		return jsonify(status=status)
	else:
		return abort(402)


@api.route('/user/show.json', methods=['GET'])
def user_show_json():
	required_arguments = ['username']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = api_controllers.user_show_json(**arguments)
		return jsonify(api_response = api_response)
	else:
		return abort(402)


@api.route('/user/set_location.json', methods=['GET', 'PUT'])      #Temporarily allow GET for debug
def user_set_location():
	required_arguments = ['latitude', 'longitude']
	arguments = util.unpack_arguments(required_arguments)
	print arguments
	if not arguments == None:
		status = api_controllers.user_set_geolocation_json(**arguments)
		return jsonify(status=status)
	else:
		return abort(402)


# Question Resources
###############################################################################

@api.route('/question/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def question_create_json():
	return jsonify(api_controllers.question_create_json())


@api.route('/questions', methods=['GET'])     #Temporarily allow GET for debug
def questions_wrapper():
	required_arguments = []
	print request
	print request.args
	print request.values

	result = controllers.questions()
	print "jsonified result"
	answer = json.dumps(result)
	print answer
	resp = Response(response=answer, status=200, mimetype="application/json")
	print resp
	return resp


	



	# arguments = util.unpack_arguments(required_arguments)
	# if not arguments == None:
	# 	question_list = api_controllers.question_list_json(**arguments)
	# 	return jsonify(question_list = [question.serialize() for question in question_list])
	# else:
	# 	abort(402)    # TODO change to whatever bad argument error number is 
	return "things"

@api.route('/question/get.json', methods=['GET'])
def question_get_json():
	required_arguments = ['question_id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		question = api_controllers.question_get_json(**arguments)
		return jsonify(question = question.serialize())
	else:
		abort(402)



# Answer Routes
###############################################################################

@api.route('/answer/create.json', methods=['GET', 'POST'])        #Temporarily allow GET for debug
def answer_create_json():
	return jsonify(api_controllers.answer_create_json())

@api.route('/answer/list.json', methods=['GET'])
def answer_list_json():
	required_arguments = ['question_id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		answer_list = api_controllers.answer_list_json(**arguments)
		return jsonify(answer_list = [answer.serialize() for answer in answer_list])
	else:
		abort(402)


@api.route('/answer/get.json', methods=['GET'])
def answer_get_json():
	required_arguments = ['answer_id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		answer = api_controllers.answer_get_json(**arguments)
		return jsonify(answer = answer.serialize())
	else:
		abort(402)   # TODO change to whatever the bad argument error number is
	

# Comment Routes
###############################################################################
@api.route('/comment/create.json', methods=['GET', 'POST'])       # Temporarily allow GET
def comment_create_json():
	return jsonify(api_controllers.comment_create_json())


@api.route('/comment/list.json', methods=['GET'])
def comment_list_json():
	required_arguments = ['commentable_id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		comment_list = api_controllers.comment_list_json(**arguments)
		return jsonify(comment_list = [comment.serialize() for comment in comment_list])
	else:
		abort(402)


@api.route('/comment/get.json', methods=['GET'])
def comment_get_json():
	required_arguments = ['comment_id']
	arguments = util.unpack_arguments(required_arguments)
	if not arguments == None:
		comment = api_controllers.comment_get_json(**arguments)
		return jsonify(comment = comment.serialize())
	else:
		abort(402)   # TODO change to whatever the bad argument error number is



