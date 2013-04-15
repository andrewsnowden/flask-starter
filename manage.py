from flask.ext.script import Manager
from flask.ext.alembic import ManageMigrations
import os

from starter import app, db
from starter.users.models import user_datastore


manager = Manager(app)
manager.add_command("migrate", ManageMigrations())


@manager.command
def add_admin(email, password):
    user = user_datastore.create_user(email=email, password=password)

    admin_role = user_datastore.find_or_create_role("admin")
    user_datastore.add_role_to_user(user, admin_role)

    db.session.commit()
    print "Created admin user: %s" % (user, )


@manager.command
def init(name):
    print "Initializing flask-starter project with name '%s'" % (name, )

    module_name = "_".join(name.split()).lower()
    print "Python main module will be:", module_name

    module_files = ["manage.py", "dev.py", "shell.py", "starter/config.py"]

    for filename in module_files:
        print "Updating module name in '%s'" % (filename, )

        with open(filename) as f:
            lines = [l.replace("starter", module_name) for l in f.readlines()]

        with open(filename, 'w') as f:
            f.writelines(lines)

    print "Renaming 'starter' module to '%s'" % (module_name, )
    os.rename("starter", module_name)


if __name__ == "__main__":
    manager.run()
