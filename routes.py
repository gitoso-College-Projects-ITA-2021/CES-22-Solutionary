from flask import render_template, redirect, url_for, request
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
        if current_user.is_authenticated:
            return "Logged in with flask-login!"

        return render_template("index.html")

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

@app.route('/project/', methods=['POST'])
@login_required
def project():

    proj_form = ProjectForm()
    del_proj_form = DeleteProjectForm()

    form_name = request.form['form-name']
    # Cria
    if form_name == 'add' and proj_form.validate_on_submit():
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
        
        return display_projects()
        #return redirect(url_for('index'))

    # Deleta
    if form_name == 'delete' and del_proj_form.validate_on_submit():
        name = del_proj_form.name.data
        # Check name exists
        project_object = Project.query.filter_by(name=name).first()
        if project_object:
            id = load_user( current_user.id ).id
            if project_object.owner == id:
                db.session.delete(project_object)
                db.session.commit()
            
            #else TODO
            # colocar notificação de que não foi possível deletar
        
        return display_projects()
        #return redirect(url_for('index'))

    return display_projects()
    #return render_template('projects.html', form=proj_form, del_form=del_proj_form)

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

@app.route('/project/', methods=['GET'])
@login_required
def display_projects():
    projects = Project.query.all()
    my_projects = Project.query.filter_by(owner=load_user( current_user.id ).id)
    proj_form = ProjectForm()
    del_proj_form = DeleteProjectForm()
    return render_template('projects.html', form=proj_form, del_form=del_proj_form, projects=projects,
    my_projects=my_projects)

#@app.route('/projects/', methods=['GET'])
#@login_required
#def all_projects():
#    projects = Project.query.all()
#
#    search_form = SearchProjects()
#    return render_template('all_projects.html', projects=projects, form=search_form)

@app.route('/projects/', methods=['GET', 'POST'])
@app.route('/projects/<string:name>', methods=['GET', 'POST'])
@login_required
def all_projects(name=None):
    search_form = SearchProjects()

    projects = Project.query.all()
    if not name:
        if request.method == 'GET':
            return render_template('all_projects.html', projects=projects, form=search_form)
        

        form_name = request.form['form-name']
        if form_name == 'search' and search_form.validate_on_submit():
            name = search_form.name.data

    
    projects = Project.query.filter_by(name=name)

    return render_template('all_projects.html', projects=projects, form=search_form)

#@app.route('/project/<project_id>')
#def project(project_id):
#    return render_template('')