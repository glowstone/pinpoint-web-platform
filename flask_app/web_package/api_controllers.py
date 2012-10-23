from flask import render_template, redirect, url_for, session, request, flash, jsonify
from utils import *
from models import *
from web_package import db_session
import json


# API Account Resource Handlers

def user_create_json():
	"""Create a User from a web form or from Android"""
	response = {}

	# Right now assumes parameters passed as a form. Need to generalize
	form_names = ['username', 'password', 'password_repeat']
	# TODO - write a better functional style utility that returns which names are missing too.
	if not all(request.form.has_key(name) for name in form_names):
		return jsonify(error_response("Temp message about needing correct names"))   #TODO Generalize spec
	
	username = request.form['username']
	password = request.form['password']
	password_retry = request.form['password_repeat']

	# TODO real validation - return errors in json
	
	# TODO take optional latitude, longitude, elevation starting values
	location = Geolocation(0, 0, 0)
	db_session.add(location)
	db_session.commit()                          # Atomicity is somewhat desired here. TODO
	hash, salt = hash_password(password)
	user = User(username, hash, salt, location)
	db_session.add(user)
	db_session.commit()
	# Set the session information for the new user

	# Can Android store cookies?
	session['username'] = username

	response['success'] = True
	response['username'] = username
	return response


def user_verify_credentials_json():
	response = {}
	return {"success": False, "username": None, "error": "Implementation in progress"}

	
	
def error_response(message):
	return {'success': False, \
			'error': message}







