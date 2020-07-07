
from JobtransparencyNLP import db,login_manager
from sqlalchemy import Column, Integer, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

user_role_as = db.Table('user_role_as',
    db.Column('user_role_id', db.Integer, db.ForeignKey('userroles.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class UserRole(db.Model):
    __tablename__ = 'userroles'

    id = db.Column(db.Integer,primary_key=True)
    rolename = db.Column(db.String(64),unique=True,index=True)
    users = db.relationship('User',secondary = 'user_role_as')

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('UserRole',secondary = 'user_role_as')


    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

class ApiStats(db.Model):
    __tablename__ = 'apistats'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    hit_count = db.Column(db.Integer)

    def __init__(self,name,hit_count):
        self.name = name
        self.hit_count = hit_count

    def addHit(self):
        self.hit_count += 1

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class nlprecords(db.Model):
    __tablename__ = 'nlprecords'

    id = db.Column(db.Integer,primary_key=True)
    input_text = db.Column(db.Text)
    output_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    # updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    def __init__(self,input_text,output_text):
        self.input_text = input_text
        self.output_text = output_text
        self.created_at = datetime.datetime.utcnow()


