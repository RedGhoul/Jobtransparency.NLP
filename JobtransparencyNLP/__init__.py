import os
from datetime import datetime
from flask import Flask,url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,current_user
from config import SECRET_KEY,SQLALCHEMY_DATABASE_URI
from flask import jsonify
import json
login_manager = LoginManager()
# $env:FLASK_APP = "app.py"
#$env:NasaMarsDataBaseUrl="https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0"
app = Flask(__name__)
# Connects our Flask App to our Database
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] =  SQLALCHEMY_DATABASE_URI #os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 40
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
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
from JobtransparencyNLP.adminModelViewer import RegModelView, SuperModelView
from JobtransparencyNLP.models import nlprecords, User, UserRole

admin = Admin(app, name='JobtransparencyNLP Admin', template_mode='bootstrap3')

admin.add_view(RegModelView(User, db.session))
admin.add_view(RegModelView(nlprecords, db.session))
admin.add_view(SuperModelView(UserRole, db.session))

