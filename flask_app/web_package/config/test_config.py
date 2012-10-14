# Testing Application Configuration
import os


dialect = "sqlite:////"
db_name = "testing.sqlite"
SQLALCHEMY_DATABASE_URI = dialect + os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", db_name)

SECRET_KEY = 'testing key'
TESTING = True
DEBUG = True
