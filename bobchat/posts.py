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


@bp.route('/')
def index():
    return '<p>DJFHSDLJFHSDLJHFLKJSDHF</p>'
