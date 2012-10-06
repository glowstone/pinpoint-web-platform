from flask import Flask, g
from contextlib import closing
import sqlite3
#import sqlite3

#App configuration will go here.
#DATABASE = "db/code_blue.db"
app = Flask(__name__)
app.config.from_object('web_package.config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

# To prevent circular dependency problems, import views at the end and do not use the views inside __init__.py.
from web_package import routes