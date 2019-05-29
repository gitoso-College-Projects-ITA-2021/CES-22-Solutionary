from flask import Flask, render_template, redirect, url_for

from wtform_fields import *
from models import *

import flask

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://unuolholzadzsf:b2476c2787249f570b47e1c8c4cc435af6a6890acf8cba134f43f227f68fc1ef@ec2-54-83-192-245.compute-1.amazonaws.com:5432/d8id0sfmdse8sn'

db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Add it into DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    
    

    return render_template('index.html', form=reg_form)
    
@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validade_on_submit():
        return "Logged in, finally!"

    return render_template("login.html", form=login_form)



if __name__ == "__main__":

    app.run(debug=True)