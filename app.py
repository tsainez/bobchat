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
    return Users.query.get(int(user_id))

# so the templates folder works or something
bootstrap = Bootstrap(app)

# for the templates also
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    firstname = StringField('first name', validators=[InputRequired()])
    lastname = StringField('last name',validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    confpass = PasswordField('confirm password', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    major = StringField('major', validators=[InputRequired()])


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
        if (Users.query.filter_by(username = form.username.data).first() is not None):
            # if the user exists then check the password, this way only log in if user exists and password is correct
            if(Users.query.filter_by(username = form.username.data).first().password == form.password.data):
                user = Users.query.filter_by(username = form.username.data).first()
                login_user(user)
                # session['user'] = user
                return redirect('/home')
            print(Users.query.filter_by(username = form.username.data).first().password)
            print(form.password.data)
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if (request.method == 'POST'):
        
        # only add to db if user does not exist
        if (Users.query.filter_by(username = form.username.data).first() is not None):
            return '<a href=\'/register\'>username already exists, click here to try again.</a>'
        
        # next make sure passwords match
        if (form.confpass.data != form.password.data):
            return '<a href=\'/register\'>passwords did not match, click here to try again.</a>'
        
        # if username not already taken and passwords match then add to db
        db.session.add(Users(username = form.username.data, password = form.password.data))
        db.session.commit()
        return '<a href=\'/login\'>account created, click here to head to login</a>'
    
    # if the request method is not POST then serve the register page.
    return render_template('register.html', form = form)


@app.route('/home')
@login_required
def home():
    denList = ""
    name = Users.query.filter_by(id = current_user.id).first().firstname
    for row in Users_And_Dens.query.filter_by(user_id = current_user.id).all():
        denName = str(Dens.query.filter_by(id = row.den_id).first().name)
        denUrl = denName.replace(' ', '%20')
        denList += "<p><a href = '/{}'>{}</a></p>".format(denUrl, denName)
    return render_template('home.html', name = name, dens = denList)

@app.route('/<den>', methods=['GET','POST'])
@login_required
def den(den):
    denName = den.replace('%20', ' ')
    if Dens.query.filter_by(name = denName).first() is None:
        return redirect('/home')
    if request.method == 'POST':
        print(request.form['toPost'])
        print(current_user.firstname)
        
    return render_template('den.html', denName = denName, denUrl = den)

if __name__ == '__main__':
    app.run()