# Deployment Configuration File
import os

DEBUG = False
SECRET_KEY = os.urandom(24)

# Custom Config Variables (not native to Flask)
HOST = os.environ.get('HOST', '0.0.0.0')   # Flask HTTP Server requires 0.0.0.0 on Heroku
PORT = int(os.environ.get('PORT', 5000))   # Heroku server sets desired PORT

# Database
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

