# Define models to be used by the Flask Application
#from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, backref, validates
from web_package.database import Base

# One to ones relationships are never truly balanced. After all, the implicit parent may access the 
# child by a property while the implicit child stores the parent_id and accesses the parent via a 
# a backreference. Now the Geolocation has been made the implicit parent. This allows us to enforce 
# the invariant that a Geolocation must exist before a Pin can be created. In other words, at all times, 
# a pin will have a non-null geolocation object associated with it. A Geolocation will not at all times 
# have a Pin associated with it.

# Creating a raw Pin or Posting object is now fine. Null polymorphic types shoudl never be allowed
# at any level of representing an object. Represents the exact (leaf) type of an ORM object.


class Geolocation(Base):
    __tablename__ = "geolocation"
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)         # Meters
    # Relationships
    person = relationship('Pin', uselist=False, backref="geolocation")

    @validates('latitude')
    def validate_latitude(self, key, latitude):              # User-level, not ORM
        assert (latitude >= -90 and latitude <= 90)
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        assert (longitude >= -180 and longitude <= 180)
        return longitude
     
    def __init__(self, latitude, longitude, elevation):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def __repr__(self):
        return '<Geolocation %s, %s>' % (self.latitude, self.longitude)


class Pin(Base):
    __tablename__ = 'pin'
    id = Column(Integer, primary_key=True)
    # Unique constraint ensures that the relationship remains 1-1. No geolocation tied to multiple Pins.
    geolocation_id = Column(Integer, ForeignKey('geolocation.id'), unique=True, nullable=False)  # True one to one relationship (Implicit child)
    type = Column('type', String(50), nullable=False)     # discriminator   #Cannot create raw Pin
    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'pin'}

    def __init__(self, geolocation_id):
        self.geolocation_id = geolocation_id


class User(Pin):
    __tablename__ = 'user'
    # Customary to combine the primary key and foreign key to parent under the column name id or parent_id
    id = Column(Integer, ForeignKey('pin.id'), primary_key=True)
    user_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    username = Column(String(80), unique=True)
    password_hash = Column(String(120))
    salt = Column(String(120))
    posts = relationship('Posting', primaryjoin="(User.user_id==Posting.user_id)", backref=backref('user'), lazy='dynamic')   #One User to many Postings.
    __mapper_args__ = {'polymorphic_identity': 'user',
                       'inherit_condition': (id == Pin.id)}

    def __init__(self, username, password_hash, salt, geo_id):
        super(User, self).__init__(geo_id)
        self.username = username
        self.password_hash = password_hash
        self.salt = salt

    def __repr__(self):
        return '<User %s>' % (self.username)


class Posting(Pin):
    __tablename__ = 'posting'
    id = Column(Integer, ForeignKey('pin.id'), primary_key=True)

    posting_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    creation_time = Column(DateTime)
    expiration_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.user_id'))              # One User to many Postings
    type = Column('type', String(50), nullable=False)  # discriminator    # Cannot create raw Posting
    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'posting',
                        'inherit_condition': (id == Pin.id)}

    def __init__(self, creation_time, expiration_time, user_id, geo_id):
        super(Posting, self).__init__(geo_id)
        # For now, require creation time to be passed in. May make this default to current time.
        self.creation_time = creation_time
        self.expiration_time = expiration_time
        self.user_id = user_id

    def __repr__(self):
        #TODO come up with a better representation
        return '<Post %s>' % (self.creation_time)


class Alert(Posting):
    __tablename__ = 'alert'
    id = Column(Integer, ForeignKey('posting.id'), primary_key=True)
    alert_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    message = Column(String(140))
    __mapper_args__ = {'polymorphic_identity': 'alert',
                        'inherit_condition': (id == Posting.id)}

    def __init__(self, creation_time, expiration_time, message, user_id, geo_id):
        super(Alert, self).__init__(creation_time, expiration_time, user_id, geo_id)
        self.message = message

    def __repr__(self):
        return '<Alert %s>' % (self.message)
        

# class Pin(db.Model):
#     __tablename__ = "pin"
#     id = db.Column(db.Integer, primary_key=True)
#     geolocation_id = db.Column(db.Integer, db.ForeignKey('geolocation.id'))  # True one to one relationship (Implicit child)

#     def __init__(self, geolocation_id):
#         self.geolocation_id = geolocation_id

#     def __repr__(self):
#         return '<Pin Object %s>' % id(self)      # Instance id merely useful to differentiate instances.


# class User(Pin):
#     #id = db.Column(db.Integer, primary_key=True)
#     pin_id = db.Column(db.Integer, db.ForeignKey('pin.id'), primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password_hash = db.Column(db.String(120), nullable=False)
#     salt = db.Column(db.String(120), nullable=False)
#     # Relationships
#     #posts = db.relationship('Post', backref=db.backref('user'), lazy='dynamic')        #One User to many Postings.

#     def __init__(self, username, password_hash, salt, geolocation_id):
#         super(Pin, self).__init__(self, geolocation_id)
#         self.username = username
#         self.password_hash = password_hash
#         self.salt = salt

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



