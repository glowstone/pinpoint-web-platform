from app_pkg.database import db_session
from app_pkg.blueprints.api_pkg.models import *

import datetime

g1 = Geolocation(1,2,3)
db_session.add(g1)
db_session.commit()

dalton = User('dalton', 'dsadsadas', 'dwqeqdsadwq', g1)
db_session.add(dalton)
db_session.commit()

g2 = Geolocation(2,3,4)
db_session.add(g2)
db_session.commit()

post1 = Posting(datetime.timedelta(hours=6), dalton, g2)
db_session.add(post1)
db_session.commit()

g3 = Geolocation(3,4,5)
db_session.add(g3)
db_session.commit()

post2 = Posting(datetime.timedelta(hours=12), dalton, g3)
db_session.add(post2)
db_session.commit()

g4 = Geolocation(4,5,6)
db_session.add(g4)
db_session.commit()

commentable1 = Commentable(datetime.timedelta(hours=12), dalton, g4)
db_session.add(commentable1)
db_session.commit()


print dalton                  
print dalton.geolocation
print dalton.geolocation.pin

print User.query.all()

print post2
print post2.geolocation
print post2.type
print post2.user
print post2.id                 #Should be 3 since its the 3rd pin created.
print post2.posting_id         #Should be 2

print commentable1
print commentable1.id          #Should be 4
print commentable1.type        #Should be type commentable (raw posting/commentable still have appropriate types)

print Posting.query.all()
for post in dalton.postings:
	print post
print Commentable.query.all()
print Noncommentable.query.all()

print "Phase 2 of Testing"

g5 = Geolocation(5,6,7)
db_session.add(g5)
db_session.commit()

tommy = User('tommy', 'weqeqeqew', 'dasdasda', g5)
db_session.add(tommy)
db_session.commit()

g6 = Geolocation(6,7,8)
db_session.add(g6)
db_session.commit()

question1 = Question(datetime.timedelta(hours=6), tommy, g6, "Does Stata food suck today?", "Just wondering")
db_session.add(question1)
db_session.commit()

print Question.query
print Question.query.filter_by(title="Does Stata food suck today?").first()

g7 = Geolocation(7,8,9)
db_session.add(g7)
db_session.commit()

comment1 = Comment(datetime.timedelta(hours=12), dalton, g7, question1, "Some comment")
db_session.add(comment1)
db_session.commit()

g8 = Geolocation(8,9,10)
db_session.add(g8)
db_session.commit()

question2 = Question(datetime.timedelta(days=1), dalton, g8, "Where is UAT today?", "I want to know")
db_session.add(question2)
db_session.commit()

g9 = Geolocation(9,10,11)
db_session.add(g9)
db_session.commit()

comment2 = Comment(datetime.timedelta(days=3), tommy, g9, question2, "Tommy's comment")
db_session.add(comment2)
db_session.commit()

print Comment.query.all()
print Answer.query.all()
print Question.query.all()


print question1
print question1.query
print question1.user_id
print question1.geolocation
print question1.user
print question1.commentable_id
print "Show all comments:"
for comment in question1.comments:
	print comment


print question2
print question2.type
print question2.geolocation

print comment1
print comment1.commentable
print comment2
print comment2.commentable.type


print "\nTesting Phase 3"
g10 = Geolocation(10,11,12)
db_session.add(g10)
db_session.commit()

answer1 = Answer(datetime.timedelta(hours=6), dalton, g10, question2, "Its in 32-123")
db_session.add(answer1)
db_session.commit()

g11 = Geolocation(11,12,13)
db_session.add(g11)
db_session.commit()

answer2 = Answer(datetime.timedelta(days=1), tommy, g11, question2, "No, its in 34-101")
db_session.add(answer2)
db_session.commit()


for answer in question2.answers:
	print answer
	print answer.user
	print answer.type
	print answer.question
	print answer.question.type