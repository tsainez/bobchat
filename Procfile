web: python3 -m venv venv; . venv/bin/activate; pip install -e .; gunicorn "bobchat:create_app()"
worker: flask init-db