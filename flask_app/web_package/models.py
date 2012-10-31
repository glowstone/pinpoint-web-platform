# Define models to be used by the Flask Application

from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, backref, validates
from web_package.database import Base

import datetime

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
    pin = relationship('Pin', uselist=False, backref="geolocation")

    @validates('latitude')
    def validate_latitude(self, key, unicode_latitude):              # User-level, not ORM. 
        latitude = float(unicode_latitude)
        assert (latitude >= -90.0 and latitude <= 90.0)
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, unicode_longitude):
        longitude = float(unicode_longitude)
        assert (longitude >= -180.0 and longitude <= 180.0)
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
    type = Column('type', String(50), nullable=False)     # discriminator   
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
    postings = relationship('Posting', primaryjoin="(User.user_id==Posting.user_id)", backref=backref('user'), lazy='dynamic')   #One User to many Postings.
    __mapper_args__ = {'polymorphic_identity': 'user',
                       'inherit_condition': (id == Pin.id)}

    def __init__(self, username, password_hash, salt, geolocation):
        super(User, self).__init__(geolocation.id)
        self.username = username
        self.password_hash = password_hash
        self.salt = salt

    def __repr__(self):
        return '<User %s>' % (self.username)

    def serialize(self):
        return self.__dict__


class Posting(Pin):
    __tablename__ = 'posting'
    id = Column(Integer, ForeignKey('pin.id'), primary_key=True)

    posting_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    creation_time = Column(DateTime)
    expiration_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.user_id'))           # One User to many Postings
    type = Column('type', String(50), nullable=False)               # discriminator    
    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'posting',
                        'inherit_condition': (id == Pin.id)}

    def __init__(self, tdelta, user, geolocation, creation_time=datetime.datetime.now()):
        super(Posting, self).__init__(geolocation.id)
        self.creation_time = creation_time
        self.expiration_time = self.creation_time + tdelta
        self.user_id = user.user_id

    def __repr__(self):
        #TODO come up with a better representation
        return '<Post %s>' % (self.creation_time)


class Commentable(Posting):
    __tablename__ = 'commentable'
    id = Column(Integer, ForeignKey('posting.id'), primary_key=True)
    commentable_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    type = Column('type', String(50), nullable=False)
    comments = relationship('Comment', primaryjoin="(Commentable.commentable_id==Comment.commentable_id)", backref=backref('commentable'), lazy='dynamic')   #One Commentable to many Comments
    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'commentable',
                       'inherit_condition': (id == Posting.id)}

    def __init__(self, tdelta, user, geolocation):
        super(Commentable, self).__init__(tdelta, user, geolocation)

    def __repr__(self):
        return '<Commentable %s>' % id(self)


class Noncommentable(Posting):
    __tablename__ = 'noncommentable'
    id = Column(Integer, ForeignKey('posting.id'), primary_key=True)
    noncommentable_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    type = Column('type', String(50), nullable=False)
    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'noncommentable',
                       'inherit_condition': (id == Posting.id)}

    def __init__(self, tdelta, user, geolocation):
        super(Noncommentable, self).__init__(tdelta, user, geolocation)

    def __repr__(self):
        return '<Commentable %s>' % id(self)


class Question(Commentable):
    __tablename__ = 'question'
    id = Column(Integer, ForeignKey('commentable.id'), primary_key=True)
    question_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    title = Column(String(140))
    text = Column(String(140))
    answers = relationship('Answer', primaryjoin="(Question.question_id==Answer.question_id)", backref=backref('question'), lazy='dynamic')
    __mapper_args__ = {'polymorphic_identity': 'question',
                        'inherit_condition': (id == Commentable.id)}

    def __init__(self, tdelta, user, geolocation, title, text):
        super(Question, self).__init__(tdelta, user, geolocation)
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Question %s>' % (self.text)


class Answer(Commentable):
    __tablename__ = 'answer'
    id = Column(Integer, ForeignKey('commentable.id'), primary_key=True)
    answer_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    text = Column(String(140))           #Change to something bigger later
    score = Column(Integer)
    question_id = Column(Integer, ForeignKey('question.question_id'))        # One Question to many answers
    __mapper_args__ = {'polymorphic_identity': 'answer',
                        'inherit_condition': (id == Commentable.id)}

    def __init__(self, tdelta, user, geolocation, question, text, score=0):
        super(Answer, self).__init__(tdelta, user, geolocation)
        self.text = text
        self.score = score
        self.question_id = question.question_id
        #self.question_id = question     #temp

    def __repr__(self):
        return '<Answer %s>' % (self.text)

    def up_vote():
        self.score += 1

    def down_vote():
        self.score -= 1


class Comment(Noncommentable):
    __tablename__ = 'comment'
    id = Column(Integer, ForeignKey('noncommentable.id'), primary_key=True)
    comment_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    text = Column(String(140))
    commentable_id = Column(Integer, ForeignKey('commentable.commentable_id'))   # One Commentable to many Comments
    __mapper_args__ = {'polymorphic_identity': 'comment',
                        'inherit_condition': (id == Noncommentable.id)}

    def __init__(self, tdelta, user, geolocation, commentable, text):
        super(Comment, self).__init__(tdelta, user, geolocation)
        self.commentable_id = commentable.commentable_id
        self.text = text

    def __repr__(self):
        return '<Comment %s>' % (self.text)


class Alert(Noncommentable):
    __tablename__ = 'alert'
    id = Column(Integer, ForeignKey('noncommentable.id'), primary_key=True)
    alert_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    message = Column(String(140))
    __mapper_args__ = {'polymorphic_identity': 'alert',
                        'inherit_condition': (id == Noncommentable.id)}

    def __init__(self, tdelta, user, geolocation, message):
        super(Alert, self).__init__(tdelta, user, geolocation, message)
        self.message = message

    def __repr__(self):
        return '<Alert %s>' % (self.message)
        




