from web_package import db_session
from web_package.models import *
import os
import sys

os.system('clear')
sys.ps1 = "cool>>"

u = User('admin', 'sample')
db_session.add(u)
db_session.commit()
User.query.all()


#os.environ['PYTHONINSPECT'] = 'True'

#u = User('dalton', 'dsadsadasd', 'dsadsaada', None)
#db.session.add(u)
#db.session.commit()

