from flask import render_template
from web_package import app

@app.route('/')
def hello_world():
	return render_template('index.html')


@app.route('/user/<id>')
def user_profile(id):
	return 'Viewing profile for user ' + str(id)


@app.route('/user/<id>/edit')
def edit_user(id):
	return 'Editing user: ' + str(id)


@app.route('/user/new')
def new_user_form():
	return 'This will be a form for creating a new user'


@app.route('/user/create')
def create_user():
	return 'This will handle the post request to create a user'


@app.route('/post')
def list_posts():
	return 'Lists the posts?'


@app.route('/post/<id>')
def view_post(id):
	return 'Viewing post ' + str(id)


@app.route('/post/new')
def new_post_form():
	return 'This will be a form for creating a new post'


@app.route('/post/create')
def create_post():
	return 'This will handle the post request for creating a new post'
