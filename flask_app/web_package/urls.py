# Web Interface URLs

# Package Variables
from web_package import app

# Package Modules
import controllers


# Pair URL routes with Controller functions

@app.route('/')
def index():
	"""Show the web interface home page"""
	return controllers.index()


# User Routes
################################################################################

@app.route('/user/signup', methods = ['GET', 'POST'])
def user_new():
	"""New user creation"""
	return controllers.user_new()


@app.route('/user/login', methods = ['POST'])
def user_login():
	"""Verify and login the User"""
	return controllers.user_login()


@app.route('/user/logout', methods = ['GET'])
def user_logout():
	"""Logout the current User"""
	return controllers.user_logout()


@app.route('/user/<username>', methods = ['GET'])
def user_view(username):
	"""View User profile of user with username 'username'"""
	return controllers.user_view(username)


@app.route('/user/<username>/settings', methods = ['GET'])
def user_edit(username):
	"""Edit User with username 'username'"""
	return controllers.user_edit(username)


#Temporary
@app.route('/user/<username>/location', methods = ['GET', 'POST'])
def user_geolocation(username):
	"""Manually update the current User's geolocation"""
	return controllers.user_geolocation(username)

# Temporary - will be deleted eventually
# Posting Routes
###############################################################################

@app.route('/posting/new', methods = ['GET', 'POST'])
def posting_new():
	"""Route showing form to create a new Posting"""
	return controllers.posting_new()

@app.route('/posting/<id>', methods = ['GET'])
def posting_view(id):
	"""Show the posting with posting_id id"""
	return controllers.posting_view(id)
	
@app.route('/posting/<id>/edit', methods = ['GET'])
def posting_edit(id):
	"""Allow editing the posting with posting_id id"""
	return controllers.posting_edit(id)

# Temporary - to be moved to API
# TODO - move this functionality
@app.route('/posting/nearby', methods=['GET', 'POST'])
def posting_nearby():
	"""Demonstration of ability to query for nearby posts"""
	return controllers.posting_nearby()


# Question Routes
###############################################################################

@app.route('/question/new', methods = ['GET', 'POST'])
def question_new():
	"""New Question creation"""
	return controllers.question_new()

@app.route('/question/<id>', methods = ['GET'])
def question_view(id):
	"""Show the question with question_id id"""
	return controllers.question_view(id)

# Temporary
@app.route('/question/<id>/edit', methods = ['GET'])
def question_edit(id):
	"""Allow editing the question with question_id id"""
	return controllers.question_edit(id)


# Answer Routes
###############################################################################

# Temporary - merge this behavior into the Question view.
@app.route('/answer/new', methods = ['GET', 'POST'])
def answer_new():
	"""Route showing form to create a new Answer"""
	return controllers.answer_new()

# Temporary
# @app.route('/question/<id>', methods = ['GET'])
# def answer_view(id):
# 	"""Show the question with id"""
# 	return controllers.question_view(id)
	
# Temporary - merge onto the Question View for the web interface
# @app.route('/answer/<id>/edit', methods = ['GET'])
# def answer_edit(id):
# 	"""Allow editing the Answer with answer_id id"""
# 	return controllers.answer_edit(id)


# Testing
@app.route('/test', methods=['GET', 'POST'])
def test():
	return controllers.test()



# Web Interface Error Handlers
###############################################################################

@app.errorhandler(404)
def page_not_found(error):
    return controllers.error_404(error)


# # Geolocation Routes
# #############################################################################
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

