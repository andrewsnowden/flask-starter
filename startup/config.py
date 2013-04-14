import os


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_NAME = "starter"

    DEBUG = True
    SECRET_KEY = ""

    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/%s" % (PROJECT_NAME, )

    if os.name == "nt":
        LESS_BIN = "lessc.cmd"
        COFFEE_BIN = "coffee.cmd"

    # Debug
    ASSETS_MINIFY = False
    ASSETS_USE_CDN = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'test@gmail.com'
    MAIL_PASSWORD = ''

    DEFAULT_MAIL_SENDER = ("Flask-Starter", "test@gmail.com")

    # Flask-Security Flags
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True


class ProductionConfig(BaseConfig):
    DEBUG = False

    ASSETS_MINIFY = True
    ASSETS_USE_CDN = True
