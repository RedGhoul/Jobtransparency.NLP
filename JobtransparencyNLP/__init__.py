import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#from config import SECRET_KEY,SQLALCHEMY_DATABASE_URI
login_manager = LoginManager()

app = Flask(__name__)
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(app)

Migrate(app,db)

from JobtransparencyNLP.users.views import users_blueprint
from JobtransparencyNLP.apistats.views import apistats_blueprint

app.register_blueprint(users_blueprint,url_prefix='/users')
app.register_blueprint(apistats_blueprint,url_prefix='/stats')

login_manager.init_app(app)
login_manager.login_view = 'users.login'