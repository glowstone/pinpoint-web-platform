from flask import render_template
from web_package import app

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/hello')
def hello():
	return 'hello, world'