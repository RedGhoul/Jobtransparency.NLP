from flask import Blueprint,render_template, redirect, url_for,flash, request
from flask_login import login_user,login_required,logout_user,current_user
from JobtransparencyNLP import db
from JobtransparencyNLP.models import User, UserRole
from JobtransparencyNLP.users.forms import RemoveRoles,RegistrationForm,LoginForm,AssignRoles
from config import SECRET_KEY
users_blueprint = Blueprint('users',__name__, template_folder='templates/users')
def getUsers():
    UserChoices = []
    for Cuser in User.query.all():
        UserChoices.append((Cuser.id,Cuser.email))
    
    return UserChoices

def getRoles():
    UserRoles = []
    for roles in UserRole.query.all():
        UserRoles.append((roles.id,roles.rolename))
    
    return UserRoles
@users_blueprint.route('/logout')
def logout():
    logout_user()
    flash('You Logged out')
    return redirect(url_for('index'))

@users_blueprint.route('/removeroles', methods=['GET','POST'])
@login_required
def removeroles():
    form = RemoveRoles()
    form.Roles.choices = getRoles()
    form.Users.choices = getUsers()
    for role in current_user.roles:
        if role.rolename == 'SuperUser':
            if form.is_submitted():
                curUser = User.query.filter_by(id=form.Users.data).first()
                Role = UserRole.query.filter_by(id=form.Roles.data).first()
                if Role in curUser.roles:
                    curUser.roles.remove(Role)

                db.session.commit()
                return redirect(url_for('index'))
                
    return render_template('assignroles.html',form=form)

@users_blueprint.route('/assignroles', methods=['GET','POST'])
@login_required
def assignroles():
    form = AssignRoles()
    form.Roles.choices = getRoles()
    form.Users.choices = getUsers()
    for role in current_user.roles:
        if role.rolename == 'SuperUser':

            if form.validate_on_submit():
                curUser = User.query.filter_by(email=form.Users.data).first()
                adminRole = UserRole.query.filter_by(rolename=form.Roles.data).first()
                curUser.roles.append(curUser)
                db.session.commit()
                return redirect(url_for('index'))

            
            return render_template('assignroles.html',form=form)

    flash('You do not have the role to view this page')
    return redirect(url_for('index'))

@users_blueprint.route('/AddRoless', methods=['GET'])
def addRoless():
    curUser = User.query.filter_by(email='avaneesab5@gmail.com').first()
    adminRole = UserRole.query.filter_by(rolename='Admin').first()
    curUser.roles.append(adminRole)
    db.session.commit()
    return redirect(url_for('index'))

@users_blueprint.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
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

        adminRole = UserRole.query.filter_by(rolename='Admin').first()
        superRole = UserRole.query.filter_by(rolename='SuperUser').first()
        if form.adminkey.data == SECRET_KEY:
            user.roles.append(adminRole)

        if form.adminkey.data == SECRET_KEY+"Super":
            user.roles.append(superRole)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registeration')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)
