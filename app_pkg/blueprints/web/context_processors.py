from app_pkg import app

@app.context_processor
def external_keys():
	"""Provides web templates with client side oauth access keys."""
	return dict(GOOGLE_API_KEY=app.config.get('GOOGLE_API_KEY'),)


@app.context_processor
def server_info():
	"""Provides web templates with basic server information"""
	return dict(ROOT_ADDRESS=app.config.get('ROOT_ADDRESS'))
