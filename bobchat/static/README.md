# static

Flask automatically adds a static view that takes a path relative to the bobchat/static directory and serves it.
The base.html template already has a link to the style.css file:

    {{ url_for('static', filename='style.css') }}
