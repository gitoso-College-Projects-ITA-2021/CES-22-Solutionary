from flask import render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms import *
from app import app, db
from models import *

# Configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('index'))

    return render_template("index.html", form=login_form)

@app.route("/private", methods=['GET', 'POST'])
@login_required
def private():

    # Usar isso se na for usar o "@login_required"
    #if not current_user.is_authenticated:
    #    return "Please login."
    return "something"

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    return "Logged out"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()

    # Updated database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)

        # Check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            render_template('register.html', form=reg_form)
        # Add it into DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html', form=reg_form)

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/project/', methods=['GET', 'POST'])
@login_required
def project():

    proj_form = ProjectForm()
    del_proj_form = DeleteProjectForm()

    if del_proj_form.submit_button.data and del_proj_form.validate_on_submit():

        name = del_proj_form.name.data
        # Check name exists
        project_object = Project.query.filter_by(name=name).first()
        if project_object:
            db.session.delete(project_object)
            db.session.commit()
        
        return redirect(url_for('index'))

    if proj_form.submit_button.data and proj_form.validate_on_submit():
        name = proj_form.name.data

        # Check name exists
        project_object = Project.query.filter_by(name=name).first()
        if project_object:
            render_template('projects.html', form=proj_form, del_form=del_proj_form)
        # Add it into DB
        id = load_user( current_user.id ).id
        project = Project(name=name, owner=id)
        db.session.add(project)
        db.session.commit()
        

        return redirect(url_for('index'))

    
    return render_template('projects.html', create_form=proj_form, del_form=del_proj_form)

@app.route('/project/<string:name>', methods=['POST'])
@login_required
def delete_project(name):
    # Check name exists
    project_object = Project.query.filter_by(name=name).first()
    if project_object:
        render_template('projects.html', form=ProjectForm(), del_form=DeleteProjectForm())
    # Add it into DB
    id = load_user( current_user.id ).id
    project = Project(name=name, owner=id)
    db.session.add(project)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/quill')
def quill():
    return render_template('quill.html')
