from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from models import User

def invalid_credentials(form, field):
    """ Username and password checker """

    username = form.username.data
    password = field.data

    user_object = User.query.filter_by(username=username).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password, user_object.password):
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):
    """" Registration form """


    fullname = StringField("fullname_label", 
        validators=[InputRequired(message="Name required"),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    username = StringField("username_label", 
        validators=[InputRequired(message="Email required"),
        Length(min=4, max=25, message="Email must be between 4 and 25 characters")])
    password = PasswordField("password_label",
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField("confirm_pswd_lab",
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select a different username.")

class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label', 
        validators=[InputRequired(message="Username required")])
    password = StringField('password_label',
        validators=[InputRequired(message="Password required"), 
        invalid_credentials])
    submit_button = SubmitField('Log in')

class ProjectForm(FlaskForm):
    """ Project Form """

    name = StringField('name_label', 
        validators=[InputRequired(message="Project name required"), Length(min=4)])
    
    submit_button = SubmitField('Create')

class DeleteProjectForm(FlaskForm):
    """ Project Delete Form """

    name = StringField('name_label', 
        validators=[InputRequired(message="Project name required"), Length(min=1)])
    
    submit_button = SubmitField('Delete')

class SearchProjects(FlaskForm):
    """ Search Project Form """

    name = StringField('name_label', 
        validators=[InputRequired(message="Project name required"), Length(min=1)])
    
    submit_button = SubmitField('Search')