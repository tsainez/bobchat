# Define the blueprint and register it in the application factory.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bobchat.auth import login_required
from bobchat.db import get_db
bp = Blueprint('dens', __name__, url_prefix='/dens')


# The index will show all the dens available, which you can click on to view a den in more detail.
# A JOIN is used so that the author information from the user table is available in the result.
@bp.route('/')
def index():
    db = get_db()
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

    # TODO:
    #     Write a view to show an individual post on a page, where the user doesn’t matter because they’re not modifying the post.
    #     The check_author argument is defined so that the function can be used to get a post without checking the author.

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


# If you don’t specify int: and instead do <id>, it will be a string.
# The create and update views look very similar.
# The main difference is that the update view uses a post object and an UPDATE query instead of an INSERT.
# With some clever refactoring, you could use one view and template for both actions.
@bp.route('/test/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE posts SET title = ?, body = ?'
                'WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('dens.index'))
    # To generate a URL to the update page, url_for() needs to be passed the id so it knows what to fill in: url_for('dens.update', id=post['id'])
    return render_template('dens/update.html', post=post)


# The delete view doesn’t have its own template, the delete button is part of update.html
# and posts to the /<id>/delete URL. Since there is no template, it will only handle the
# POST method and then redirect to the index view.
@bp.route('/test/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dens.index'))

# return all the posts associated with a den
@bp.route('/<int:den_id>')
@login_required
def den(den_id):
    posts = get_posts(den_id)
    den_info = get_den_info(den_id)
    # print(posts[0]['author_id'])
    # return '<p>{}</p>'.format(str(posts))
    return render_template('dens/den.html', den = den_info, posts=posts)

# returns of a list of sqlite3 objects
# containing all available information dens queried by id (id of den) 
def get_den_info(den_id):
    info = get_db().execute('''
    select dens.name, dens.created, dens.description, users.username, dens.id
    from dens, users
    where users.id = dens.author_id
    and dens.id = ?
    ''',
    (den_id,)
    ).fetchone()
    return info

# returns a list of sqlite3 objects
# containing username, date dreated, and title of posts queried by den_id
def get_posts(den_id):
    posts = get_db().execute('''
    select users.username, posts.created, posts.title, posts.id
    from posts, users
    where posts.author_id = users.id 
    and den_id = ?
    order by posts.created DESC
    ''',
    (den_id,)
    ).fetchall()
    return posts

# returns information about the post.
# TODO: also return comments/likes/other info
@bp.route('/<int:den_id>/<int:post_id>', methods=['POST','GET'])
@login_required
def den_post(den_id, post_id):
    if request.method == 'POST':
        try:
            get_db().execute('''
                insert into post_like_assoc(user_id, post_id) values(?, ?);
            ''',(g.user['id'], post_id,)
            )
            get_db().commit()
        except get_db().IntegrityError:
            print('already liked')
            get_db().execute('''
                delete from post_like_assoc 
                where user_id = ?
                and post_id = ?;
            ''',(g.user['id'], post_id,)
            )
            get_db().commit()

    den_info = get_den_info(den_id)
    post_info = get_post(post_id)
    likes = get_likes(post_id)
    comments = get_comments(post_id)
    return render_template('dens/post.html', den = den_info, post = post_info, likes = likes, comments = comments)

# returns username, date created, title, body of a single post
# queried by id (id of post)
def get_post(post_id):
    post = get_db().execute('''
    select posts.id, users.username, posts.created, posts.title, posts.body
    from posts, users, post_like_assoc
    where users.id = posts.author_id
    and posts.id = ?;
    ''',
    (post_id,)
    ).fetchone()
    return post


# returns the number of likes by post_id
# originally I tried to make this a part of get_post(post_id) but ran into
# trouble when there were zero likes it would return an empty list 
def get_likes(post_id):
    likes = get_db().execute('''
    select count(*) as count
    from post_like_assoc
    where post_id = ?;
    ''',
    (post_id,)
    ).fetchone()
    return likes['count']

# return a list of comments
# originallly tried to make this a part of get_post(post_id) but ran into same trouble as get_post(post_id)
def get_comments(post_id):
    comments = get_db().execute('''
        select users.username, comments.body, comments.created, comments.id
        from comments, users
        where comments.author_id = users.id
        and comments.post_id = ?
        order by comments.created DESC;
    ''',
    (post_id,)).fetchall()
    return comments

# route that is used when the user wants to comment on a post
# users are not checked to be members of the den in which the post exists
@bp.route('/<int:den_id>/<int:post_id>/comment', methods=['POST'])
@login_required
def comment(den_id, post_id):
    body = request.form['comment']

    get_db().execute('''
    insert into comments(author_id, post_id, body)
    values(?, ?, ?)
    ''',
    (g.user['id'], post_id, body)
    )
    get_db().commit()
    return redirect(url_for('dens.den_post', den_id = den_id, post_id = post_id))


