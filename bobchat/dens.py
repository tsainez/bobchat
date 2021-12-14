#
#   dens.py
#       Handles the main use-cases for our program.
#

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bobchat.auth import login_required
from bobchat.db import get_db
bp = Blueprint('dens', __name__, url_prefix='/dens')


# The index will show all the dens available, which you can click on to view a den in more detail.
# A JOIN is used so that the author information from the user table is available in the result.
@bp.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()
    if request.method == 'POST' and request.form['search'] != '':
        # print('user is looking for: {}'.format(request.form['search']))
        results = db.execute('''
            SELECT name,
            username,
            d.created,
            description,
            d.id
            FROM dens d
            JOIN users u ON d.author_id = u.id
            where d.name like '%{}%'
            ORDER BY d.created DESC;
        '''.format(request.form['search'])).fetchall()
    else:
        results = db.execute('''
        SELECT name,
            username,
            d.created,
            description,
            d.id
        FROM dens d
            JOIN users u ON d.author_id = u.id
        ORDER BY d.created DESC;
        ''').fetchall()
    return render_template('dens/index.html', dens=results)


# The create view works the same as the auth register view.
# Either the form is displayed, or the posted data is validated
# and the post is added to the database or an error is shown.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
# The login_required decorator is used on the den views.
# A user must be logged in to visit these views, otherwise
# they will be redirected to the login page
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            # Confused on what flash() does?
            # See: https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO dens (name, description, author_id)'
                ' VALUES (?, ?, ?)',
                (name, description, g.user['id'])
            )
            db.commit()
            return redirect(url_for('dens.index'))

    return render_template('dens/create.html')


# Both the update and delete views will need to fetch a post by id
# and check if the author matches the logged in user. To avoid
# duplicating code, you can write a function to get the post and call it from each view.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        # abort() will raise a special exception that returns an HTTP status code.
        # 404 means “Not Found”.
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        # 403 means “Forbidden”.
        abort(403)

    return post


# Route for updating a den
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    #
    # TODO: authenticate that a user owns permission to edit a den before they can make changes
    #       should already know that a user is logged in due to the @login_required decorator function
    #

    den = get_den_info(id)
    print(g.user['id'])
    print(den['author_id'])
    if (int(g.user['id']) != int(den['author_id'])):
        print('error')
        return abort(403)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE dens SET name = ?, description = ?'
                'WHERE id = ?',
                (title, body, id))
            db.commit()
            return redirect(url_for('dens.index'))
    # To generate a URL to the update page, url_for() needs to be passed the id so it knows what to fill in: url_for('dens.update', id=post['id'])
    return render_template('dens/update.html', den=den)


# The delete view doesn’t have its own template, the delete button is part of update.html
# and posts to the /<id>/delete URL. Since there is no template, it will only handle the
# POST method and then redirect to the index view.
@bp.route('/<int:den_id>/delete', methods=('POST', 'GET'))
@login_required
def delete(den_id):
    get_post(den_id)
    db = get_db()
    db.execute('pragma foreign_keys = on;')
    db.execute('delete FROM dens WHERE id = ?', (den_id,))
    db.commit()
    return redirect(url_for('dens.index'))


# This route returns all the posts associated with a den.
@bp.route('/<int:den_id>', methods=['POST', 'GET'])
@login_required
def den(den_id):
    search = ''
    if request.method == 'POST':
        search = request.form['search']
    follow = get_db().execute('''
        select *
        from user_den_assoc
        where user_id = {}
        and den_id = {}
    '''.format(g.user['id'], den_id)).fetchone()
    if follow is None:
        follow = 'follow'
    else:
        follow = 'unfollow'
    posts = get_posts(den_id, search)
    den_info = get_den_info(den_id)
    return render_template('dens/den.html', den=den_info, posts=posts, follow=follow)


# Returns information for a specific den by id
def get_den_info(den_id):
    info = get_db().execute('''
    SELECT dens.name,
        dens.created,
        dens.description,
        users.username,
        dens.id,
        dens.author_id
    FROM dens,
        users
    WHERE users.id = dens.author_id
        AND dens.id = ?
    ''', (den_id,)).fetchone()
    return info


# Returns a list of all posts attached to a specific den by id and search keyword
def get_posts(den_id, search):
    if search == '':
        posts = get_db().execute('''
        SELECT users.username,
            posts.created,
            posts.title,
            posts.id,
            IFNULL(post.likes, 0) AS likes
        FROM users,
            posts
            LEFT JOIN (
                SELECT post_id,
                    COUNT(*) AS likes
                FROM post_like_assoc,
                    posts
                WHERE posts.id = post_like_assoc.post_id
                    AND posts.den_id = ?
                GROUP BY post_like_assoc.post_id
            ) AS post ON post_id = posts.id
        WHERE posts.den_id = ?
            AND posts.author_id = users.id
        ORDER BY likes DESC;
        ''',(den_id, den_id,)).fetchall()
    else:
        posts = get_db().execute('''
        SELECT users.username,
            posts.created,
            posts.title,
            posts.id,
            IFNULL(post.likes, 0) AS likes
        FROM users,
            posts
            LEFT JOIN (
                SELECT post_id,
                    COUNT(*) AS likes
                FROM post_like_assoc,
                    posts
                WHERE posts.id = post_like_assoc.post_id
                    AND posts.den_id = { }
                GROUP BY post_like_assoc.post_id
            ) AS post ON post_id = posts.id
        WHERE posts.den_id = { }
            AND posts.author_id = users.id
            AND posts.title LIKE '%{}%'
        ORDER BY likes DESC;
        '''.format(den_id, den_id, search)).fetchall()
    return posts


# Route for showing specific post information
@bp.route('/<int:den_id>/<int:post_id>', methods=['POST', 'GET'])
@login_required
def den_post(den_id, post_id):
    db = get_db()
    if request.method == 'POST':
        try:
            db.execute('''
            INSERT INTO post_like_assoc(user_id, post_id)
            VALUES(?, ?);
            ''', (g.user['id'], post_id,)
            )
            db.commit()
        except get_db().IntegrityError:
            # This user already liked the post, so the database will throw an IntegrityError
            # since there is a uniqueness constraint attached to the post_like_assoc table.
            db.execute('''
                DELETE FROM post_like_assoc
                WHERE user_id = ?
                    AND post_id = ?;
            ''', (g.user['id'], post_id,)
            )
            db.commit()

    den_info = get_den_info(den_id)
    post_info = get_post(post_id)
    likes = get_likes(post_id)
    comments = get_comments(post_id)

    return render_template('dens/post.html', den=den_info, post=post_info, likes=likes, comments=comments)


# Returns the username, created, title, and body of a single post queried by id
def get_post(post_id):
    post = get_db().execute('''
    SELECT posts.id,
        users.username,
        posts.created,
        posts.title,
        posts.body
    FROM posts,
        users
    WHERE users.id = posts.author_id
        AND posts.id = ?;
    ''', (post_id,)).fetchone()
    return post


# Returns the number of likes by post_id...
def get_likes(post_id):
    # TODO: handle getting likes for comments as well, see: https://github.com/tsainez/bobchat/issues/8
    likes = get_db().execute('''
        SELECT COUNT(*) AS COUNT
        FROM post_like_assoc
        WHERE post_id = ?;
        ''', (post_id,)).fetchone()
    return likes['count']


# Return a list of comments attached to a post
def get_comments(post_id):
    comments = get_db().execute('''
        SELECT users.username,
            comments.body,
            comments.created,
            comments.id
        FROM comments,
            users
        WHERE comments.author_id = users.id
            AND comments.post_id = ?
        ORDER BY comments.created DESC;
    ''', (post_id,)).fetchall()
    return comments


# Route that is used when the user wants to comment on a post
@bp.route('/<int:den_id>/<int:post_id>/comment', methods=['POST'])
# Although you are required to be logged in, you do not have to be a member of a den to comment in it.
@login_required
def comment(den_id, post_id):
    body = request.form['comment']
    db = get_db()
    db.execute('''
    INSERT INTO comments(author_id, post_id, body)
    VALUES(?, ?, ?)
    ''', (g.user['id'], post_id, body))
    db.commit()

    return redirect(url_for('dens.den_post', den_id=den_id, post_id=post_id))


# Route for when a user wants to follow a den...
@bp.route('/follow', methods=['POST'])
@login_required
def follow():
    db = get_db()
    den_id = request.form['den_id']
    if request.form['follow'] == 'unfollow':
        db.execute('''
            DELETE FROM user_den_assoc
            WHERE user_id = ?
                AND den_id = ?
        ''', (g.user['id'], den_id))
        db.commit()
    else:
        db.execute('''
            INSERT INTO user_den_assoc(user_id, den_id)
            VALUES(?, ?)
        ''', (g.user['id'], den_id))
        db.commit()
    return redirect(url_for('dens.den', den_id=den_id))
