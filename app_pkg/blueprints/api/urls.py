from flask import jsonify, redirect, abort, request, Response
# Provides an API call for session authentication.
from flask import session
from app_pkg.blueprints.api import custom_api_bp as api
from app_pkg.blueprints.api.util import login_required

import json

# Package Modules
import custom

import util

# Custom API Routes
###############################################################################

@api.route('/user_create', methods=['POST'])
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
		return abort(400)     # Bad Request


@api.route('/user_authenticate', methods=['POST'])
def user_authenticate_wrapper():
	"""
	Wrapper around the custom API user_authenticate method.
	Expects 'user_identifier'(username or email) and 'password' fields to be POSTed
	Note: POSTed not because they modify server data, but so that arguments (plaintext
	password) do not appear in any client visible representations.
	Returns a JSON representation of the custom API success response containing
	the serialized version of the authenticated Usser, or the custom API error response.
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
@login_required
def user_show_wrapper():
	"""
	Wrapper around the custom API user_show method.
	Expects 'username' field to be passed via GET
	Returns a JSON representation of the custom API success containing the
	serialized version fo the authenticated User, or the custom API error response.
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

# Custom API Calls for the Android Client
###############################################################################

@api.route('/user_put_latlong', methods=['POST'])
@login_required
def user_put_latlong():
	"""
	Wrapper around the custom API user_put_latlong method.
	Expects 'latitude' and 'longitude' fields to be passed via POST.
	Returns a JSON representation of the custom API success containing the 
	serialized version of the authenticated User, of the custom API error response.
	"""
	print "Got here"
	required_arguments = ['latitude', 'longitude']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = custom.user_put_latlong(**arguments)
		if api_response.get('success', False):
			# data field will contain a User object
			api_response['data'] = api_response.get('data').serialize()
			return jsonify(api_response)
		else:
			return jsonify(api_response)
	else:
		return abort(400)      # Bad Request


@api.route('/user_register_gcm', methods=['POST'])
@login_required
def user_register_gcm_wrapper():
	"""
	Wrapper around the custom API user_register_gcm method.
	Expects 'registration_id' field to be passed via POST.
	Returns a JSON representation of the custom API success containing the 
	serialized version of the authenticated User, of the custom API error response.
	"""
	required_arguments = ['registration_id']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = custom.user_register_gcm(**arguments)
		if api_response.get('success', False):
			# data field will contain a User object
			api_response['data'] = api_response.get('data').serialize()
			return jsonify(api_response)
		else:
			return jsonify(api_response)
	else:
		return abort(400)      # Bad Request


@api.route('/question_create', methods=['POST'])
@login_required
def question_create_wrapper():
	"""
	Wrapper around the custom API question_create method.
	Expects 'title', 'text', 'latitude', 'longitude' fields to be POSTed.
	Returns a JSON representation of the custom API success or error response.
	"""
	required_arguments = ['title', 'text', 'latitude', 'longitude']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = custom.question_create(**arguments)
		if api_response.get('success', False):
			return jsonify(api_response)
		else:
			return jsonify(api_response)
	else:
		return abort(400)     # Bad Request

@api.route('/answer_create', methods=['GET', 'POST'])
@login_required
def answer_create_wrapper():
	"""
	Wrapper around the custom API answer_create method.
	Expects 'text', 'latitude', 'longitude', and 'question_id' fields to be POSTed.
	Returns a JSON representation of the custom API success or error response.
	"""
	required_arguments = ['text', 'latitude', 'longitude', 'question_id']
	arguments = util.unpack_arguments(required_arguments)
	if arguments:
		api_response = custom.answer_create(**arguments)
		if api_response.get('success', False):
			return jsonify(api_response)
		else:
			return jsonify(api_response)
	else:
		return abort(400)     # Bad Request


