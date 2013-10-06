from flask.ext.script import Manager
from flask.ext.alembic import ManageMigrations
import os
import datetime
import bcrypt
from flask.ext.security.utils import encrypt_password

from starter import app, db
from starter.users.models import user_datastore


manager = Manager(app)
manager.add_command("migrate", ManageMigrations())


@manager.command
def add_admin(email, password):
    """Add an admin user to your database"""
    user = user_datastore.create_user(email=email,
        password=encrypt_password(password))

    admin_role = user_datastore.find_or_create_role("admin")
    user_datastore.add_role_to_user(user, admin_role)
    user.confirmed_at = datetime.datetime.utcnow()

    db.session.commit()
    print "Created admin user: %s" % (user, )


@manager.command
def init(name, test=False, indent=""):
    """Initialize and rename a flask-starter project"""

    print "{0}Initializing flask-starter project with name '{1}'".format(
        indent, name)

    module_name = "_".join(name.split()).lower()
    print "{0}Python main module will be: {1}".format(indent, module_name)

    module_files = ["manage.py", "dev.py", "shell.py", "starter/config.py"]

    for filename in module_files:
        print "{0}Updating module name in '{1}'".format(indent, filename)

        if not test:
            with open(filename) as f:
                lines = [l.replace("starter", module_name) for l in f.readlines()]

            with open(filename, 'w') as f:
                f.writelines(lines)

    print '{0}Generating salts and secret keys'.format(indent)
    with open("starter/config.py") as f:
        lines = f.readlines()

    if not test:
        with open("starter/config.py", "w") as f:
            for line in lines:
                if "REPLACE_WITH_RANDOM" in line:
                    line = line.replace("REPLACE_WITH_RANDOM", bcrypt.gensalt())

                f.write(line)

    print "{0}Renaming 'starter' module to '{1}'".format(indent, module_name)
    if not test:
        os.rename("starter", module_name)

    print "{0}Finished initializing project".format(indent)


@manager.command
def wizard(test=False):
    """New project wizard to go through all required startup steps"""
    print 'Starting the flask-starter wizard'

    indent = ' ' * 4

    default_name = "starter"
    print '\n\nProject name:'
    name = raw_input("> Please enter a name for your project [{0}]: ".format(
        default_name))

    name = name or default_name
    init(name, test=test, indent=indent)

    if test:
        name = default_name

    config_file = "{0}/config.py".format(name)

    lines = []
    database_string = ""

    with open(config_file) as f:
        for line in f:
            if line.strip().startswith("SQLALCHEMY_DATABASE_URI"):
                parts = line.split("=", 1)
                uri = parts[1].strip()

                print '\n\nDatabase configuration:'
                print '*** NB Please ensure your database has been created'
                print ('Database string must be a valid python expression that'
                    ' will be understood by SQLAlchemy. Please include '
                    'surrounding quotes if this is just a static string')

                database_string = raw_input("> Please enter your database "
                    "connection string [{0}]: ".format(uri))

                database_string = database_string or uri

                parts[1] = " {0}\n".format(database_string)
                parts.insert(1, "=")
                lines.append("".join(parts))
            else:
                lines.append(line)

    print "{0}Writing database connection string: {1}".format(indent,
        database_string)

    if not test:
        with open(config_file, "w") as f:
            f.writelines(lines)

    print '{0}Initializing Alembic migrations'.format(indent)
    os.system("python manage.py migrate init")

    print '{0}Creating first revision'.format(indent)
    os.system('python manage.py migrate revision --autogenerate -m '
        '"Initial database migration"')

    print "{0}Upgrading database to head".format(indent)
    os.system("python manage.py migrate upgrade head")

    print "\n\nCreate admin user"
    email = raw_input("> Please enter an admin email address: ")
    password = raw_input("> Please enter an admin password: ")
    add_admin(email, password)


if __name__ == "__main__":
    manager.run()
