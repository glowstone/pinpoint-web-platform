from app_pkg.blueprints.web import web_bp as web 
from app_pkg import app   # Web blueprint responsible for general application errors.
from app_pkg.blueprints.web import controllers


# Connect URL routes with Controller functions

@web.route('/')
def index():
    return controllers.index()
    

@web.route('/signup', methods = ['POST'])
def signup():
    """Accept posts to create new User."""
    return controllers.signup()


@web.route('/login', methods = ['POST'])
def login():
    """Attempt to authenticate User who tries to login."""
    return controllers.login()


@web.route('/logout', methods = ['GET'])
def logout():
    """Destroy User's authenticated session"""
    return controllers.logout()


@web.route('/user/<username>', methods=['GET'])
def question_list():
    """Show the question listing page"""
    return controllers.question_list()


@web.route('/question/<int:question_id>', methods=['GET'])
def question_detail(question_id):
    """Show the question_detail page for the specified question"""    
    return controllers.question_detail(question_id)


@web.route('/users', methods=['GET'])
def user_list():
    return controllers.user_list()
    

@web.route('/settings', methods = ['GET'])
def settings():
    return controllers.settings()


# Meta Pages
###############################################################################

@web.route('/about', methods = ['GET'])
def about():
    return controllers.about()

@web.route('/contact', methods = ['GET'])
def contact():
    return controllers.contact()

@web.route('/faq', methods = ['GET'])
def faq():
    return controllers.faq()

@web.route('/privacy', methods = ['GET'])
def privacy():
    return controllers.privacy()


# Web Interface Error Handlers
###############################################################################


@app.errorhandler(404)
def error_404(error):
    return controllers.error_404(error)
