from flask import render_template, redirect, url_for, session, \
request, flash, abort
from app_pkg.blueprints.api.models import *
from app_pkg.blueprints.api import custom as custom_api

import util
from util import login_required


def index():
    """
    Show the web interface home page or redirect to the question_list if the User
    is already authenticated.
    """
    if session.get('user', False):
        user = session.get('user')
        # UI would be confusing is logged in Users could visit the Index page (for Signup/Login)
        return redirect(url_for('web.question_list', username=user.username))
    else:
        context_vars = {}
        context_vars['next'] = request.args.get('next', None)
        return render_template('index.html', **context_vars)


def signup():
    """
    Accepts POST only.
    Makes an API request to authenticate the user, log the User in, and redirect
    to the question listing page.
    """
    if request.method == 'POST':
        required_arguments = ['username', 'email', 'password']
        arguments = util.unpack_arguments(required_arguments)
        api_response = custom_api.user_create(**arguments)
        print api_response
        if api_response.get('success', False):
            user = api_response.get('data', None)
            session['user'] = user
            return redirect(url_for('web.question_list', username=user.username))
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
        api_response = custom_api.user_authenticate(**filtered_arguments)
        print api_response
        if api_response.get('success', False):
            user = api_response.get('data', None)
            session['user'] = user
            if arguments.get('next', False):
                # Respect 'next' login input
                return redirect(arguments['next'])
            else:
                # Default landing page after login
                return redirect(url_for('web.question_list', username=user.username))
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
def question_list(username):
    """
    Show the question listing page for the User with the given username.
    """
    api_response = custom_api.user_show(username)
    if api_response.get('success', False):
        user = api_response['data']
        context_vars = {}
        context_vars['user_id'] = session['user'].id
        context_vars['page_for'] = user
        return render_template('question_list.html', **context_vars)
    else:
        # No User with that username
        abort(404)


@login_required
def question_detail(question_id):
    """Show the question_detail page for the specified question"""    
    context_vars = {}
    context_vars['user_id'] = session['user'].id
    context_vars['question_id'] = question_id
    return render_template('question_detail.html', **context_vars)


@login_required
def user_list():
    """Show the user listing page"""
    context_vars = {}
    context_vars['user_id'] = session['user'].id
    return render_template('user_list.html', **context_vars)


@login_required
def settings():
    """Change the settings for the current User"""
    return render_template('settings.html')
    

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


# Web Interface Error Handlers
###############################################################################

def error_404(error):
    """Show the page not found error page"""
    return render_template('error/404.html'), 404






