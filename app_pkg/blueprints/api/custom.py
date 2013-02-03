# Environment Modules
from flask import session, request

# Package Variables
from app_pkg.database import db_session

from app_pkg.blueprints.api import util

# Package Modules
#from sqlalchemy.core.exceptions import *
from models import *


# Libraries
import datetime


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
        db_session.rollback()       # TODO: Does not rollback geolocation creation as we would like
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
    """Queries for the given user. Check whether that is the current user"""
    user = User.query.filter_by(username=username).first()
    authenticated_user_id = session.get("user_id", None)
    if user:
        if user.user_id == authenticated_user_id:       # Authenticated User
            return util.success_response({"user": user, "authenticated": True})
        else:                                           # Unauthenticated User (public profile will be shown)
            return util.success_response({"user": user, "authenticated": False})
    else:
        return util.error_response("No user with username " + username)


def current_session_user():
    """Internal Method for finding the User object corresponding to the current authenticated request session"""
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return util.success_response(user)
        else:
            return util.error_response("No user found with Session's user_id")
    else:
        return util.error_response("Session does not contain a user_id")


def user_set_geolocation_json(latitude, longitude, elevation=None):
    """Update's the authenticated user's Geolocation"""
    user = current_session_user()['data']
    if user:
        latitude = float(latitude)        # Take out when argument manager is created
        longitude = float(longitude)      # Take out when argument manager is created
        # Update Geolocation
        geolocation = user.geolocation
        geolocation.latitude = latitude
        geolocation.longitude = longitude
        if elevation:
            geolocation.elevation = elevation
        db_session.commit()
        return util.success_response()
    else:
        return util.error_response("Session user was not found.")



