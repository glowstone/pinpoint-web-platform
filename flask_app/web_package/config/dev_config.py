# Development Application Configuration
import os

dialect = "sqlite:////"
db_name = "development.sqlite"

SQLALCHEMY_DATABASE_URI = dialect + os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", db_name)

# Eventually move this to a separate file
SECRET_KEY = 'development key'
DEBUG = True
