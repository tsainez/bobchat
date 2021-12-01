from flask import Flask
from numpy import append
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# For manipulating the CSVs.
import pandas as pd

# For looking at all the tables in a database.
from sqlalchemy import inspect

# For debugging purposes.
import time

# Now, handle the Flask object relational mapping (ORM).
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Required by Flask in order to run.
app.config['SECRET_KEY'] = 'Super Secret Key'

# SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# We need to create the database schema in Flask-SQLAlchemy in order to utilize the ORM.
db = SQLAlchemy(app)

# We create an engine object in order to execute raw SQL statements.
# For more information on the engine object, see the following links:
#     https://docs.sqlalchemy.org/en/13/core/engines.html
#     https://docs.sqlalchemy.org/en/13/core/connections.html
engine = db.engine

# Data Definition Language (DDL) is as follows:


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)


class Dens(db.Model):
    __tablename__ = 'dens'
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128), nullable=False)


class Users_And_Dens(db.Model):
    __tablename__ = 'users_and_dens'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, primary_key=False)
    den_id = db.Column(db.Integer, nullable=False, primary_key=False)


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    content = db.Column(db.String(4096), nullable=False)
    time = db.Column(db.Date, nullable=False)
    den_id = db.Column(db.Integer, nullable=False)


# Checking if the database has tables.
inspector = inspect(engine)
tables = inspector.get_table_names()
if not (tables):
    # There are no tables in the database.
    db.create_all()
    db.session.commit()
    print("Creating database schema...")
del inspector

# TODO:: See if there's a better way to "refresh" this inspector instead of deleting and recreating it.
# Might have something to do with sessions? https://stackoverflow.com/questions/70177674/refreshing-the-inspector-in-sqlalchemy

# Checking if the tables are populated.
with engine.connect() as connection:
    # Iterating through all the tables in the database...
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    for table_name in tables:
        start_time = time.time()
        result = connection.execute(
            "SELECT COUNT(*) FROM {}".format(table_name))
        for row in result:
            if row[0] == 0:
                # This table has zero rows, so we insert data from
                # a CSV with the same name as the table.
                try:
                    print("\t'{}' table is empty.".format(table_name))
                    df = pd.read_csv(
                        "./csv/{}.csv".format(table_name), header=0)
                    for index, row in df.iterrows():
                        df.to_sql(table_name, engine, index=False,
                                  if_exists="replace", method="multi")
                except FileNotFoundError:
                    print(
                        "\tERROR: There is no CSV to populate '{}'!\n".format(table_name))
                    continue
            print("\t'{}' filled.\n\t{} seconds elapsed.\n".format(
                table_name, (time.time() - start_time)))
    del inspector
