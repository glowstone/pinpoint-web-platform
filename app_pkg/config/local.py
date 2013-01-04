# Local Development Configuration File
import os

DEBUG = True
SECRET_KEY = 'local_development_secret'

# Custom Config Variables (not native to Flask)
# To allow only localhost to connect, '127.0.0.1', to allow any IP (on subnet), '0.0.0.0'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

# Database Settings
dialect = "mysql://"
host = "localhost"
database_name = "code_blue_db"
username = "dghubble"
password = "sample"
raw_connection_string = ""

if raw_connection_string:      # Raw Database Connection String Provided
	SQLALCHEMY_DATABASE_URI = raw_connection_string
else:                          # Construct Connection String
	SQLALCHEMY_DATABASE_URI = dialect + username + ":" + password + "@" + host + "/" + database_name