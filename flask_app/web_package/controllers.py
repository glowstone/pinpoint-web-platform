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
            return redirect(url_for('user_view', username = session.get('username', None)))
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
    #post = Post.query.filter_by(id=id).first()
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
        api_response = api.question_create_json()
        if api_response.get('success', False):
            return redirect(url_for('user_view', username = session.get('username', None)))
        else:
            # TODO show validation errors
            flash("Bad Question creation request")
            return redirect(url_for('question_new'))

def question_list():
    questions = api.question_list_json()
    if questions:
        return render_template('question_list.html', questions=questions)
    else:
        abort(404)

def question_get(id):
    """Show the Question with 'question_id' id"""
    question = api.question_get_json(id)
    # if api_response.get('success', False):
    #     question = api_response.get('question', None)           # Safe dict lookup
    if question:
        return render_template('question_view.html', question=question)
    else:
        abort(404)

# Temporary
def question_edit(id):
    """Edit the Question with 'question_id' id"""
    # API Call
    return render_template('question_edit.html', id=id)


# Answer Controller Handlers
###############################################################################

def answer_new():
    """On GET show form to create Answer or on POST create new Answer"""
    # Temporary - will make answers from question view page
    if request.method == 'GET':
        return render_template('answer_new.html')
    else:
        api_response = api.answer_create_json()
        if api_response.get('success', False):
            return redirect(url_for('user_view', username = session.get('username', None)))
        else:
            # TODO show validation errors
            flash("Failed to create the Answer")
            return redirect(url_for('answer_new'))

def answer_new_async():
    # TODO
    pass
    



# Comment Controller Handler
###############################################################################

def comment_new():
    """On GET show form to create Comment or on POST create new Answer"""
    # Temporary - will make comments from question view page
    if request.method == 'GET':
        return render_template('comment_new.html')
    else:
        api_response = api.comment_create_json()
        if api_response.get('success', False):
            return redirect(url_for('user_view', username = session.get('username', None)))
        else:
            # TODO show validation errors
            flash("Failed to create the Answer")
            return redirect(url_for('answer_new'))




# Testing
def test():
    abort(404)



# Web Interface Error Handlers
###############################################################################

def error_404(error):
    """Show the page not found error page"""
    return render_template('page_not_found.html'), 404

