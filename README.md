flask-starter
=============

A batteries included boilerplate Flask project for getting new projects up and
running quickly.

Warning: This project is not under active development

Features and extensions include:

* Bootstrap 3
* SQLAlchemy database and automatic migrations using Flask-Alembic
* CoffeeScript and LESS compilation and bundling using Flask-Assets
* User management and logins using Flask-Security
* Admin interface using Flask-Superadmin with automatically generated CRUD
* REST API using Flask-Restful
* Email using Flask-Mail
* Better development mode using Flask-Failsafe
* Deployment helpers for nginx/uWSGI and upstart
* Basic management scripts using Flask-Scripts


Getting started
---------------

### Installing dependencies

You may want to initialize a virtualenv for your project:

    $ virtualenv venv
    $ source venv/bin/activate

First you must install the python package dependencies using PIP. By default
the project installs database drivers for PostgreSQL, you can change this and
add MySQL/SQLite if you like in requirements.txt

    $ pip install -r requirements.txt

Compilers for LESS and CoffeeScript require the Node.js packages. Install npm
from http://nodejs.org/ or using apt-get install npm. Once you have installed
NPM you can must install the compilers:

    $ npm install -g coffee-script
    $ npm install -g less


### Naming your project

Once you have installed the dependencies, call the init script to name your
project:

    $ python manage.py init <project_name>

You will need to configure your database settings and then perform the required
database initialization.

### Creating and connecting to your database

Database support is provided through Flask-SQLAlchemy. By default this is
configured to use PostgresQL. You can change this by using a different database
URL in config.py. You should update this to use the correct username and host
for your database. For example:

    SQLALCHEMY_DATABASE_URI = "postgresql://andrew@localhost/{}".format(PROJECT_NAME)

Before getting started you must create your database in PostgreSQL/MySQL

    $ psql
    $ create database <database-name>

Database migrations are handled by [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)

You will need to perform all three of these steps to create your database
before the first run.

First, have Flask-Migrate generate an alembic.ini

    $ python manage.py db init

To automatically generate a new revision:

    $ python manage.py db revision --autogenerate -m "message describing migration"

You should generate a migration every time you change the models so that the
database will be in sync with the models. To apply migrations you would want to
run:

    $ python manage.py db upgrade head

### Adding an admin user

Once you have initialized the database you should add yourself as an admin:

    $ python manage.py add_admin test@example.com password

This will allow you to view the admin interface at /admin once you have logged
in

### Customizing Flask-Security

All of the available Flask-Security templates have been included in the project.
They have been modified so that they extend from base templates so that you can
easily modify the look and feel of these pages and emails without editing each
one individually.

Emails extend from the security/mails/base.html and security/mails/base.txt
templates. User related pages extend from the security/base.html template
(which also extends from your standard project base template)


Deployment:
-----------

### Heroku:

To deploy to Heroku you will need to add the Node.js buildpack to your
application so that our LESS/Coffee assets can be compiled on the server.

    $ heroku buildpacks:set https://github.com/heroku/heroku-buildpack-python.git
    $ heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-nodejs.git

### uWSGI and nginx:

Deployment is done using uWSGI and nginx.

Install uWSGI and use the uwsgi.conf upstart script to start uWSGI with the
Emperor enabled. Link starter.ini into /etc/uwsgi/apps-enabled

The starter.conf is the simplest nginx script to serve the site, link this into
/etc/nginx/sites-enabled
