# posts.py should provide a blueprint for generating post related pages.
# it's probably best if it's nested off of the dens blueprint
# https://flask.palletsprojects.com/en/2.0.x/blueprints/#nesting-blueprints
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bobchat.auth import login_required
from bobchat.db import get_db

bp = Blueprint('posts', __name__, url_prefix='/posts')

# route to delete a comment
# can only delete comments if you are the author
@bp.route('/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete(comment_id):
    author_id = get_db().execute('''
        select author_id
        from comments
        where id = ?
    ''',(comment_id,)).fetchone()

    if g.user['id'] != author_id['author_id']:
        abort(403)

    get_db().execute('''
        delete from comments
        where id = ?
    ''',(comment_id,))
    get_db().commit()

    den_id = request.form['den_id']
    post_id = request.form['post_id']
    return redirect(url_for('dens.den_post', den_id = den_id, post_id = post_id))
