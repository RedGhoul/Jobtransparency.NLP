from flask import Blueprint,render_template, redirect, url_for,flash, request
from flask_login import login_user,login_required,logout_user
from JobtransparencyNLP import db
from JobtransparencyNLP.models import User
from JobtransparencyNLP.users.forms import RegistrationForm,LoginForm

users_blueprint = Blueprint('users',__name__, template_folder='templates/users')

@users_blueprint.route('/logout')
def logout():
    logout_user()
    flash('You Logged out')
    return redirect(url_for('index'))

@users_blueprint.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in')
            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('index')

            return redirect(next)

    return render_template('login.html',form=form)

@users_blueprint.route('/register', methods=['GET','POST'])
def register():

    form = RegistrationForm()
   
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username=form.username.data, 
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registeration')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)
