import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# g is a special object that is unique for each request.
# It is used to store data that might be accessed by multiple
# functions during the request. The connection is stored and
# reused instead of creating a new connection if get_db is
# called a second time in the same request.

# current_app is another special object that points to the Flask
# application handling the request. Since we used an application
# factory, there is no application object when writing the rest of
# our code. get_db will be called when the application has been
# created and is handling a request, so current_app can be used.


# Returns a database connection, which is used to execute the commands read from the file.
def get_db():
    if 'db' not in g:
        # Establishes a connection to the file pointed at by the DATABASE configuration key.
        # This file doesn’t have to exist yet, and won’t until you initialize the database later.
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


# Checks if a connection was created by checking if g.db was set. If the connection exists, it is closed.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Running the SQL commands in 'schema.sql' to initialize the database.
def init_db():
    db = get_db()

    # Opens a file relative to the bobchat package,
    # which is useful since we won’t necessarily know
    # where that location is when deploying the application later.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# Defines a command line command called init-db that calls the init_db function and shows a success message to the user
# Also see: https://flask.palletsprojects.com/en/2.0.x/cli/
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# The close_db and init_db_command functions need to be registered with the application instance.
# Otherwise, they won’t be used by the application. However, since we're using a factory function,
# that instance isn’t available when writing the functions. Instead, write a function that takes
# an application and does the registration.
def init_app(app):
    # Tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)

    # Adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)
