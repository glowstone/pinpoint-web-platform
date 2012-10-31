from flask import render_template, redirect, url_for, session, request, flash, abort
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
            username = session.get('username', None)
            if username:
                return redirect(url_for('user_view', username=username)
            else:
                # TODO handle this case. Session was not set correctly
                flash('Server Error')
                return redirect(url_for('user_new'))
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
        # TODO: Handle Invalid logins
        flash("Invalid login")
        return redirect(url_for('index'))

def user_logout():
    """Remove the session username"""
    session.pop('username', None)
    return redirect(url_for('index'))

def user_view(username):
    """Show the current user's profle or redirect to the page with user login"""
    api_response = api.user_current_json()
    if api_response.get('success', None):
        user = api_response['user']
        return render_template('user_view.html', user=user)
    else:
        flash("You must be logged in to view this profile.")
        return redirect(url_for('index'))   

def user_edit(username):
    return render_template('user_edit.html')


def user_geolocation(username):
    """On GET, show form to update user location and on POST update User's geolocation"""
    if request.method == 'GET':
        return render_template('user_geolocation.html')
    elif request.method == 'POST':
        api_response = api.user_set_geolocation_json()
        if api_response.get('success', False):
            return redirect(url_for('user_view', username = session.get('username', None)))
        else:
            # TODO show validation errors
            flash("Bad geolocation update")
            return redirect(url_for('user_geolocation', username = session.get('username', None)))

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



# Question Controller Handlers
###############################################################################

def question_new():
    """On GET show form to create Question or on POST create new Question"""
    if request.method == 'GET':
        return render_template('question_new.html')
    else:
        api_response = api.posting_create_json()
        if api_response.get('success', False):
            return redirect(url_for('user_view', username = session.get('username', None)))
        else:
            # TODO show validation errors
            flash("Bad Posting creation request")
            return redirect(url_for('posting_new'))
    return render_template('question_new.html')


def question_view(id):
    """"""
    return render_template('question_view.html')


def posting_edit(id):
    """"""
    return render_template('question_edit.html')


# Answer Controller Handlers
###############################################################################

def answer_new():
    """"""
    return render_template('answer_new.html')


# Testing
def test():
    abort(404)



# Web Interface Error Handlers
###############################################################################

def error_404(error):
    """Show the page not found error page"""
    return render_template('page_not_found.html'), 404




# # Geolocation Resources
# ###########################################################
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

