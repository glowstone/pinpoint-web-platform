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
    salt = Column(String(120))
    profile_img_url = Column(String(200))
    # Relationships
    geolocation = relationship('Geolocation', uselist=False, backref='user')
    questions = relationship('Question', backref='author')
    authors = relationship('Answer', backref='author')

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

    def __repr__(self):
        return '<User %s>' % (self.username)

    
class Geolocation(Base):
    __tablename__ = 'geolocation'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    # Relationships
    user_id = Column(Integer, ForeignKey('user.id'))           # One Geolocation to one User
    question_id = Column(Integer, ForeignKey('question.id'))   # One Geolocation to one Question
    # Note either user_id or question_id is null. Users and Questions have their own Geolocation objects. 

    def __init__(self, latitude, longitude, user_id, question_id, *args, **kwargs):
        """
        RESTless requires that each model have an __init__ method that accepts kwargs since 
        this is used for POST create requests.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id
        self.question_id = question_id
        super(Geolocation, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Geolocation %s,%s>' % (self.latitude, self.longitude)


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    text = Column(String(140))
    # Relationships
    user_id = Column(Integer, ForeignKey('user.id'))                    # One User to many Questions
    answers = relationship("Answer", backref="question")                # One Question to many Answers
    geolocation = relationship('Geolocation', uselist=False, backref='question') # One Geolocation to one Question

    def __init__(self, title, text, user_id, *args, **kwargs):
        """
        RESTless requires that each model have an __init__ method that accepts kwargs since 
        this is used for POST create requests.
        """
        self.title = title
        self.text = text
        self.user_id = user_id
        super(Question, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Question %s>' % (self.text)


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    #score = Column(Integer)
    # Relationships
    user_id = Column(Integer, ForeignKey('user.id'))            # One User to many Answers
    question_id = Column(Integer, ForeignKey('question.id'))    # One Question to many Answers

    def __init__(self, text, user_id, *args, **kwargs):
        """
        RESTless requires that each model have an __init__ method that accepts kwargs since 
        this is used for POST create requests.
        """
        self.text = text
        self.user_id = user_id
        super(Answer, self).__init__(*args, **kwargs) 

    def __repr__(self):
        return '<Answer %s>'