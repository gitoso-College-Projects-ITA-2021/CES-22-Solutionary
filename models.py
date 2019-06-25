from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)


relations = db.Table('relations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'))
)

class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    # Relationship with project table
    projects = db.relationship('Project', secondary=relations, backref=db.backref('subscribers', lazy='dynamic'))


class Project(UserMixin, db.Model):
    """ User model """

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
