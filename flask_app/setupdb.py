from contextlib import closing
import sqlite3
from web_package import app

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with open('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()



if __name__ == '__main__':
    init_db()
