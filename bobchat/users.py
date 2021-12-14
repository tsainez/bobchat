#
#   users.py
#       Handles the rendering for all user-page related content.
#

# Define the blueprint and register it in the application factory.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bobchat.db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')


# The index will show the most recent posts.
# A JOIN is used so that the author information from the user table is available in the result.
@bp.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()
    if request.method == 'POST':
        users = db.execute(
            '''
            select *
            from users
            where username like ?;
            ''',('%'+request.form['search']+'%',)
        ).fetchall()
    else:
        users = db.execute(
            '''
            select *
            from users;
            '''
        ).fetchall()
    return render_template('users/index.html', users=users)

@bp.route('/<username>')
def user_page(username):
    print(str(username))
    db = get_db()
    user = db.execute(
        '''
        select *
        from users
        where username = ?
        ''',(username,)
    ).fetchone()
    author_id = user['id']
    posts = db.execute(
        '''
        SELECT 
            posts.id,
            posts.den_id,
            posts.created,
            posts.title,
            dens.name as den_name,
            IFNULL(post.likes, 0) AS likes
        FROM dens, posts
            LEFT JOIN (
                SELECT post_id, COUNT(*) AS likes
                FROM post_like_assoc, posts
                WHERE posts.id = post_like_assoc.post_id
                GROUP BY post_like_assoc.post_id
            ) AS post ON post_id = posts.id
        WHERE posts.author_id = ?
        and posts.den_id = dens.id
        ORDER BY likes DESC;
        ''',(author_id,)
    ).fetchall()
    return render_template('users/user_page.html', user = user, posts = posts)