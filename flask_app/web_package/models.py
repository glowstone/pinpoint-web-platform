# Define models to be used by the Flask Application
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from web_package import db

class User(db.Model):
    # User Database Representation
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(120), nullable=False)
    # Relationship References
    posts = db.relationship('Post', backref=db.backref('user'), lazy='dynamic')

    # User Initialization
    def __init__(self, username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt

    # User Methods
    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    # Post Database Representation
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #abstract_location_id = db.Column(db.Integer, db.ForeignKey('AbstractLocation.id'))
    creation_time = db.Column(db.DateTime)
    deletion_time = db.Column(db.DateTime)
    ttl_time = db.Column(db.DateTime)
    # Eventually move these attributes to a subclass
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    # Relationship References
    # Abstract location

    # Post initialization
    def __init__(self, title, body, create_time, ttl_time, delete_time, user_id):
        self.create_time = create_time
        self.ttl_time = ttl_time
        self.delete_time = delete_time
        self.user_id = user_id
        #self.abstract_location_id = abstract_location_id
        self.title = title
        self.body = body

    # Post Methods
    def __repr__(self):
        return '<Post %r>' % self.title

# class Query(Post):
#   def __init__(self, title, text):
#       self.title = title
#       self.text = text


# class Event(Post):
#   def __init__(self, title, text, start_time, end_time):
#       self.title = title
#       self.text = text
#       self.start_time = start_time
#       self.end_time = end_time

# class Challenge(Post):
#   def __init__(self, title, challenge_text):
#       self.title = title


# class Alert(Post):
#   def __init__(self, alert_msg);
#       self.alert_msg = alert_msg



