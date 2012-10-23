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


@app.route('/user/signup', methods = ['GET'])
def user_new():
	"""Signup form for creating a new user"""
	return controllers.user_new()


@app.route('/user/create', methods = ['POST'])
def user_create():
	"""Create a new user from POSTed form"""
	return controllers.create_user_from_form()


@app.route('/user/login', methods = ['POST'])
def user_login():
	"""Log the user in"""
	return controllers.login()


@app.route('/user/logout', methods = ['GET', 'POST'])
def user_logout():
	"""Log the user out"""
	return controllers.logout()


@app.route('/user/<username>', methods = ['GET'])
def user_view(username):
	"""View user profile"""
	return controllers.user_view()


@app.route('/user/<id>/settings', methods = ['GET'])
def user_edit(id):
	"""Edit user settings"""
	return controllers.user_edit()



@app.route('/user/location', methods = ['GET', 'POST'])
def set_user_location():
	"""Temporary page for setting a user's location"""
	pass

# Post Resources
#######################################################
@app.route('/post/<id>', methods = ['GET'])
def post_show(id):
	pass
	#post = Post.query.filter_by(id=id).first()
	#return render_template('post_show.html', post=post)

@app.route('/post/<id>/edit', methods = ['GET'])
def post_edit(id):
	# TODO
	#return render_template('post_edit.html')
	pass

@app.route('/post/new', methods = ['GET'])
def post_new():
	pass
	#return render_template('post_new.html')


@app.route('/post/create', methods = ['POST'])
def post_create():
	# user = get_current_user()
	# if request.method == 'POST':
	# 	form_names = ['title', 'body', 'tdelta']
	# 	if not all(request.form.has_key(name) for name in form_names):
	# 		print "Bad form. Validation error. Do something appropriate"
	# 		return redirect(url_for('index'))
	# 	# Copy user's location into a new geolocation object.
	# 	user_gloc = user.geolocation
	# 	post_gloc = create_geolocation(user_gloc.latitude, user_gloc.longitude, user_gloc.elevation)
	# 	create_post(request.form['title'], request.form['body'], request.form['tdelta'], user, post_gloc)		
	# 	# Need to check success status
	# 	return redirect(url_for('post_new'))
	# else:
	# 	# Do some sort of flash
	# 	# User not logged in
	# 	return redirect(url_for('index'))
	pass


# @app.route('/post/nearby', methods = ['GET', 'POST'])
# @login_required
# def post_nearby():
# 	pass
	# if request.method == 'POST':
	# 	radius = float(request.form['radius'])
	# 	location = get_current_user().geolocation
	# 	posts = closest_posts(location, radius)
	# 	return render_template('nearby_posts.html', location=location, radius=radius, posts=posts)
		
	# elif request.method == 'GET':
	# 	return render_template('nearby_posts.html')

@app.route('/post/nearby', methods=['GET', 'POST'])
def post_nearby():
	pass


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

