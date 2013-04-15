from .. import app, db, api
from flask.ext import security
import pytz

# Define models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, security.RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, security.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(32))
    current_login_ip = db.Column(db.String(32))
    login_count = db.Column(db.Integer())
    timezone = db.Column(db.String(64))

    def get_tz(self):
        if self.timezone:
            return pytz.timezone(self.timezone)
        else:
            return app.config.get("DEFAULT_TIMEZONE", pytz.utc)

    def dict(self):
        """
        A dictionary representation that can be used for JSON serialization
        """
        return {
            "email": self.email,
            "active": self.active,
            "confirmed_at": api.serialize_date(self.confirmed_at),
            "timezone": self.timezone
        }

    def __str__(self):
        return "User(%s)" % (self.email, )

# Setup Flask-Security
user_datastore = security.SQLAlchemyUserDatastore(db, User, Role)
app.security = security.Security(app, user_datastore)
