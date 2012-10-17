from web_package import db_session
from web_package.models import *
import os
import sys

os.system('clear')
sys.ps1 = "cool>>"

e = Engineer('python')
db_session.add(e)
db_session.commit()
print e.primary_language
print e.person_id

n = Nobody('lame')
db_session.add(n)
db_session.commit()
print n.name
print n.person_id


os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()

