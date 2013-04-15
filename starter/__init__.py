import flask
from flask.ext import sqlalchemy
from flask.ext import bootstrap
from flask.ext import assets as webassets
from flask.ext.mail import Mail, Message
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user

from werkzeug.contrib.fixers import ProxyFix

import logging
import os
import os.path

from .config import BaseConfig
from .utils.api import Api

# Expose API constructs through this module
app = flask.Flask(BaseConfig.PROJECT_NAME)
app.config.from_object(BaseConfig)

app.wsgi_app = ProxyFix(app.wsgi_app)

# Flask Extensions
bootstrap.Bootstrap(app)
mail = Mail(app)

# Database
db = sqlalchemy.SQLAlchemy(app)

# An API
api = Api(app, prefix="/api/v1")

# Asset bundles
assets = webassets.Environment(app)

# Coffee Scripts
scripts_path = os.path.abspath(os.path.join(app.config["BASEDIR"],
    "static/scripts"))

coffee_scripts = ["scripts/%s" % (f, )
        for f in os.listdir(scripts_path) if f.endswith(".coffee")]

assets.register("coffee_scripts", webassets.Bundle(*coffee_scripts,
                filters=("coffeescript,rjsmin" if app.config["ASSETS_MINIFY"]
                    else "coffeescript"),
                output="scripts/generated.js"))

# Less stylesheets
styles_path = os.path.abspath(os.path.join(app.config["BASEDIR"],
    "static/styles"))

less_stylesheets = ["styles/%s" % (f, )
        for f in os.listdir(styles_path) if f.endswith(".less")]

assets.register("less_stylesheets", webassets.Bundle(*less_stylesheets,
                filters=("less,cssmin" if app.config["ASSETS_MINIFY"]
                    else "less"),
                output="styles/generated.css"))


# Sending templated emails
def send_mail(destination, subject, template, **template_kwargs):
    text = flask.render_template("{0}.txt".format(template), **template_kwargs)

    logging.info("Sending email to {0}. Body is: {1}".format(
        destination, repr(text)[:50]))

    msg = Message(
        subject,
        recipients=[destination]
    )

    msg.body = text
    msg.html = flask.render_template("{0}.html".format(template),
            **template_kwargs)

    mail.send(msg)


# Admin interface
class SecuredAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role("admin")


class SecuredModelView(ModelView):
    def is_accessible(self):
        return current_user.has_role("admin")

admin = Admin(app, "Auth", index_view=SecuredAdminIndexView())


if app.config.get("AUTOGENERATE_MODEL_ADMIN", True):
    # We have to hook in to the db.Model metaclass to keep track of any table
    # classes we define
    class _AdminBoundDeclarativeMeta(sqlalchemy._BoundDeclarativeMeta):
        def __init__(self, name, bases, d):
            super(self.__class__, self).__init__(name, bases, d)
            if name != "Model":
                admin.add_view(SecuredModelView(self, db.session,
                    category="CRUD"))

    db.Model = sqlalchemy.declarative_base(cls=sqlalchemy.Model,
        name="Model", mapper=sqlalchemy.signalling_mapper,
        metaclass=_AdminBoundDeclarativeMeta)
    db.Model.query = sqlalchemy._QueryProperty(db)


# Automatically include views, files and APIs
include_files = set(["views.py", "models.py", "api.py"])

for root, dirname, files in os.walk(app.config["BASEDIR"]):
    for filename in files:
        if filename in include_files:
            relative = os.path.relpath(os.path.join(root, filename))[:-3]
            module = ".".join(relative.split(os.sep))
            __import__(module, level=-1)
