# Environment Imports
from flask import render_template, redirect, url_for, g, session, request, jsonify

# Package Modules
from web_package.models import *
import api_controllers

# Package Variables
from web_package import app


# API Routes

@app.route('/user/create.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def user_create_json():
	return jsonify(api_controllers.user_create_json())

@app.route('/user/verify_credentials.json', methods=['GET', 'POST'])     #Temporarily allow GET for debug
def user_verify_credentials_json():
	return jsonify(api_controllers.user_verify_credentials_json())


# Just these for now