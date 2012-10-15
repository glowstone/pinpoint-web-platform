# Environment Imports
from flask import render_template, redirect, url_for, g, session, request

# Library Imports
import datetime

# Package Modules
from web_package.models import *
from utils import *

# Package Variables
from web_package import app, db


@app.route('/')
def index():
	return render_template('index.html')

# User Resources
#######################################################
@app.route('/user/<username>', methods = ['GET'])
def user_profile(username):
	user = get_current_user()
	print user.posts
	return render_template('user_profile.html', posts=user.posts)


@app.route('/user/<id>/edit', methods = ['GET'])
def user_edit(id):
	print "User ", str(id), " attempting to edit"
	return render_template('user_edit.html')


@app.route('/user/new', methods = ['GET'])
def user_signup():
	return render_template('user_signup.html')


@app.route('/user/create', methods = ['POST'])
def user_create():
	# TODO: check if the user can be created
	create_user(request.form['username'], request.form['password'])
	return redirect(url_for('index'))


@app.route('/user/login', methods = ['POST'])
def user_login():
	username = request.form['username']
	password = request.form['password']
	if check_password(username, password):
		do_login(username)
		return redirect(url_for('user_profile', username=username))
	else:
		return "Bad login"


@app.route('/user/logout', methods = ['GET', 'POST'])
def user_logout():
	do_logout()
	return redirect(url_for('index'))


@app.route('/user/location', methods = ['GET', 'POST'])
def set_user_location():
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

		db.session.commit()
		return "set location"


# Post Resources
#######################################################
@app.route('/post/<id>', methods = ['GET'])
def post_show(id):
	post = Post.query.filter_by(id=id).first()
	return render_template('post_show.html', post=post)

@app.route('/post/<id>/edit', methods = ['GET'])
def post_edit(id):
	# TODO
	return render_template('post_edit.html')


@app.route('/post/new', methods = ['GET'])
def post_new():
	return render_template('post_new.html')


@app.route('/post/create', methods = ['POST'])
def post_create():
	user = get_current_user()
	if request.method == 'POST':
		form_names = ['title', 'body', 'tdelta']
		if not all(request.form.has_key(name) for name in form_names):
			print "Bad form. Validation error. Do something appropriate"
			return redirect(url_for('index'))
		# Copy user's location into a new geolocation object.
		user_gloc = user.geolocation
		post_gloc = create_geolocation(user_gloc.latitude, user_gloc.longitude, user_gloc.elevation)
		create_post(request.form['title'], request.form['body'], request.form['tdelta'], user, post_gloc)		
		# Need to check success status
		return redirect(url_for('post_new'))
	else:
		# Do some sort of flash
		# User not logged in
		return redirect(url_for('index'))


@app.route('/post/nearby', methods = ['GET', 'POST'])
def post_nearby():
	if request.method == 'POST':
		radius = float(request.form['radius'])
		location = get_current_user().geolocation
		posts = closest_locations(location, radius)
		return render_template('nearby_posts.html', location=location, radius=radius, posts=posts)
		
	elif request.method == 'GET':
		return render_template('nearby_posts.html')


# Geolocation Resources
###########################################################
@app.route('/location/<id>', methods = ['GET'])
def geolocation_show(id):
	geolocation = Geolocation.query.filter_by(id=id).first()
	return render_template('geolocation_show.html', geolocation=geolocation)

@app.route('/location/new', methods = ['GET'])
def geolocation_new():
	return render_template('geolocation_new.html')

@app.route('/location/create', methods = ['POST'])
def geolocation_create():
	user = get_current_user()
	return redirect(url_for('index'))

#############################################################
@app.route('/test', methods = ['GET'])
def test():
	username = session['username']
	print "All your Posts"
	user = User.query.filter_by(username=username).first()

	print user.posts
	for post in user.posts:

		print post
		print post.geolocation

	return render_template('test.html', posts=user.posts)

