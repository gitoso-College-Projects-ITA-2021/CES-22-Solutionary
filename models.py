from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

class Project(UserMixin, db.Model):
    """ User model """

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    owner = db.Column(db.Integer(), nullable=False)

db.create_all()