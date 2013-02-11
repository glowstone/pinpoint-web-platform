# Define models to be used by the Flask Application

from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Float, DateTime, Unicode, \
Text
from sqlalchemy.orm import relationship, backref, validates
from app_pkg.database import Base

from app_pkg.blueprints.api import util

# Libraries for encoding urls and generating md5 hashes for Gravatar
import urllib, hashlib

import datetime


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(140), nullable=False)
    salt = Column(String(120), nullable=False)
    profile_img_url = Column(String(200), nullable=False)
    gcm_registration_id = Column(String(250))
    # Relationships
    questions = relationship('Question', backref='author')
    answers = relationship('Answer', backref='author')

    def __init__(self, username, email, password_hash, salt, *args, **kwargs):
        """
        RESTless requires that each model have an __init__ method that accepts kwargs since 
        this is used for POST create requests.
        """
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.salt = salt
        self.set_gravatar_profile_img(email)
        super(User, self).__init__(*args, **kwargs)

    @staticmethod
    def create_user(username, email, password):
        """
        Accepts string username, email and password. Creates and returns a new User object 
        (with gravatar profile img url setup) by generating a random salt and hashing the 
        provided password. Returned User object has not been saved to the db.
        This method is meant to be the Flask variant of Django's auth.User 
        User.objects.create_user(username, email, password)
        """
        salt = util.random_salt()
        password_hash = util.hash_w_salt(password, salt)
        user = User(username, email, password_hash, salt)
        user.set_gravatar_profile_img(email)
        return user
        
    def set_gravatar_profile_img(self, email):
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':'identicon'})
        self.profile_img_url = gravatar_url

    def serialize(self):
        return {
            'id': self.id,
            'username' : self.username,
            'profile_img_url': self.profile_img_url,
            'gcm_registration_id': self.gcm_registration_id,
        }

    def __repr__(self):
        return '<User %s>' % (self.username)


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    title = Column(String(140), nullable=False)
    text = Column(String(140), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    # Relationships
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)    # One User to many Questions
    answers = relationship("Answer", backref="question")                # One Question to many Answers

    def __init__(self, title, text, latitude, longitude, user_id, *args, **kwargs):
        """
        RESTless requires that each model have an __init__ method that accepts kwargs since 
        this is used for POST create requests.
        """
        self.title = title
        self.text = text
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        super(Question, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Question %s>' % (self.title)


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False) 
    # Relationships
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)            # One User to many Answers
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)    # One Question to many Answers

    def __init__(self, text, latitude, longitude, question_id, user_id, *args, **kwargs):
        """
        RESTless requires that each model have an __init__ method that accepts kwargs since 
        this is used for POST create requests.
        """
        self.text = text
        self.latitude = latitude
        self.longitude = longitude
        self.question_id = question_id
        self.user_id = user_id
        super(Answer, self).__init__(*args, **kwargs) 

    def __repr__(self):
        return '<Answer %s>' % self.text