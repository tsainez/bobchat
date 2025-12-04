import os
from flask import (
    Blueprint, request, jsonify, abort
)
from bobchat.db import get_db

bp = Blueprint('integrations', __name__, url_prefix='/integrations')

@bp.route('/github/webhook', methods=['POST'])
def github_webhook():
    # Use environment variable for the secret token
    # Default to a placeholder only for development, but in prod it should be set
    expected_token = os.environ.get('BOBCHAT_GITHUB_TOKEN', 'dev_token_please_change')

    token = request.headers.get('X-Auth-Token')

    # Secure comparison could be better but this is sufficient for this scope
    if token != expected_token:
        # Also check query param for flexibility
        if request.args.get('token') != expected_token:
            abort(403)

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON payload provided'}), 400

    title = data.get('title')
    body = data.get('body')
    den_id = data.get('den_id', 1) # Default to den_id 1 if not specified

    if not title or not body:
        return jsonify({'status': 'error', 'message': 'Title and body are required'}), 400

    db = get_db()

    # Try to find a 'github_bot' user, or fallback to user id 1
    user = db.execute('SELECT id FROM users WHERE username = ?', ('github_bot',)).fetchone()

    if user:
        author_id = user['id']
    else:
        # Fallback to the first user (usually admin created by init-db)
        # We need to ensure this user exists to avoid foreign key errors.
        # Given init-db creates users, id 1 should exist.
        author_id = 1

    # Verify den exists
    den = db.execute('SELECT id FROM dens WHERE id = ?', (den_id,)).fetchone()
    if not den:
         return jsonify({'status': 'error', 'message': f'Den with id {den_id} not found'}), 404

    db.execute('''
        INSERT INTO posts(author_id, den_id, title, body)
        VALUES(?, ?, ?, ?)
    ''', (author_id, den_id, title, body,))
    db.commit()

    return jsonify({'status': 'success', 'message': 'Post created'}), 201
