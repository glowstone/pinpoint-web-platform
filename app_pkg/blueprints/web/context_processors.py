from app_pkg import app

@app.context_processor
def external_keys():
	return dict(GOOGLE_API_KEY=app.config.get('GOOGLE_API_KEY'),)


@app.context_processor
def server_info():
	return dict(ROOT_ADDRESS=app.config.get('ROOT_ADDRESS'))
