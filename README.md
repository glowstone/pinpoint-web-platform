
# Code Blue Web Platform

# Versioning

Alpha. No compatability guarantees of any kind.

# Quickstart

    git clone git@github.com:dghubble/code-blue-web-platform.git
    cd code-blue-web-platform
    virtualenv blue-env --distribute
    source blue-env/bin/activate
    pip install -r requirements.txt
    export APP_CONFIG_FILE=config/local.py
    python setupdb.py                 # Re-create Model tables
    python bootstrapdb.py             # Initialize some data in the tables
    python runserver.py               # Run local server

# Local MySQL Database Setup

    mysql -u root -p
    CREATE USER username@localhost IDENTIFIED BY 'password';
    CREATE DATABASE code_blue_db;
    GRANT ALL PRIVILEGES ON code_blue_db.* TO username@localhost;

Fill out the Database Settings in app_pkg/config/local.py to correspond to your local setup.

# MySQL Installation

    sudo apt-get install mysql-server

When setting up the MySQL server, you will be prompted to create a password for the root user.

To secure the installation by removing anonymous users, disallowing remote root logins, removing test database, and reloading the privileges table run the following. You will be prompted for a root password.

    sudo mysql_secure_installation
    sudo apt-get install mysql-client



