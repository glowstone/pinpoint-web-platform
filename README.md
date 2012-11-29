
Code Blue Web Platform
======================


Versioning
==========

Alpha. No compatability guarantees of any kind.

Getting Started
===============

Local Setup
-----------

    sudo apt-get install build-essential
    sudo apt-get install python-dev
    sudo easy_install -U distribute
    sudo apt-get install libmysqlclient-dev      # Needed for MySQL-python PyPI package

    git clone git@github.com:dghubble/code-blue-web-platform.git
    cd code-blue-web-platform
    virtualenv blue-env --distribute
    source blue-env/bin/activate
    pip install -r pip-env-reqs.txt

Minimal Configuration
---------------------

In the web_package/config Python package, include a config_secrets.py module as follows:

    username = ""
    password = ""
    db_name = ""

Local Testing
-------------

    source blue-env/bin/activate
    cd flask_app
    python setupdb.py               # Initialize the SQL Tables
    python runserver.py             # Run web app at localhost:5000

