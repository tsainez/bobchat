#
#   posts.py
#       Handles post-specific operations, such as adding and deleting comments...
#

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bobchat.auth import login_required
from bobchat.db import get_db
from bobchat.dens import den_post

#
# TODO: It would be nice if we could nest this blueprint off of the dens blueprint.
#       see: https://flask.palletsprojects.com/en/2.0.x/blueprints/#nesting-blueprints
#

bp = Blueprint('posts', __name__, url_prefix='/posts')


# Route to delete a comment — only accessible if you are the author
@bp.route('/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete(comment_id):
    db = get_db()

    author_id = db.execute('''
        SELECT author_id
        FROM comments
        WHERE id = ?
    ''', (comment_id,)).fetchone()

    if g.user['id'] != author_id['author_id']:
        abort(403)

    db.execute('''
        DELETE FROM comments
        WHERE id = ?
    ''', (comment_id,))
    db.commit()

    den_id = request.form['den_id']
    post_id = request.form['post_id']

    return redirect(url_for('dens.den_post', den_id=den_id, post_id=post_id))


# Route for creating a post in a den with den_id
@bp.route('/create/<int:den_id>', methods=['POST', 'GET'])
@login_required
def create(den_id):
    db = get_db()
    den = db.execute('''SELECT *
                        FROM dens
                        WHERE id= ?''', (den_id,)).fetchone()

    if request.method == 'GET':
        return render_template('posts/create.html', den=den)
    else:
        title = request.form['title']
        body = request.form['body']
        db.execute('''
            INSERT INTO posts(author_id, den_id, title, body)
            VALUES(?, ?, ?, ?)
        ''', (g.user['id'], den_id, title, body,))
        db.commit()
        return redirect(url_for('dens.den', den_id=den_id))


# Route for updating a post with specific post_id
@bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?',
                      (post_id,)).fetchone()
    den = db.execute('SELECT * FROM dens WHERE id = ?',
                     (post['den_id'],)).fetchone()

    if request.method == 'GET':
        return render_template('posts/update.html', post=post)
    else:
        try:
            request.form['delete']
            db.execute('pragma foreign_keys = on;')
            db.execute('DELETE FROM posts WHERE id = ? AND author_id = ?',
                       (request.form['delete'], g.user['id']))
            db.commit()
        except KeyError:
            title = request.form['title']
            body = request.form['body']
            db.execute('''
                UPDATE posts
                SET body = ?, title = ?
                WHERE id = ?
                AND author_id = ?
            ''', (body, title, post_id, g.user['id'],))
            db.commit()
        return redirect(url_for('dens.den', den_id=den['id']))
