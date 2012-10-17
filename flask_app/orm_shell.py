from web_package import db_session
from web_package.models import *
import os
import sys
import datetime

os.system('clear')
sys.ps1 = "cool>>"


g = Geolocation(5,6,7)
db_session.add(g)
db_session.commit()

d = User('dalton', 'dsadsadas', 'dwqeqdsadwq', g.id)
db_session.add(d)
db_session.commit()

q = Geolocation(8,9,10)
db_session.add(q)
db_session.commit()

p = Posting(datetime.datetime.now(), datetime.datetime.now(), d.user_id, q.id)
db_session.add(p)
db_session.commit()

# ql = Geolocation(9,10,11)
# db_session.add(ql)
# db_session.commit()

# r = Posting(datetime.datetime.now(), datetime.datetime.now(), d.user_id, ql.id)
# db_session.add(r)
# db_session.commit()

gm = Geolocation(2,3,4)
db_session.add(gm)
db_session.commit()

t = User('tommy', 'weqeqeqew', 'dasdasda', gm.id)
db_session.add(t)
db_session.commit()

# gn = Geolocation(1,2,3)
# db_session.add(gn)
# db_session.commit()

# s = Posting(datetime.datetime.now(), datetime.datetime.now(), t.user_id, gn.id)
# db_session.add(s)
# db_session.commit()

go = Geolocation(0,1,2)
db_session.add(go)
db_session.commit()

a = Alert(datetime.datetime.now(), datetime.datetime.now(), "Warning!!!", t.user_id, go.id)
db_session.add(a)
db_session.commit()

gp = Geolocation(10,9,9)
db_session.add(gp)
db_session.commit()

b = Alert(datetime.datetime.now(), datetime.datetime.now(), "Flood!!", d.user_id, gp.id)
db_session.add(b)
db_session.commit()


print d.username
print d.geolocation
print d.type

print p
print p.geolocation
print p.creation_time
print p.type

# print r
# print r.geolocation
# print r.creation_time

print "Posts"
for post in d.posts:
	print post


for post in Posting.query.all():
	print post
	print post.user

print a
print a.user
print a.type
print a.geolocation
print a.message
print a.user.geolocation

print b
print b.user
print b.geolocation
print b.message
print b.user.geolocation




os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()

