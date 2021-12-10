# The __init__.py serves double duty: it will contain the application factory,
# and it tells Python that the bobchat directory should be treated as a package.

import os

from flask import Flask

# TODO:: Implement Flask-Bootstrap to handle our webpage styling.
#           See: https://github.com/mbr/flask-bootstrap/blob/master/sample_app/__init__.py
#           also: https://www.youtube.com/watch?v=4nzI4RKwb5I
#           and: https://pythonhosted.org/Flask-Bootstrap/basic-usage.html

def create_app(test_config=None):
    # We are using the "Application Factory"-pattern here, which is described
    # in detail inside the Flask docs:
    # http://flask.pocoo.org/docs/patterns/appfactories/

    app = Flask(__name__, instance_relative_config=True)
    # __name__ is the name of the current Python module.
    # The app needs to know where it’s located to set up some paths,
    # and __name__ is a convenient way to tell it that.

    # instance_relative_config=True tells the app that configuration
    # files are relative to the instance folder. The instance folder
    # is located outside the bobchat package and can hold local data
    # that shouldn’t be committed to version control, such as configuration
    # secrets and the database file.
    # See: https://flask.palletsprojects.com/en/2.0.x/config/#instance-folders

    # SECRET_KEY is used by Flask and extensions to keep data safe.
    # It’s set to 'dev' to provide a convenient value during development,
    # but it should be overridden with a random value when deploying.
    # So, we try to get the SECRET_KEY from Heroku's environment variables.
    if (SECRET_KEY := os.getenv('FLASK_SECRET_KEY')) is None:
        SECRET_KEY = 'dev'

    # Here we add our configurations to the Flask app.
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,

        # DATABASE is the path where the SQLite database file will be saved.
        # It’s under app.instance_path, which is the path that Flask has chosen
        # for the instance folder.
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # Overrides the default configuration with values taken from the config.py
        # file in the instance folder if it exists.
        # When deploying, this is used to set a real SECRET_KEY.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        # This is so the tests can be configured independently of any
        # development values you have configured.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        # Flask doesn’t create the instance folder automatically,
        # but it needs to be created because the project will
        # create the SQLite database file there.
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    # TODO:: Change the main index page to user, where you can view all the dens you're apart of.
    from . import dens
    from . import posts
    app.register_blueprint(posts.bp)
    app.register_blueprint(dens.bp)
    # Unlike the auth blueprint, the den blueprint does not have a url_prefix.
    # So the index view will be at /, the create view at /create, and so on.

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    print(" * Using SECRET_KEY: " + app.config['SECRET_KEY'])

    return app
