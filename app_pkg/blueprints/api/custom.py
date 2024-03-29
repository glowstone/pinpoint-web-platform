# Environment Modules
from flask import session, request

# Package Variables
from app_pkg.database import db_session

from app_pkg.blueprints.api import util
from app_pkg.blueprints.api.util import login_required, send_gcm_message

from models import User, Question, Answer


def user_create(username, email, password):
    """Create a new User"""
    if len(username) < 3:
        return util.error_response("Username too short")
    
    salt = util.random_salt()
    password_hash = util.hash_w_salt(password, salt)
    user = User(username, email, password_hash, salt)
    db_session.add(user)
    try:
        db_session.commit()
    except Exception:               # SQLAlchemyError would be better, but not sure how to import it.
        db_session.rollback()       
        return util.error_response("Database error creating User")
        
    return util.success_response(user)


def user_authenticate(user_identifier, password):
    """Authenticate the user with either email or password"""
    # Try to authenticate with Username
    user = User.query.filter_by(username=user_identifier).first()
    if user is not None:
        if util.is_authenticated(password, user.salt, user.password_hash):
            return util.success_response(user)
        else:
            return util.error_response('Invalid password')
    # Try to authenticate with Email
    else:
        user = User.query.filter_by(email=user_identifier).first()
        if user is not None:
            if util.is_authenticated(password, user.salt, user.password_hash):
                return util.success_response(user)
            else:
                return util.error_response('Invalid password')
        else:
            return util.error_response('No User with that username or email')


def user_show(username):
    """
    Queries for a user with the given username and returns the user as 'data' if found.
    """
    user = User.query.filter_by(username=username).first()    # Returns None if no User found
    if user:
        return util.success_response(user)
    else:
        return util.error_response("No user with username " + username)


def user_put_latlong(latitude, longitude):
    """Update's the authenticated user's Geolocation"""
    username = session['user'].username
    # We want to modify the database User, not the (possibly stale) copy in the session.
    user = User.query.filter_by(username=username).first()    # Returns None if no User found
    if user:
        user.latitude = float(latitude)
        user.longitude = float(longitude)
        db_session.commit()
        return util.success_response(user)
    else:
        return util.error_response("Session user was not found.")


def user_register_gcm(registration_id):
    """
    Updates the current authenticated User's gcm_registration_id.
    """
    username = session['user'].username
    # We want to modify the database User, not the (possible stale) copy in the session.
    user = User.query.filter_by(username=username).first()    # Returns None if no User found
    if user:
        user.gcm_registration_id = registration_id
        db_session.commit()
        return util.success_response(user)
    else:
        return util.error_response("No user with username " + username)


def question_create(title, text, latitude, longitude):
    """Create a new Question"""
    user_id = session['user'].id
    question = Question(title, text, latitude, longitude, user_id)
    try:
        db_session.add(question)
        db_session.commit()

        # Send a GCM message
        users = User.query.filter(User.id != user_id).all()
        send_gcm_message(users, {'data': 'New message'})
        return util.success_response({})
    except Exception:               # SQLAlchemyError would be better, but not sure how to import it.
        db_session.rollback()
        return util.error_response("Database error creating Question")
        

def answer_create(text, latitude, longitude, question_id):
    """Create a new Question"""
    user_id = session['user'].id
    answer = Answer(text, latitude, longitude, question_id, user_id)
    try:
        db_session.add(answer)
        db_session.commit()
        return util.success_response({})
    except Exception:               # SQLAlchemyError would be better, but not sure how to import it.
        db_session.rollback()
        return util.error_response("Database error creating Answer")





