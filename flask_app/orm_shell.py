from web_package import db_session
from web_package.models import *
import os
import sys
import datetime

os.system('clear')
sys.ps1 = "cool>>"


g1 = Geolocation(1,2,3)
db_session.add(g1)
db_session.commit()

dalton = User('dalton', 'dsadsadas', 'dwqeqdsadwq', g1.id)
db_session.add(dalton)
db_session.commit()

g2 = Geolocation(2,3,4)
db_session.add(g2)
db_session.commit()

post1 = Posting(datetime.datetime.now(), datetime.datetime.now(), dalton.user_id, g2.id)
db_session.add(post1)
db_session.commit()

g3 = Geolocation(3,4,5)
db_session.add(g3)
db_session.commit()

post2 = Posting(datetime.datetime.now(), datetime.datetime.now(), dalton.user_id, g3.id)
db_session.add(post2)
db_session.commit()

g4 = Geolocation(4,5,6)
db_session.add(g4)
db_session.commit()

commentable1 = Commentable(datetime.datetime.now(), datetime.datetime.now(), dalton.user_id, g4.id)
db_session.add(commentable1)
db_session.commit()


print dalton                  
print dalton.geolocation
print dalton.geolocation.pin

print post2
print post2.geolocation
print post2.type
print post2.user
print post2.id                 #Should be 3 since its the 3rd pin created.
print post2.posting_id         #Should be 2

print commentable1
print commentable1.id          #Should be 4
print commentable1.type        #Should be type commentable (raw posting/commentable still have appropriate types)

for post in dalton.postings:
	print post


print "Phase 2 of Testing"

g5 = Geolocation(5,6,7)
db_session.add(g5)
db_session.commit()

tommy = User('tommy', 'weqeqeqew', 'dasdasda', g5.id)
db_session.add(tommy)
db_session.commit()

g6 = Geolocation(6,7,8)
db_session.add(g6)
db_session.commit()

question1 = Question(datetime.datetime.now(), datetime.datetime.now(), "Does Stata food suck today?", tommy.user_id, g6.id)
db_session.add(question1)
db_session.commit()

g7 = Geolocation(7,8,9)
db_session.add(g7)
db_session.commit()

comment1 = Comment(datetime.datetime.now(), datetime.datetime.now(), "Some comment", dalton.user_id, g7.id, question1.commentable_id)
db_session.add(comment1)
db_session.commit()

g8 = Geolocation(8,9,10)
db_session.add(g8)
db_session.commit()

question2 = Question(datetime.datetime.now(), datetime.datetime.now(), "Where is UAT today?", dalton.user_id, g8.id)
db_session.add(question2)
db_session.commit()

g9 = Geolocation(9,10,11)
db_session.add(g9)
db_session.commit()

comment2 = Comment(datetime.datetime.now(), datetime.datetime.now(), "Tommy's comment", tommy.user_id, g9.id, question2.commentable_id)
db_session.add(comment2)
db_session.commit()

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

answer1 = Answer(datetime.datetime.now(), datetime.datetime.now(), dalton.user_id, g10.id, question2.question_id, "Its in 32-123")
db_session.add(answer1)
db_session.commit()

g11 = Geolocation(11,12,13)
db_session.add(g11)
db_session.commit()

answer2 = Answer(datetime.datetime.now(), datetime.datetime.now(), tommy.user_id, g11.id, question2.question_id, "No, its in 34-101")
db_session.add(answer2)
db_session.commit()


for answer in question2.answers:
	print answer
	print answer.user
	print answer.type
	print answer.question
	print answer.question.type




# gp = Geolocation(10,9,9)
# db_session.add(gp)
# db_session.commit()

# b = Alert(datetime.datetime.now(), datetime.datetime.now(), "Flood!!", d.user_id, gp.id)
# db_session.add(b)
# db_session.commit()

# gq = Geolocation(11,11,9)
# db_session.add(gq)
# db_session.commit()

# c = Question(datetime.datetime.now(), datetime.datetime.now(), "Are you there?", d.user_id, gq.id)
# db_session.add(c)
# db_session.commit()

# print "d Object"
# print d.username
# print d.geolocation
# print d.type

# print "p object"
# print p
# print p.geolocation
# print p.creation_time
# print p.type

# # print r
# # print r.geolocation
# # print r.creation_time

# print "Posts"
# for post in d.posts:
# 	print post


# for post in Posting.query.all():
# 	print post
# 	print post.user

# print "a object"
# print a
# print a.user
# print a.type
# print a.posting_id
# print a.geolocation
# print a.message
# print a.user.geolocation

# print "b object"
# print b
# print b.user
# print b.geolocation
# print b.message
# print b.user.geolocation

# print "c object"
# print c
# print c.query
# print c.type




os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()