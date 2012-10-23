from flask import render_template, redirect, url_for, session, request, flash
from utils import *
from models import *
from web_package import db_session


def index():
	return render_template('index.html')

# User Controller Handlers

def user_new():
	"""Render the template showing the form to create a User"""
	return render_template('user_new.html')

# Temporary - will move to API eventually
def user_new2():
	"""Create User from the POSTed form"""
	# TODO: check if the user can be created
	username = request.form['username']
	password = request.form['password']
	#Check the form fields
	# Validate the form
	user = create_user(username, password)       #Make sure this returns None on failure
	print user
	if user:
		return redirect(url_for('user_view', username = user.username))
	else:
		#Flash bad login
		return redirect(url_for('index'))
		
def create_user(username, password):
	location = Geolocation(0, 0, 0)
	db_session.add(location)
	db_session.commit()
	# Hash the password provided in the new user form. Store the hashed value and the salt used in the hash.
	hash, salt = hash_password(password)
	user = User(username, hash, salt, location.id)
	# Insert the user object into the database
	db_session.add(user)
	db_session.commit()
	# Set the session information for the new user
	session['username'] = username
	return user

def user_login():
	username = request.form['username']
	password = request.form['password']
	if check_password(username, password):
		session['username'] = username
		return redirect(url_for('user_view', username = username))
	else:
		return "Bad login"

def user_logout():
	session.pop('username', None)
	return redirect(url_for('index'))

def user_view(username):
	"""Show the current user's profle or redirect to the page with user login"""
	user = get_current_user()
	if user:
		return render_template('user_view.html', user=user)
	else:
		flash("You're not logged in")
		return redirect(url_for('index'))	

def user_edit(id):
	return render_template('user_edit.html')

# Temporary
def user_location():
	user = get_current_user()
	if request.method == 'GET':
		return render_template('user_location.html')
	elif request.method == 'POST':
		lat = request.form['latitude']
		lng = request.form['longitude']
		elev = request.form['elevation']

		user = get_current_user()

		geolocation = user.geolocation
		geolocation.latitude = lat
		geolocation.longitude = lng
		geolocation.elevation = elev

		db_session.commit()
		return "set location"

# Post Controller Handlers

def posting_new():
	return render_template('posting_new.html')

def posting_new2():
	user = get_current_user()
	print user
	if request.method == 'POST':
		form_names = ['title', 'body', 'tdelta']
		if not all(request.form.has_key(name) for name in form_names):
			print "Bad form. Validation error. Do something appropriate"
			return redirect(url_for('index'))
		# Copy user's location into a new geolocation object.
		user_gloc = user.geolocation
		post_gloc = Geolocation(user_gloc.latitude, user_gloc.longitude, user_gloc.elevation)
		db_session.add(post_gloc)
		db_session.commit()
		post = Posting(user, post_gloc)		
		# Need to check success status
		db_session.add(post)
		db_session.commit()
		return redirect(url_for('posting_new'))
	else:
		flash("Failed to create Posting")
		return redirect(url_for('index'))

def posting_view(id):
	# TODO: Check whether user has permission to view the post
	# Current permission model - all public, but don't show authors if not authenticated.
	post = Post.query.filter_by(id=id).first()
	return render_template('posting_view.html', post=post)


def posting_edit(id):
	# TODO populate form apprpriately and check permissions
	return render_template('posting_edit.html')

# Temporary - will be moved to API
def posting_nearby():
	if request.method == 'POST':
		radius = float(request.form['radius'])
		location = get_current_user().geolocation
		posts = closest_posts(location, radius)
		return render_template('nearby_posts.html', location=location, radius=radius, posts=posts)
		
	elif request.method == 'GET':
		return render_template('nearby_posts.html')


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

