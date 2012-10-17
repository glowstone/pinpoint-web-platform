from web_package import db_session
from web_package.models import *
import os
import sys
import datetime

os.system('clear')
sys.ps1 = "cool>>"


# g = Geolocation(5,6,7)
# db_session.add(g)
# db_session.commit()

# d = User('dalton', 'dsadsadas', 'dwqeqdsadwq', g.id)
# db_session.add(d)
# db_session.commit()

# q = Geolocation(8,9,10)
# db_session.add(q)
# db_session.commit()

# p = Posting(datetime.datetime.now(), datetime.datetime.now(), q.id)
# db_session.add(p)
# db_session.commit()

# print d.geolocation
# print d.username

# print p.geolocation
# print p.creation_time



g = Geolocation(5,6,7)
db_session.add(g)
db_session.commit()

d = User('dalton', 'dsadsadas', 'dwqeqdsadwq', g.id)
db_session.add(d)
db_session.commit()

q = Geolocation(8,9,10)
db_session.add(q)
db_session.commit()

p = Posting(datetime.datetime.now(), datetime.datetime.now(), d.id, q.id)
db_session.add(p)
db_session.commit()

r = Posting(datetime.datetime.now(), datetime.datetime.now(), d.id, q.id)
db_session.add(p)
db_session.commit()

print d.username
print d.geolocation
print d.posts

print p
print p.geolocation
print p.creation_time

print r
print r.geolocation
print r.creation_time



os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()

