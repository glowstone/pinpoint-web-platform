from flask_app import app
from flask import render_template

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/hello')
def hello():
	return 'hello, world'