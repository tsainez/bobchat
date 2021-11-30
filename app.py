from db import *
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from flask_wtf import FlaskForm
from flask.templating import render_template
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
from flask import request, Response


# some bullshit from the flask_login slides from 106
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# so the templates folder works or something
bootstrap = Bootstrap(app)

# for the templates also
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    confpass = PasswordField('confirm password', validators=[InputRequired()])

@app.route('/')
def index():
    return redirect('/home')

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()

    # if method is post then check was was posted, otherwise serve templates/login.html
    if (request.method == 'POST'):
        
        # I think these ifs can be combined but fck it
        # make sure user exists in user table
        if (User.query.filter_by(username = form.username.data).first() is not None):
            # if the user exists then check the password, this way only log in if user exists and password is correct
            if(User.query.filter_by(username = form.username.data).first().password == form.password.data):
                user = User.query.filter_by(username = form.username.data).first()
                login_user(user)
                # session['user'] = user
                return redirect('/home')
        else:
            # otherwise tell user to try again
            return '<a href=\'/login\'>wrong username or password, click here to try again</a>'
    
    return render_template('login.html', form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if (request.method == 'POST'):
        
        # only add to db if user does not exist
        if (User.query.filter_by(username = form.username.data).first() is not None):
            return '<a href=\'/register\'>username already exists, click here to try again.</a>'
        
        # next make sure passwords match
        if (form.confpass.data != form.password.data):
            return '<a href=\'/register\'>passwords did not match, click here to try again.</a>'
        
        # if username not already taken and passwords match then add to db
        db.session.add(User(username = form.username.data, password = form.password.data))
        db.session.commit()
        return '<a href=\'/login\'>account created, click here to head to login</a>'
    
    # if the request method is not POST then serve the register page.
    return render_template('register.html', form = form)

@app.route('/home')
@login_required
def home():
    return '<p>you are logged in</p>'


if __name__ == '__main__':
    app.run()