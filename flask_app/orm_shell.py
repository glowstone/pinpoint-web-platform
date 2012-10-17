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

ql = Geolocation(9,10,11)
db_session.add(ql)
db_session.commit()

r = Posting(datetime.datetime.now(), datetime.datetime.now(), d.user_id, ql.id)
db_session.add(r)
db_session.commit()

gm = Geolocation(2,3,4)
db_session.add(gm)
db_session.commit()

t = User('tommy', 'weqeqeqew', 'dasdasda', gm.id)
db_session.add(t)
db_session.commit()

gn = Geolocation(1,2,3)
db_session.add(gn)
db_session.commit()

s = Posting(datetime.datetime.now(), datetime.datetime.now(), t.user_id, gn.id)
db_session.add(s)
db_session.commit()


print d.username
print d.geolocation

print p
print p.geolocation
print p.creation_time

print r
print r.geolocation
print r.creation_time

print "Posts"
for post in d.posts:
	print post


for post in Posting.query.all():
	print post
	print post.user




os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()

