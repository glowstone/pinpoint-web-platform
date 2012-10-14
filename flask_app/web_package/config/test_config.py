# Development Application Configuration
import os

dialect = "sqlite:////"
SQLALCHEMY_DATABASE_URI = dialect + os.path.join(os.path.dirname(__file__), "db", "testing.sqlite")

# Eventually move this to a separate file
SECRET_KEY = 'testing key'
TESTING = True
DEBUG = True
