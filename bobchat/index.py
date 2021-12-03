# Define the blueprint and register it in the application factory.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
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
    if g.user is None:
        # We want the 5 most recent posts...
        posts = db.execute('''
        SELECT users.username,
            dens.name,
            posts.*
        FROM posts,
            users,
            dens
        WHERE users.id = posts.author_id
            AND dens.id = den_id
        ORDER BY created DESC
        LIMIT 5;
        ''').fetchall()

        # And also some site data to display in the about section...
        site_data = db.execute('''
        SELECT COUNT(DISTINCT users.id) AS users,
            COUNT(DISTINCT posts.id) AS posts
        FROM users,
            posts;
        ''').fetchone()
        return render_template('home.html', posts=posts, site_data=site_data)
    else:
        posts = db.execute('''
        SELECT users.username,
            dens.name,
            posts.*
        FROM posts,
            users,
            dens
        WHERE den_id IN (
                SELECT den_id
                FROM user_den_assoc
                WHERE user_id = 1
            )
            AND users.id = posts.author_id
            AND dens.id = den_id
        ORDER BY created DESC;
        ''').fetchall()
        return render_template('feed.html', posts=posts)
        # return render_template('users/feed.html', posts = posts)
