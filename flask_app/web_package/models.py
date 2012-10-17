# Define models to be used by the Flask Application
#from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from web_package.database import Base

# One to ones relationships are never truly balanced. After all, the implicit parent may access the 
# child by a property while the implicit child stores the parent_id and accesses the parent via a 
# a backreference. Now the Geolocation has been made the implicit parent. This allows us to enforce 
# the invariant that a Geolocation must exist before a Pin can be created. In other words, at all times, 
# a pin will have a non-null geolocation object associated with it. A Geolocation will not at all times 
# have a Pin associated with it.


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=True)
#     email = Column(String(120), unique=True)

#     def __init__(self, name=None, email=None):
#         self.name = name
#         self.email = email

#     def __repr__(self):
#         return '<User %r>' % (self.name)


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column('type', String(50))                  # discriminator
    __mapper_args__ = {'polymorphic_on': type}

    def __init__(self, name):
        self.name = name

# Customary to combine the primary key and foreign key to parent under the column name id or <parent>_id. 
# Also allowed to use 'id' in the table to refer to the foreign key and <class>_id as an explicit reference 
# to the id column in class (id = <class>_id)

class Engineer(Person):
    __tablename__ = 'engineer'
    __mapper_args__ = {'polymorphic_identity': 'engineer'}
    
    # Customary to combine the primary key and foreign key to parent under the column name parent_id
    #person_id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    engineer_id = Column('id', Integer, ForeignKey('person.id'), primary_key=True)
    primary_language = Column(String(50))

    def __init__(self, primary_language, name="Ben"):
        super(Engineer, self).__init__(name)
        self.primary_language = primary_language

    def __repr__(self):
        return '<Engineer %s>' % (self.primary_language)


class Nobody(Person):
    __tablename__ = 'nobody'
    __mapper_args__ = {'polymorphic_identity': 'nobody'}
    nobody_id = Column('id', Integer, ForeignKey('person.id'), primary_key=True)
    prop = Column(String(50))

    def __init__(self, prop, name="Nameless"):
        super(Nobody, self).__init__(name)
        self.prop = prop

    def __repr__(self):
        return '<Nobody %s>' % (self.name)




# class Geolocation(db.Model):
#     __tablename__ = "geolocation"
#     id = db.Column(db.Integer, primary_key=True)
#     latitude = db.Column(db.Float)
#     longitude = db.Column(db.Float)
#     elevation = db.Column(db.Float)         # Meters
#     # Relationships
#     pin = db.relationship('Pin', uselist=False, backref="geolocation")
     
#     def __init__(self, latitude, longitude, elevation):
#         self.latitude = latitude
#         self.longitude = longitude
#         self.elevation = elevation

#     def __repr__(self):
#         return '<Geolocation %s, %s>' % (self.latitude, self.longitude)


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



