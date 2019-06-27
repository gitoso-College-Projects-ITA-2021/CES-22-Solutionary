from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, JSON
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
    """ Project model """

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    subs = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(25), unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

class Question(UserMixin, db.Model):
    """ Question model """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    sol_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.JSON, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    project = db.Column(db.Integer, db.ForeignKey('projects.id'))

class Solution(UserMixin, db.Model):
    """ Solution model """

    __tablename__ = "solutions"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.JSON, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner_name = db.Column(db.String(25), nullable=False)
    question = db.Column(db.Integer, db.ForeignKey('questions.id'))

class QuillTest(UserMixin, db.Model):
    """ Quill model """

    __tablename__ = "quills"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.JSON, nullable=False)
    p_name = db.Column(db.String(300), nullable=True)
    question_id = db.Column(db.Integer, nullable=True)