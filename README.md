flask-starter
=============

A boilerplate Flask project, features and included extensions include:

* SQLAlchemy database and automatic migrations using Flask-Alembic
* CoffeeScript and LESS compilation and bundling using Flask-Assets
* User management and logins using Flask-Security
* Email using Flask-Mail
* Better development mode using Flask-Failsafe
* Deployment helpers for nginx/uWSGI and upstart
* Admin interface using Flask-Admin with automatically generated CRUD
* Basic management scripts using Flask-Scripts


Installing dependencies
-----------------------

PIP Requirements:

    $ pip install -r requirements.txt

Web assets:

There is a bug in flask-assets that doesn't recompile LESS files, you have to
install the dev version until these are packaged properly for PyPI:

    $ easy_install http://github.com/miracle2k/flask-assets/tarball/master
    $ easy_install http://github.com/miracle2k/webassets/tarball/master

Compilers for LESS and CoffeeScript require the Node.js packages. Install npm
from http://nodejs.org/ or using apt-get install npm.

    $ npm install -g coffee-script
    $ npm install -g less

Getting started
---------------

### Naming your project

To get started, just clone the project and run the init script to rename your project:

    $ python manage.py init <project_name>

You will need to configure your database settings and then perform the required database initialization.

### Creating your database

Database migrations are handled by [Flask-Alembic](https://github.com/tobiasandtobias/flask-alembic)

You will need to perform all three of these steps to create your database before the first run.

First, have Flask-Alembic generate an alembic.ini

    $ python manage.py migrate init

To automatically generate a new revision:

    $  python manage.py migrate revision --autogenerate -m "message describing migration"

You should generate a migration every time you change the models so that the
database will be in sync with the models. To apply migrations you would want to
run:

    $ python manage.py migrate upgrade head

### Adding an admin user

Once you have initialized the database you should add yourself as an admin:

    $ python manage.py add_admin test@example.com password

This will allow you to view the admin interface at /admin once you have logged in


Deployment:
-----------

Deployment is done using uWSGI and nginx.

Install uWSGI and use the uwsgi.conf upstart script to start uWSGI with the
Emperor enabled. Link starter.ini into /etc/uwsgi/apps-enabled

The starter.conf is the simplest nginx script to serve the site, link this into
/etc/nginx/sites-enabled