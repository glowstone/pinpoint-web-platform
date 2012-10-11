# Environment Imports
from flask import render_template, redirect, url_for, g, session, request
import datetime
# Package Variables
from web_package import app, db
# Package Modules
from web_package.models import *
from utils import hash_password, check_password, create_user, do_login, do_logout

@app.route('/')
def index():
	return render_template('index.html')

# User Resources
#######################################################
@app.route('/user/<username>', methods = ['GET'])
def user_profile(username):
	print "Your identifier is " + str(username)
	print session['username']
	return render_template('user_profile.html')


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
		return redirect(url_for('index'))
	else:
		return "Bad login"


@app.route('/user/logout', methods = ['GET', 'POST'])
def user_logout():
	do_logout()
	return redirect(url_for('index'))


# Post Resources
#######################################################
@app.route('/post/<id>', methods = ['GET'])
def post_show(id):
	post = Post.query.filter_by(id=id)
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
	if request.method == 'POST':
		username = session['username']

		user = User.query.filter_by(username=username).first()
		geolocation = Geolocation(42.355751, -71.099474, 40.0)
		print user
		print geolocation
		print geolocation.id


		db.session.add(geolocation)
		db.session.commit()

		found = Geolocation.query.filter_by(id=1).first()
		print found
		print found.id

		post = Post(request.form['title'], request.form['body'], \
			datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=5), \
			user.id, geolocation.id)
		
		print post

		db.session.add(post)
		db.session.commit()	

		
		# Need to check success status
		return redirect(url_for('post_new'))
	else:
		# Do some sort of flash
		return redirect(url_for('index'))


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





