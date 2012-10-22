from flask import render_template, redirect, url_for, session, request


from utils import *

def index():
	return "Index page"


# User Controller Handlers

def user_view():
	user = get_current_user()
	if user:
		return render_template('user_profile.html', posts=user.posts)
	else:
		return redirect(url_for('user_login'))	

def user_edit(id):
	#TODO
	print "User ", str(id), " attempting to edit"
	return render_template('user_edit.html')

@app.route('/user/new', methods = ['GET'])
def user_signup():
	return render_template('user_signup.html')

def user_create():
	# TODO: check if the user can be created
	print request.form['username']
	create_user(request.form['username'], request.form['password'])
	return redirect(url_for('index'))

def user_login():
	username = request.form['username']
	password = request.form['password']
	if check_password(username, password):
		do_login(username)
		return redirect(url_for('user_profile', username=username))
	else:
		return "Bad login"

def user_logout():
	do_logout()
	return redirect(url_for('index'))


# @app.route('/user/location', methods = ['GET', 'POST'])
# def set_user_location():
# 	user = get_current_user()
# 	if request.method == 'GET':
# 		return render_template('user_location.html')
# 	elif request.method == 'POST':
# 		lat = request.form['latitude']
# 		lng = request.form['longitude']
# 		elev = request.form['elevation']

# 		user = get_current_user()

# 		geolocation = user.geolocation
# 		geolocation.latitude = lat
# 		geolocation.longitude = lng
# 		geolocation.elevation = elev

# 		db.session.commit()
# 		return "set location"




# Post Controller Handlers