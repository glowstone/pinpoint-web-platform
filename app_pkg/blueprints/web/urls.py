# Web Interface URLs
from flask import render_template, redirect, url_for
# Package Variables
from app_pkg.blueprints.web import web_bp as web 

# Package Modules
from app_pkg.blueprints.web import controllers

# Web blueprint responsible for general Application errors (404, etc.)
from app_pkg import app


# Connect URL routes with Controller functions

@web.route('/')
def index():
    """Show the web interface home page"""
    return controllers.index()
    

@web.route('/signup', methods = ['POST'])
def signup():
    """New user creation"""
    return controllers.signup()


@web.route('/login', methods = ['POST'])
def login():
    """Verify and set the User authenticated session context"""
    return controllers.login()


@web.route('/logout', methods = ['GET'])
def logout():
    """Destroy User's authenticated session"""
    return controllers.logout()


@web.route('/questions', methods=['GET'])
def question_list():
    """Show the questions map"""
    return controllers.question_list()


@web.route('/question/<int:question_id>', methods=['GET'])
def question_show(question_id):
    """Shows a particular question in detail"""
    print question_id
    print controllers.question_show
    print controllers.question_show(question_id)
    return controllers.question_show(question_id)


@web.route('/ask', methods=['GET'])
def ask():
    """Shows the interface for asking a question"""
    return controllers.ask()
    
# @web.route('/user/<username>', methods = ['GET'])
# def profile(username):
#     """Show User profile of user with username 'username'"""
#     return controllers.profile(username)


@web.route('/settings', methods = ['GET', 'POST'])
def settings():
    """Change the settings for the current User"""
    return controllers.settings()


# Footer Linked Pages
###############################################################################

@web.route('/about', methods = ['GET'])
def about():
    """About Page"""
    return controllers.about()

@web.route('/contact', methods = ['GET'])
def contact():
    """Contact Page"""
    return controllers.contact()

@web.route('/faq', methods = ['GET'])
def faq():
    """FAQ Page"""
    return controllers.faq()

@web.route('/privacy', methods = ['GET'])
def privacy():
    """Privacy Policy Page"""
    return controllers.privacy()


# Web Interface Error Handlers
###############################################################################

@web.route('/test')
def test():
    return controllers.test()

@app.errorhandler(404)
def error_404(error):
    return controllers.error_404(error)



# #Temporary
# @web.route('/user/<username>/location', methods = ['GET', 'POST'])
# def user_geolocation(username):
#     """Manually update the current User's geolocation"""
#     return controllers.user_geolocation(username)

# # Temporary - will be deleted eventually
# # Posting Routes
# ###############################################################################

# @app.route('/posting/new', methods = ['GET', 'POST'])
# def posting_new():
#     """Route showing form to create a new Posting"""
#     return controllers.posting_new()

# @app.route('/posting/<id>', methods = ['GET'])
# def posting_view(id):
#     """Show the posting with posting_id id"""
#     return controllers.posting_view(id)
    
# @app.route('/posting/<id>/edit', methods = ['GET'])
# def posting_edit(id):
#     """Allow editing the posting with posting_id id"""
#     return controllers.posting_edit(id)

# # Temporary - to be moved to API
# # TODO - move this functionality
# @app.route('/posting/nearby', methods=['GET', 'POST'])
# def posting_nearby():
#     """Demonstration of ability to query for nearby posts"""
#     return controllers.posting_nearby()


# Question Routes
###############################################################################

# @web.route('/question/new', methods = ['GET', 'POST'])
# def question_new():
#     """New Question creation"""
#     return controllers.question_new()

# @web.route('/question', methods=['GET'])
# def question_list():
#     """List all the Questions near to the current User"""
#     # TODO Just dumps all questions for now
#     return controllers.question_list()

# @web.route('/question/<id>', methods = ['GET'])
# def question_show(id):
#     """Show the question with 'question_id' id"""
#     return controllers.question_show(id)

# # Temporary
# @web.route('/question/<id>/edit', methods = ['GET'])
# def question_edit(id):
#     """Allow editing the question with question_id id"""
#     return controllers.question_edit(id)


# Answer Routes
###############################################################################

# # Temporary - merge this behavior into the Question view.
# @web.route('/answer/new', methods = ['GET', 'POST'])
# def answer_new():
#     """Route showing form to create a new Answer"""
#     return controllers.answer_new()

# # Comment Routes
# ###############################################################################

# @web.route('/comment/new', methods = ['GET', 'POST'])
# def comment_new():
#     """Route for creating a Comment"""
#     return controllers.comment_new()


# ###############################################################################

# # Testing
# @web.route('/test', methods=['GET', 'POST'])
# def test():
#     return controllers.test()






# # Geolocation Routes
# #############################################################################
# @app.route('/location/<id>', methods = ['GET'])
# def geolocation_show(id):
#   geolocation = Geolocation.query.filter_by(id=id).first()
#   return render_template('geolocation_show.html', geolocation=geolocation)

# @app.route('/location/new', methods = ['GET'])
# def geolocation_new():
#   return render_template('geolocation_new.html')

# @app.route('/location/create', methods = ['POST'])
# def geolocation_create():
#   user = get_current_user()
#   return redirect(url_for('index'))

# #############################################################
# @app.route('/test', methods = ['GET'])
# def test():
#   username = session['username']
#   print "All your Posts"
#   user = User.query.filter_by(username=username).first()

#   print user.posts
#   for post in user.posts:

#       print post
#       print post.geolocation

#   return render_template('test.html', posts=user.posts)

