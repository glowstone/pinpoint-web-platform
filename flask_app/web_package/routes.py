from flask import render_template, redirect, url_for, g, session, request
from web_package import app
from web_package import user

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
	print "Created user. TODO: Set session user"
	user.User.create(request.form['username'], request.form['password'])
	return redirect(url_for('index'))


# Post Resources
#######################################################



