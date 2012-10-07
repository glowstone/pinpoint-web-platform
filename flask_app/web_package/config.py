# Flask Application Configuration
import os

dialect = "sqlite:////"
SQLALCHEMY_DATABASE_URI = dialect + os.path.join(os.path.dirname(__file__), "db", "development.sqlite")

# Eventually move this to a separate file
SECRET_KEY = 'development key'
DEBUG = True
