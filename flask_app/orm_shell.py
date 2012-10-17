from web_package import db_session
from web_package.models import *
import os
import sys

os.system('clear')
sys.ps1 = "cool>>"

e = Engineer('python')            #Named Ben
db_session.add(e)
db_session.commit()
print e.primary_language
print e.name
print e.id
print e.engineer_id

n = Nobody('some-string')
db_session.add(n)
db_session.commit()
print n.prop
print n.name
print n.type


os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()

