from flask import render_template, redirect, url_for, session, request, flash, abort
import util

from app_pkg.blueprints.api.models import *
from app_pkg.blueprints.api import controllers as api

from util import login_required


def index():
    if session.get('user', False):
        # UI would be confusing is logged in Users could visit the Index page (for Signup/Login)
        return redirect(url_for('web.question_list'))
    else:
        context_vars = {}
        context_vars['next'] = request.args.get('next', None)
        return render_template('index.html', custom_vars=context_vars)


def signup():
    """Accepts POST only, to create new User"""
    if request.method == 'POST':
        required_arguments = ['username', 'email', 'password']
        arguments = util.unpack_arguments(required_arguments)
        api_response = api.user_create(**arguments)
        print api_response
        if api_response.get('success', False):
            user = api_response.get('data', None)
            session['user'] = user
            return redirect(url_for('web.question_list'))
        else:
            # TODO show validation errors
            flash("Bad User creation request. " + api_response['error'])
            return redirect(url_for('web.index'))
    else:
        return redirect(url_for('web.index'))
      

def login():
    """
    Accepts POST only.
    Makes an API request to log the user in and redirect Answer page
    """
    if request.method == 'POST':
        required_arguments = ['user_identifier', 'password']
        arguments = util.unpack_arguments(required_arguments)
        filtered_arguments = {'user_identifier': arguments['user_identifier'], \
                              'password': arguments['password']}
        api_response = api.user_authenticate(**filtered_arguments)
        print api_response
        if api_response.get('success', False):
            user = api_response.get('data', None)
            session['user'] = user
            if arguments.get('next', False):
                # Respect 'next' login input
                return redirect(arguments['next'])
            else:
                # Default landing page after login
                return redirect(url_for('web.question_list'))
        else:
            # TODO: Handle Invalid logins
            flash("Invalid login")
            return redirect(url_for('web.index'))
    else:
        return redirect(url_for('web.index'))


def logout():
    """Deauthenticate user by popping the user's session instance."""
    session.pop('user', None)
    flash("Logged out")
    return redirect(url_for('web.index'))


@login_required
def question_list():
    return render_template('question_list.html')


@login_required
def question_show(question_id):
    print question_id
    context_vars = {}
    context_vars['question_id'] = question_id
    return render_template('question_show.html', custom_vars=context_vars)


@login_required
def ask():
    return render_template('ask.html')
    

@login_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html')
    else:
        print request.form
        required_arguments = ['old_password', 'new_password', 'new_password_repeat']

        return "Re-setting"


# Controllers for Meta Pages
###############################################################################

def about():
    """About Page"""
    return render_template('meta/about.html')


def contact():
    """Contact Page"""
    return render_template('meta/contact.html')


def faq():
    """FAQ Page"""
    return render_template('meta/faq.html')


def privacy():
    """Privacy Policy Page"""
    return render_template('meta/privacy.html')


# Testing
def test():
    print "testing"
    abort(404)



# Web Interface Error Handlers
###############################################################################

def error_404(error):
    """Show the page not found error page"""
    return render_template('error/404.html'), 404









# def user_geolocation(username):
#     """On GET, show form to update user location and on POST update User's geolocation"""
#     if request.method == 'GET':
#         return render_template('user_geolocation.html')
#     elif request.method == 'POST':
#         api_response = api.user_set_geolocation_json()
#         if api_response.get('success', False):
#             return redirect(url_for('web.user_show', username = session.get('username', None)))
#         else:
#             # TODO show validation errors
#             flash("Bad geolocation update")
#             return redirect(url_for('web.user_geolocation', username = session.get('username', None)))

# # Posting Controller Handlers
# ###############################################################################

# def posting_new():
#     """On GET show form to create Posting or on POST create new Posting"""
#     if request.method == 'GET':
#         return render_template('posting_new.html')
#     else:
#         api_response = api.posting_create_json()
#         if api_response.get('success', False):
#             return redirect(url_for('web.user_show', username = session.get('username', None)))
#         else:
#             # TODO show validation errors
#             flash("Bad Posting creation request")
#             return redirect(url_for('web.posting_new'))

# def posting_view(id):
#     # TODO: Check whether user has permission to view the post
#     # Current permission model - all public, but don't show authors if not authenticated.
#     #post = Post.query.filter_by(id=id).first()
#     return render_template('posting_view.html', post=post)


# def posting_edit(id):
#     # TODO populate form apprpriately and check permissions
#     return render_template('posting_edit.html')

# # Temporary - will be moved to API
# def posting_nearby():
#     if request.method == 'POST':
#         radius = float(request.form['radius'])
#         location = get_current_user().geolocation
#         posts = closest_posts(location, radius)
#         return render_template('nearby_posts.html', location=location, radius=radius, posts=posts)
        
#     elif request.method == 'GET':
#         return render_template('nearby_posts.html')



# # Question Controller Handlers
# ###############################################################################

# def question_new():
#     """On GET show form to create Question or on POST create new Question"""
#     if request.method == 'GET':
#         return render_template('question_new.html')
#     else:
#         api_response = api.question_create_json()
#         if api_response.get('success', False):
#             return redirect(url_for('user_show', username = session.get('username', None)))
#         else:
#             # TODO show validation errors
#             flash("Bad Question creation request")
#             return redirect(url_for('question_new'))

# def question_list():
#     questions = api.question_list_json()
#     if questions:
#         return render_template('question_list.html', questions=questions)
#     else:
#         abort(404)

# def question_show(id):
#     """Show the Question with 'question_id' id"""
#     question = api.question_get_json(id)
#     # if api_response.get('success', False):
#     #     question = api_response.get('question', None)           # Safe dict lookup
#     if question:
#         return render_template('question_show.html', question=question)
#     else:
#         abort(404)

# # Temporary
# def question_edit(id):
#     """Edit the Question with 'question_id' id"""
#     # API Call
#     return render_template('question_edit.html', id=id)


# # Answer Controller Handlers
# ###############################################################################

# def answer_new():
#     """On GET show form to create Answer or on POST create new Answer"""
#     # Temporary - will make answers from question view page
#     if request.method == 'GET':
#         return render_template('answer_new.html')
#     else:
#         api_response = api.answer_create_json()
#         if api_response.get('success', False):
#             return redirect(url_for('user_show', username = session.get('username', None)))
#         else:
#             # TODO show validation errors
#             flash("Failed to create the Answer")
#             return redirect(url_for('answer_new'))

# def answer_new_async():
#     # TODO
#     pass
    



# # Comment Controller Handler
# ###############################################################################

# def comment_new():
#     """On GET show form to create Comment or on POST create new Answer"""
#     # Temporary - will make comments from question view page
#     if request.method == 'GET':
#         return render_template('comment_new.html')
#     else:
#         api_response = api.comment_create_json()
#         if api_response.get('success', False):
#             return redirect(url_for('user_show', username = session.get('username', None)))
#         else:
#             # TODO show validation errors
#             flash("Failed to create the Answer")
#             return redirect(url_for('answer_new'))






