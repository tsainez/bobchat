#
#   auth.py
#       A blueprint that handles all pages dealing with user authentication, as well as
#       provides a few helper functions and a decorator function that are used in
#       other blueprints where verifying users is important.
#

# A Blueprint is a way to organize a group of related views and other code.
# Rather than registering views and other code directly with an application,
# they are registered with a blueprint. Then the blueprint is registered with
# the application when it is available in the factory function.

# This creates a Blueprint named 'auth'. Like the application object, the blueprint
# needs to know where it’s defined, so __name__ is passed as the second argument.
# The url_prefix will be prepended to all the URLs associated with the blueprint.

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bobchat.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# When the user visits the /auth/register URL, the register view will return HTML
# with a form for them to fill out. When they submit the form, it will validate
# their input and either show the form again with an error message or create the
# new user and go to the login page.


# @bp.route associates the URL /register with the register view function.
# When Flask receives a request to /auth/register, it will call the register view
# and use the return value as the response.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # If the user submitted the form, request.method will be 'POST'.
    # In this case, start validating the input.
    if request.method == 'POST':
        # request.form is a special type of dict mapping submitted
        # form keys and values. The user will input their username and password.
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        major = request.form['major']

        db = get_db()
        error = None

        # Validate that username and password are not empty.
        # redundant check in register.html form (required attribute on <input> tags)
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # If validation succeeds, insert the new user data into the database.
        if error is None:
            try:
                # db.execute takes a SQL query with ? placeholders for any user input,
                # and a tuple of values to replace the placeholders with. The database
                # library will take care of escaping the values so you are not vulnerable
                # to a SQL injection attack.
                db.execute(
                    "INSERT INTO users (username, password, firstname, lastname, email, major) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password),
                     firstname, lastname, email, major),
                )
                # For security, passwords should never be stored in the database directly.
                # Instead, generate_password_hash() is used to securely hash the password,
                # and that hash is stored. Since this query modifies data, db.commit()
                # needs to be called afterwards to save the changes.
                db.commit()
            except db.IntegrityError:
                # An sqlite3.IntegrityError will occur if the username already exists,
                # which should be shown to the user as another validation error.
                error = f"User {username} is already registered."
            else:
                # After storing the user, they are redirected to the login page.
                # url_for() generates the URL for the login view based on its name.
                # This is preferable to writing the URL directly as it allows you to
                # change the URL later without changing all code that links to it.
                # redirect() generates a redirect response to the generated URL.
                return redirect(url_for("auth.login"))

        # If validation fails, the error is shown to the user.
        # flash() stores messages that can be retrieved when rendering the template.
        flash(error)

    # When the user initially navigates to auth/register, or there was a validation error,
    # an HTML page with the registration form should be shown. render_template() will render
    # a template containing the HTML.
    return render_template('auth/register.html')


# This view follows the same pattern as the register view above.
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        # The user is queried first and stored in a variable for later use.
        # fetchone() returns one row from the query. If the query returned no results, it returns None.
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        # check_password_hash() hashes the submitted password in the same way as the stored hash
        # and securely compares them. If they match, the password is valid.
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # 'session' is a dict that stores data across requests.
        # When validation succeeds, the user’s id is stored in a new session.
        # The data is stored in a cookie that is sent to the browser,
        # and the browser then sends it back with subsequent requests.
        if error is None:
            session.clear()
            session['user_id'] = user['id']

            # Now that the user’s id is stored in the session, it will be available on subsequent requests.
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    # load_logged_in_user checks if a user id is stored in the session
    # and gets that user’s data from the database, storing it on g.user,
    # which lasts for the length of the request.
    user_id = session.get('user_id')

    # If there is no user id, or if the id doesn’t exist, g.user will be None.
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


# To log out, we need to remove the user id from the session.
# Then load_logged_in_user won’t load a user on subsequent requests.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Creating, editing, and deleting den posts will require a user to be logged in.
# A decorator can be used to check this for each view it’s applied to.
# For more information, see: https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/
def login_required(view):
    # This decorator returns a new view function that wraps the original view it’s applied to.
    # The new function checks if a user is loaded and redirects to the login page otherwise.
    # If a user is loaded the original view is called and continues normally. You’ll use this decorator when writing the blog views.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # The url_for() function generates the URL to a view based on a name and arguments.
            # The name associated with a view is also called the endpoint,
            # and by default it’s the same as the name of the view function.

            # When using a blueprint, the name of the blueprint is prepended to the name of the function,
            # so the endpoint for the login function written above is 'auth.login' because it is a part of the 'auth' blueprint.
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
