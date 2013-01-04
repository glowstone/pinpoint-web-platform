# Development Application Configuration
import os
from config_secrets import username, password, db_name

# dialect = "sqlite:////"
# db_name = "development.sqlite"

# SQLALCHEMY_DATABASE_URI = dialect + os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", db_name)

dialect = "mysql://"

# Username and password to be moved to a secret file. DB will have independent user management
#username = "tgarv"
#password = "lam63sot"	# This is a random password only used for sql.mit.edu, should probably store it somewhere else
# Eventually databse and host will be shared and centralized.
host = "sql.mit.edu"
#db_name = "tgarv+code_blue"           #Add this back once we just have one db
 
#SQLALCHEMY_DATABASE_URI = dialect + username + ":" + password + "@" + host + "/" + db_name
#print "SQLALCHEMY_DATABASE_URI: %s" % SQLALCHEMY_DATABASE_URI

# Eventually move this to a separate file
SECRET_KEY = 'development key'
DEBUG = True
