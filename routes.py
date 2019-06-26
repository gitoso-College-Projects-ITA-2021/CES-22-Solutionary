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
    reg_form = RegistrationForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('index'))

    return render_template("index.html", register_form=reg_form, login_form=login_form)

@app.route("/private", methods=['GET'])
@login_required
def private():

    # Usar isso se na for usar o "@login_required"
    #if not current_user.is_authenticated:
    #    return "Please login."
    return "something"

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['POST'])
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

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/create-project/', methods=['POST'])
@login_required
def create_project():
    proj_form = ProjectForm()

    if proj_form.validate_on_submit():
        name = proj_form.name.data

        # Check name exists
        project_object = Project.query.filter_by(name=name).first()
        if project_object:
            return redirect(url_for('projects')) # Colocar mensagem de erro se nome for igual
        # Add it into DB
        id = load_user( current_user.id ).id
        project = Project(name=name, owner=id)
        db.session.add(project)
        db.session.commit()
    
    return redirect(url_for('projects'))

@app.route('/delete-project', methods=['POST'])
@login_required
def delete_project():

    project_id = request.form['project_id']
    # Check name exists
    project_object = Project.query.filter_by(id=project_id).first()
    if project_object:
        id = load_user( current_user.id ).id
        if project_object.owner == id:
            db.session.delete(project_object)
            db.session.commit()
        
        #else TODO
        # colocar notificação de que não foi possível deletar
        
    return redirect(url_for('projects'))


# @app.route('/project/', methods=['POST'])
# @login_required
# def project():

#     proj_form = ProjectForm()
#     del_proj_form = DeleteProjectForm()

#     form_name = request.form['form-name']
#     # Cria
#     if form_name == 'add' and proj_form.validate_on_submit():
#         name = proj_form.name.data

#         # Check name exists
#         project_object = Project.query.filter_by(name=name).first()
#         if project_object:
#             render_template('projects.html', form=proj_form, del_form=del_proj_form)
#         # Add it into DB
#         id = load_user( current_user.id ).id
#         project = Project(name=name, owner=id)
#         db.session.add(project)
#         db.session.commit()
        
#         return display_projects()
#         #return redirect(url_for('index'))

#     # Deleta
#     if form_name == 'delete' and del_proj_form.validate_on_submit():
#         name = del_proj_form.name.data
#         # Check name exists
#         project_object = Project.query.filter_by(name=name).first()
#         if project_object:
#             id = load_user( current_user.id ).id
#             if project_object.owner == id:
#                 db.session.delete(project_object)
#                 db.session.commit()
            
#             #else TODO
#             # colocar notificação de que não foi possível deletar
        
#         return display_projects()
#         #return redirect(url_for('index'))

#     return display_projects()
#     #return render_template('projects.html', form=proj_form, del_form=del_proj_form)

# @app.route('/project/', methods=['GET'])
# @login_required
# def display_projects():
#     projects = Project.query.all()
#     my_projects = Project.query.filter_by(owner=load_user( current_user.id ).id)
#     subscribed_projects = current_user.projects
#     proj_form = ProjectForm()
#     del_proj_form = DeleteProjectForm()

#     return render_template('projects.html', form=proj_form, del_form=del_proj_form, projects=projects,
#     my_projects=my_projects, subscribed=subscribed_projects)

@app.route('/projects/', methods=['GET', 'POST'])
@login_required
def projects():
    # Forms de busca
    search_form = SearchProjects()
    # Todos os projetos existentes
    projects = Project.query.all()
    # Projetos os quais sou owner
    my_projects = Project.query.filter_by(owner=load_user( current_user.id ).id)
    # Projetos nos quais estou inscrito
    subscribed_projects = current_user.projects
    # Form para a criação de projetos
    proj_form = ProjectForm()

    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'search' and search_form.validate_on_submit():
            name = search_form.name.data
            projects = Project.query.filter_by(name=name)

    return render_template('projects.html', projects=projects, form=search_form, my_projects=my_projects,
     subscribed_projects=subscribed_projects, create_project_form=proj_form)


@app.route('/projects/<string:project_name>/subscribe', methods=['POST'])
@login_required
def subscribe(project_name=None):
    if not project_name:
        return 'Not possible'   # TODO
    
    project_object = Project.query.filter_by(name=project_name).first()

    project_object.subscribers.append(current_user)
    db.session.commit()

    return redirect(url_for('projects'))

@app.route('/projects/<string:project_name>/unsubscribe', methods=['POST'])
@login_required
def unsubscribe(project_name=None):
    if not project_name:
        return 'Not possible'   # TODO
    
    project_object = Project.query.filter_by(name=project_name).first()

    project_object.subscribers.remove(current_user)
    db.session.commit()

    return redirect(url_for('projects'))


@app.route('/quill')
def quill():
    return render_template('quill.html')

@app.route("/temp", methods=['GET', 'POST'])
@login_required
def temp():
    return render_template('temp.html')
