# Define models to be used by the Flask Application
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from web_package import db

# One to ones relationships are never truly balanced. After all, the implicit parent may access the 
# child by a property while the implicit child stores the parent_id and accesses the parent via a 
# a backreference. Here Pin is the implicit parent but, notice that this is wrong for our purposes.
# This means you create a Pin and then create a Geolocation. A geolocation cannot exist without a Pin 
# being made for it first - we wish to enforce the opposite invariant - a Pin will at all times have 
# a geolocation.
# This simplified version of the models was very instructive, hence the commit point.

class Pin(db.Model):
    __tablename__ = "pin"
    id = db.Column(db.Integer, primary_key=True)
    geolocation = db.relationship("Geolocation", uselist=False, backref="pin")       # True one to one relationship

    def __init__(self):
        pass

    def __repr__(self):
        return '<Pin Object %s>' % id(self)      # Instance id merely useful to differentiateinstances.


class Geolocation(db.Model):
    __tablename__ = "geolocation"
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)         # Meters
    pin_id = db.Column(db.Integer, db.ForeignKey('pin.id'))           # True one to one relationship
 
    def __init__(self, latitude, longitude, elevation, pin_id):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.pin_id = pin_id

    def __repr__(self):
        return '<Geolocation %s, %s>' % (self.latitude, self.longitude)




# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password_hash = db.Column(db.String(120), nullable=False)
#     salt = db.Column(db.String(120), nullable=False)
#     geolocation_id = db.Column(db.Integer, db.ForeignKey('geolocation.id'))
#     # Relationship References
#     posts = db.relationship('Post', backref=db.backref('user'), lazy='dynamic')        #One user to many posts.
#     geolocation = db.relationship('Geolocation', backref=db.backref('user', uselist=False))

#     # User Initialization
#     def __init__(self, username, password_hash, salt, geolocation_id):
#         self.username = username
#         self.password_hash = password_hash
#         self.salt = salt
#         self.geolocation_id = geolocation_id

#     # User Methods
#     def __repr__(self):
#         return '<User %r>' % self.username



# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     creation_time = db.Column(db.DateTime)
#     expiration_time = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                           #One user to many posts
#     geolocation_id = db.Column(db.Integer, db.ForeignKey('geolocation.id'))             
#     # Relationship References
#     user = db.relationship
#     geolocation = db.relationship('Geolocation', backref=db.backref('post', uselist=False))
    
#     # Post initialization
#     def __init__(self, title, body, create_time, expiration_time, user_id, geolocation_id):
#         self.create_time = create_time
#         self.expiration_time = expiration_time
#         self.user_id = user_id
#         self.geolocation_id = geolocation_id
#         self.title = title
#         self.body = body

#     # Post Methods
#     def __repr__(self):
#         return '<Post %s>' % self.title



# # class Query(Post):
# #   def __init__(self, title, text):
# #       self.title = title
# #       self.text = text


# # class Event(Post):
# #   def __init__(self, title, text, start_time, end_time):
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



