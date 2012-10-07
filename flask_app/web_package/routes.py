# Environment Imports
from flask import render_template, redirect, url_for, g, session, request
import datetime
# Package Variables
from web_package import app, db
# Package Modules
from web_package.models import *
from utils import hash_password

@app.route('/')
def index():
	return render_template('index.html')


# User Resources
#######################################################
@app.route('/user/<id>', methods = ['GET'])
def user_profile(id):
	print "Your identifier is " + str(id)
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
	#Create a new user
	hash, salt = hash_password(request.form['password'])
	user = User(request.form['username'], hash, salt)
	session['username'] = request.form['username']
	db.session.add(user)
	db.session.commit()
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
		user = User.query.filter_by(username=username)
		
		# TODO: Clean this ugliness
		post = Post(request.form['title'], request.form['body'], datetime.datetime.now(), \
			datetime.datetime.now() + 1111, datetime.datetime.now(), user.id)
		print post
		db.session.add(post)
		db.session.commit()		
		# Need to check success status
		return redirect(url_for('post_new'))
	else:
		# Do some sort of flash
		return redirect(url_for('index'))




