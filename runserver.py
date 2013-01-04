from app_pkg import app

if __name__ == '__main__':
    # Bind to application variables if defined, otherwise they're None and 
    # local development server runs on http://127.0.0.1:5000
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))