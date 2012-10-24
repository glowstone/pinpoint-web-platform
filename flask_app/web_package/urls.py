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
	"""Verify and login the user"""
	return controllers.user_login()


@app.route('/user/logout', methods = ['GET'])
def user_logout():
	"""Logout the current user"""
	return controllers.user_logout()


@app.route('/user/<username>', methods = ['GET'])
def user_view(username):
	"""View user profile"""
	return controllers.user_view(username)


@app.route('/user/<id>/settings', methods = ['GET'])
def user_edit(id):
	"""Edit user settings"""
	return controllers.user_edit()

# Temporary
@app.route('/user/location', methods = ['GET', 'POST'])
def user_location():
	"""Temporary page for setting a user's location"""
	return controllers.user_location()

# Posting Routes
###############################################################################

@app.route('/posting/new', methods = ['GET', 'POST'])
def posting_new():
	"""Route showing form to create a new Posting"""
	return controllers.posting_new()

@app.route('/posting/<id>', methods = ['GET'])
def posting_view(id):
	"""Show the posting with id"""
	return controllers.posting_view(id)
	
@app.route('/posting/<id>/edit', methods = ['GET'])
def posting_edit(id):
	"""Allow editing the posting with id"""
	return controllers.posting_edit(id)

# Temporary - to be moved to API
@app.route('/posting/nearby', methods=['GET', 'POST'])
def posting_nearby():
	"""Demonstration of ability to query for nearby posts"""
	return controllers.posting_nearby()


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

