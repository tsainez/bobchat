import sqlite3
from sqlite3 import Error
from typing import Type

import click
from flask import current_app, g
from flask.cli import with_appcontext

import pandas as pd
import os

from werkzeug.security import generate_password_hash

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

        # Tells the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


# Checks if a connection was created by checking if g.db was set. If the connection exists, it is closed.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Running the SQL commands in 'schema.sql' to initialize the database.
# This function also populates the tables with default data.
def init_db():
    print("Verifying database integrity...\n")
    db = get_db()

    # Testing to see if any tables exist in the schema table
    # See: https://www.sqlite.org/schematab.html
    if db.cursor().execute("SELECT name FROM sqlite_master").fetchone() is not None:
        print("\tWARNING: You already have a database initialized.")
        print("\t         Are you certain you want to overwrite it?\n")
        yn = input("\ty/n: ")
        print()
        if yn != "y":
            return -1

    # Opens a file relative to the bobchat package,
    # which is useful since we won’t necessarily know
    # where that location is when deploying the application later.
    with current_app.open_resource('schema.sql') as f:
        try:
            db.executescript(f.read().decode('utf8'))
        except Error as e:
            print("\tERROR: " + str(e) + "\n")
            return -1

    # Attempt to populate all the tables with default data.
    for file_name in os.listdir('bobchat/csv'):
        table_name = file_name[:-4]  # Removing '.csv' from the file_name

        if pd.io.sql.has_table(table_name, db):
            try:
                df = pd.read_csv(
                    'bobchat/csv/{}'.format(file_name), index_col=0)
                df.to_sql('{}'.format(table_name), db, if_exists='append')
                print("\tSUCCESS: filled table {}\n".format(table_name))
            except Error as e:
                print("\tERROR: " + str(e) + "\n")
        else:
            # We are not handling creating the schema here. We do that in schema.sql.
            print(
                "\tWARNING: table {} does not exist in the schema.\n".format(table_name))

    # For the users table specifically, we need to salt and hash their passwords.
    if pd.io.sql.has_table('users', db):
        print("\tSalting and hashing passwords...\n")
        users_df = pd.read_csv(
            'bobchat/csv/users.csv', index_col=0)
        i = 1
        for row in users_df.itertuples():
            print('\r\t\t', str(i), end='')
            print(" updated.", end='')
            try:
                db.execute(
                    '''UPDATE users
                        SET password = ?
                        WHERE id = ?;''',
                    (generate_password_hash(row[2]), row[0]),
                )
                db.commit()
                i += 1
            except Error as e:
                print(e)
        print('\n')


# Defines a command line command called init-db that calls the init_db function and shows a success message to the user
# Also see: https://flask.palletsprojects.com/en/2.0.x/cli/
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    if init_db() == -1:
        click.echo('Failed to initialize database.')
    else:
        click.echo('Database initialized.')


# Defines a command line command called test-sql, used for testing purposes.
@click.command('test-sql')
@with_appcontext
def test_sql_command():
    """Quick and dirty testing SQL statements on the database."""
    db = get_db()
    cur = db.cursor()
    cur.execute('''SELECT * FROM users''')
    print(cur.fetchall())


# The close_db and init_db_command functions need to be registered with the application instance.
# Otherwise, they won’t be used by the application. However, since we're using a factory function,
# that instance isn’t available when writing the functions. Instead, write a function that takes
# an application and does the registration.
def init_app(app):
    # Tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)

    # Add commands that can be called with the flask command.
    app.cli.add_command(init_db_command)
    app.cli.add_command(test_sql_command)
