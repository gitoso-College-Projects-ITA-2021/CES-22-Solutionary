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
    login_form = LoginForm()
    app.jinja_env.globals['login_form'] = login_form
    app.jinja_env.globals['logged'] = False

    if login_form.validate_on_submit():
        app.jinja_env.globals['logged'] = True
        return render_template("index.html")
    return render_template("index.html")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    # Updated database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add it into DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html', form=reg_form)

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/project/')
def red_search():
    return redirect(url_for('search'))

@app.route('/project/<project_id>')
def project(project_id):
    return render_template('')


if __name__ == "__main__":
    app.run(debug=True)

