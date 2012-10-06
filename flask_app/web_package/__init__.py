from flask import Flask
import sqlite3

#App configuration will go here.
DATABASE = "db/code_blue.db"
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# To prevent circular dependency problems, import views at the end and do not use the views inside __init__.py.
from web_package import views