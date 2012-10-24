from flask import render_template, redirect, url_for, session, request, flash
import util
from models import *
#from web_package import db_session
import api_controllers as api


def index():
	return render_template('index.html')

# User Controller Handlers
###############################################################################

def user_new():
	"""On GET, show form to create a new User and on POST create the new User"""
	if request.method == 'GET':
		return render_template('user_new.html')
	else:
		api_response = api.user_create_json()
		if api_response.get('success', False):
			return redirect(url_for('user_view', username = session.get('username', None)))
		else:
			# TODO show validation errors
			flash("Bad User creation request")
			return redirect(url_for('user_new'))
		
def user_login():
	"""Make API request to log the user in and redirect to the profile page"""
	api_response = api.user_verify_credentials_json()
	if api_response.get('success', False):
		return redirect(url_for('user_view', username = session.get('username', None)))
	else:
		flash("Invalid login")
		return redirect(url_for('index'))

def user_logout():
	"""Remove the session username"""
	session.pop('username', None)
	return redirect(url_for('index'))

def user_view(username):
	"""Show the current user's profle or redirect to the page with user login"""
	user = util.get_current_user()
	if user:
		return render_template('user_view.html', user=user)
	else:
		flash("You're not logged in")
		return redirect(url_for('index'))	

def user_edit(id):
	return render_template('user_edit.html')

# Temporary
def user_location():
	user = util.get_current_user()
	if request.method == 'GET':
		return render_template('user_location.html')
	elif request.method == 'POST':
		lat = request.form['latitude']
		lng = request.form['longitude']
		elev = request.form['elevation']

		geolocation = user.geolocation
		geolocation.latitude = lat
		geolocation.longitude = lng
		geolocation.elevation = elev

		db_session.commit()
		return "set location"

# Posting Controller Handlers
###############################################################################

def posting_new():
	"""On GET show form to create Posting or on POST create new Posting"""
	if request.method == 'GET':
		return render_template('posting_new.html')
	else:
		api_response = api.posting_create_json()
		if api_response.get('success', False):
			return redirect(url_for('user_view', username = session.get('username', None)))
		else:
			# TODO show validation errors
			flash("Bad Posting creation request")
			return redirect(url_for('posting_new'))

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

