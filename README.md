
# Code Blue Web Platform

# Versioning

Alpha. No compatability guarantees of any kind.

# Quickstart

    git clone git@github.com:dghubble/code-blue-web-platform.git
    cd code-blue-web-platform
    mkvirtualenv code-blue-env          # Virtualenv Wrapper
    workon code-blue-env
    pip install -r requirements.txt     # May require easy_install -U distribute


# Local MySQL Database Setup

## MySQL Installation

    sudo apt-get install mysql-server

When setting up the MySQL server, you will be prompted to create a password for the root user.

To secure the installation by removing anonymous users, disallowing remote root logins, removing test database, and reloading the privileges table run the following. You will be prompted for a root password.

    sudo mysql_secure_installation
    sudo apt-get install mysql-client

    mysql -u root -p
    CREATE USER username@localhost IDENTIFIED BY 'password';
    CREATE DATABASE codeblue_db;
    GRANT ALL PRIVILEGES ON codeblue_db.* TO username@localhost;

Fill out the Database Settings in app_pkg/config/development.py to correspond to your local setup.


# Environment Variables

In your virtualenvwrapper $WORKON_HOME, find the code-blue-env (or whatever you called the virtual environment) and edit <venv_name>/bin/postactivate 

    export APP_CONFIG=development
    export ROOT_ADDRESS=http://localhost:5000
    export GOOGLE_API_KEY=xxx

and <venv_name>/bin/postdeactivate

    unset APP_CONFIG
    unset ROOT_ADDRESS
    unset GOOGLE_API_KEY

Running 

    python setupdb.py                 # Re-create Model tables
    python bootstrapdb.py             # Initialize some data in the tables
    python runserver.py               # Run local server






