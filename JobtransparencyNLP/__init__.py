import os
from flask import Flask,url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import SECRET_KEY,SQLALCHEMY_DATABASE_URI

login_manager = LoginManager()

app = Flask(__name__)
# Connects our Flask App to our Database
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI #os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY #os.environ['SECRET_KEY']

db = SQLAlchemy(app)

Migrate(app,db)

from JobtransparencyNLP.users.views import users_blueprint
from JobtransparencyNLP.apistats.views import apistats_blueprint

app.register_blueprint(users_blueprint,url_prefix='/users')
app.register_blueprint(apistats_blueprint,url_prefix='/stats')

login_manager.init_app(app)
login_manager.login_view = 'users.login'


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from JobtransparencyNLP.models import nlprecords, User, UserRole

class NLPModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
        )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                return redirect(url_for('user.login', next=request.url))

admin = Admin(app, name='JobtransparencyNLP Admin', template_mode='bootstrap3')

admin.add_view(NLPModelView(User, db.session))
admin.add_view(NLPModelView(nlprecords, db.session))
admin.add_view(NLPModelView(UserRole, db.session))
