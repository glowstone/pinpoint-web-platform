# Environment Imports
from flask import render_template, redirect, url_for, g, session, request

# Library Imports
import datetime

# Package Modules
from web_package.models import *
#from utils import *
import controllers

# Package Variables
from web_package import app
from web_package.database import db_session


# Before Request / Teardown may access the db_session directly
@app.before_request
def before_request():
	pass

@app.teardown_request
def teardown_request(exception):
	db_session.remove()                    #Shutdown SQLAlchemy db session.


# URL Routes (Pair URL Routes with Controller Functions)

@app.route('/')
def index():
	"""Show the web interface home page"""
	return controllers.index()


@app.route('/user/signup', methods = ['GET', 'POST'])
def user_new():
	"""New user creation"""
	return controllers.user_new()

@app.route('/user/login', methods = ['POST'])
def user_login():
	"""Log the user in"""
	return controllers.user_login()


@app.route('/user/logout', methods = ['GET', 'POST'])
def user_logout():
	"""Log the user out"""
	return controllers.user_logout()


@app.route('/user/<username>', methods = ['GET'])
def user_view(username):
	"""View user profile"""
	return controllers.user_view(username)


@app.route('/user/<id>/settings', methods = ['GET'])
def user_edit(id):
	"""Edit user settings"""
	return controllers.user_edit()

# Temporary
@app.route('/user/location', methods = ['GET', 'POST'])
def user_location():
	"""Temporary page for setting a user's location"""
	return controllers.user_location()

# Posting Resources - Temporary 
#######################################################

@app.route('/posting/new', methods = ['GET'])
def posting_new():
	"""Route showing form to create a new Posting"""
	return controllers.posting_new()

# Temporary
@app.route('/posting/new2', methods = ['POST'])
def posting_new2():
	"""Checks posting form submission and redirects as appropriate"""
	return controllers.posting_new2()


@app.route('/posting/<id>', methods = ['GET'])
def posting_view(id):
	"""Show the posting with id"""
	return controllers.posting_view(id)
	

@app.route('/posting/<id>/edit', methods = ['GET'])
def posting_edit(id):
	"""Allow editing the posting with id"""
	return controllers.posting_edit(id)

# Temporary - to be moved to API
@app.route('/posting/nearby', methods=['GET', 'POST'])
def posting_nearby():
	"""Demonstration of ability to query for nearby posts"""
	return controllers.posting_nearby()




# # Geolocation Resources
# ###########################################################
# @app.route('/location/<id>', methods = ['GET'])
# def geolocation_show(id):
# 	geolocation = Geolocation.query.filter_by(id=id).first()
# 	return render_template('geolocation_show.html', geolocation=geolocation)

# @app.route('/location/new', methods = ['GET'])
# def geolocation_new():
# 	return render_template('geolocation_new.html')

# @app.route('/location/create', methods = ['POST'])
# def geolocation_create():
# 	user = get_current_user()
# 	return redirect(url_for('index'))

# #############################################################
# @app.route('/test', methods = ['GET'])
# def test():
# 	username = session['username']
# 	print "All your Posts"
# 	user = User.query.filter_by(username=username).first()

# 	print user.posts
# 	for post in user.posts:

# 		print post
# 		print post.geolocation

# 	return render_template('test.html', posts=user.posts)

