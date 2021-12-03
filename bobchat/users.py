# Define the blueprint and register it in the application factory.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bobchat.auth import login_required
from bobchat.db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')


# The index will show the most recent posts.
# A JOIN is used so that the author information from the user table is available in the result.
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute('''
    SELECT p.id,
        title,
        body,
        created,
        author_id,
        username
    FROM posts p
        JOIN users u ON p.author_id = u.id
    ORDER BY created DESC
    LIMIT 10;
    ''').fetchall()
    return render_template('den/index.html', posts=posts)
