# posts.py should provide a blueprint for generating post related pages.
# it's probably best if it's nested off of the dens blueprint
# https://flask.palletsprojects.com/en/2.0.x/blueprints/#nesting-blueprints
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bobchat.auth import login_required
from bobchat.db import get_db
from bobchat.dens import den_post

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

@bp.route('/create/<int:den_id>', methods=['POST', 'GET'])
@login_required
def create(den_id):
    den = get_db().execute('select * from dens where id = ?',(den_id,)).fetchone()
    if request.method == 'GET':
        return render_template('posts/create.html', den = den)
    else:
        title = request.form['title']
        body = request.form['body']
        get_db().execute('''
            insert into posts(author_id, den_id, title, body)
            values(?, ?, ?, ?)
        ''',(g.user['id'], den_id, title, body,))
        get_db().commit()
        return redirect(url_for('dens.den', den_id = den_id))

@bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):

    post = get_db().execute('select * from posts where id = ?',(post_id,)).fetchone()
    den = get_db().execute('select * from dens where id = ?',(post['den_id'],)).fetchone()
    if request.method == 'GET':
        return render_template('posts/update.html', post=post)
    else:
        try:
            request.form['delete']
            get_db().execute('pragma foreign_keys = on;')
            get_db().execute('delete from posts where id = ? and author_id = ?',(request.form['delete'], g.user['id']))
            get_db().commit()
        except KeyError:
            title = request.form['title']
            body = request.form['body']
            get_db().execute('''
                update posts
                set body = ?, title = ?
                where id = ?
                and author_id = ?
            ''',(body, title, post_id, g.user['id'],))
            get_db().commit()
        return redirect(url_for('dens.den', den_id = den['id']))