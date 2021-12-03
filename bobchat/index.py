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
    if g.user is None:
        return render_template('bobchat.html')
    else:
        db = get_db()
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
