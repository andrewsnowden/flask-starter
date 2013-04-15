import os


class BaseConfig:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_NAME = "starter"

    DEBUG = True
    SECRET_KEY = "$2a$12$LdKsgm9HGNC6LzKVzJ48ju"

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

    SECURITY_PASSWORD_HASH = "bcrypt"

    SECURITY_PASSWORD_SALT = "$2a$12$sSoMBQ9V4hxNba5E0Xl3Fe"
    SECURITY_CONFIRM_SALT = "$2a$12$QyCM19UPUNLMq8n225V7qu"
    SECURITY_RESET_SALT = "$2a$12$GrrU0tYteKw45b5VfON5p."
    SECURITY_REMEMBER_SALT = "$2a$12$unlKF.sL4gnm4icbk0tvVe"


class ProductionConfig(BaseConfig):
    DEBUG = False

    ASSETS_MINIFY = True
    ASSETS_USE_CDN = True
