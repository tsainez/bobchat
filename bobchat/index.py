# Define the blueprint and register it in the application factory.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from bobchat.auth import login_required
from bobchat.db import get_db

bp = Blueprint('index', __name__)


# This is the index or home page for the website.
# If they aren't logged in, they will be shown a homepage, otherwise show their feed
# A JOIN is used so that the author information from the user table is available in the result.
@bp.route('/')
def index():
    db = get_db()

    # Whether or not the user is logged in, we want to show the 5 most recently made posts...
    recent_posts = db.execute('''
        SELECT users.username,
            dens.name,
            dens.id as den_id,
            posts.id as post_id,
            posts.created,
            posts.body,
            posts.title
        FROM posts,
            users,
            dens
        WHERE users.id = posts.author_id
            AND dens.id = den_id
        ORDER BY posts.created DESC
        LIMIT 5;
        ''').fetchall()
    if g.user is None:
        # Some extra data about the site for displaying on the home page.
        site_data = db.execute('''
        SELECT COUNT(DISTINCT users.id) AS users,
            COUNT(DISTINCT posts.id) AS posts
        FROM users,
            posts;
        ''').fetchone()

        return render_template('index/home.html', posts=recent_posts, site_data=site_data)
    else:
        # SQL operations usually need to use values from Python variables.
        # However, beware of using Python’s string operations to assemble queries,
        # as they are vulnerable to SQL injection attacks.
        # Instead, use the DB-API’s parameter substitution.
        # See: https://docs.python.org/3/library/sqlite3.html
        posts = db.execute('''
        SELECT users.username,
            dens.name,
            dens.id as den_id,
            posts.id as post_id,
            posts.created,
            posts.body,
            posts.title
        FROM posts,
            users,
            dens
        WHERE den_id IN (
                SELECT den_id
                FROM user_den_assoc
                WHERE user_id = {}
            )
            AND users.id = posts.author_id
            AND dens.id = den_id
        ORDER BY posts.created DESC;'''.format(session.get('user_id'))).fetchall()
        return render_template('index/feed.html', posts=posts, recents=recent_posts)
