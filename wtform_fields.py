from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User

def invalid_credentials(form, field):
    """ Username and password checker """

    username = form.username.data
    password = field.data

    user_object = User.query.filter_by(username=username).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif password != user_object.password:
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):
    """" Registration form """


    fullname = StringField("fullname_label", 
        validators=[InputRequired(message="Name required"),
        Length(min=4, max=10, message="Username must be between 4 and 10 characters")])
    username = StringField("username_label", 
        validators=[InputRequired(message="Email required"),
        Length(min=4, max=10, message="Email must be between 4 and 10 characters")])
    password = PasswordField("password_label",
        validators=[InputRequired(message="Password required"),
        Length(min=4, max=10, message="Password must be between 4 and 10 characters")])
    confirm_pswd = PasswordField("confirm_pswd_lab",
        validators=[InputRequired(message="Password required"),
        EqualTo('password', message="Passwords must match")])

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