from web_package import db_session
from web_package.models import *
import os
import sys

os.system('clear')
sys.ps1 = "cool>>"


g = Geolocation(5,6,7)
db_session.add(g)
db_session.commit()

e = Engineer('python', g.id)            #Named Ben
db_session.add(e)
db_session.commit()
print e.primary_language
print e.id
print e.engineer_id

print g.person
print e.geolocation

n = Nobody('some-string', g.id)       # try to associate multiple geolocations with 2 Pinnable Objects
db_session.add(n)
db_session.commit()

print n.prop
print n.type
print n.geolocation
print e.geolocation
print g.person


os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()

