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