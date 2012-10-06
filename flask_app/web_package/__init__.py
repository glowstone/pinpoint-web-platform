from flask import Flask
from contextlib import closing
import sqlite3

#App configuration will go here.
DATABASE = "db/code_blue.db"
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


def init_db():
	with closing(connect_db()) as db:
		with open('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

# To prevent circular dependency problems, import views at the end and do not use the views inside __init__.py.
from web_package import views