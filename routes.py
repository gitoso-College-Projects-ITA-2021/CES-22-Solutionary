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
    id = load_user( current_user.id ).id
    
    # if it is already subscribed, do not subscribe
    project_user = User.query.join(User.projects).filter(Project.name==project_name).filter(User.id==id).all()
    if project_user:
        return redirect(url_for('projects'))

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

# Project page
@app.route("/projects/<string:project_name>", methods=['GET'])
@login_required
def project(project_name=None):
    # Forms da question
    question_form = QuestionForm()

    # Returns questions related to project_name
    project_id = Project.query.filter_by(name=project_name).first().id

    # Is the user subscribed?
    is_subscribed = False
    id = load_user( current_user.id ).id
    if User.query.join(User.projects).filter(Project.name==project_name).filter(User.id==id).all():
        is_subscribed = True

    # Nonexistent project
    if not project_name or not project_id:
        return redirect(url_for('projects'))

    questions = Question.query.filter_by(project=project_id)

    return render_template('project_page.html', form=question_form, questions=questions, project_name=project_name)

@app.route("/projects/<string:project_name>/create-question", methods=['GET'])
@login_required
def create_question_page(project_name=None):
    question_form = QuestionForm()
    return render_template('create-question-page.html', project_name=project_name, question_form=question_form)

@app.route("/projects/<string:project_name>/create-question", methods=['POST'])
@login_required
def create_question(project_name=None):

    if not project_name:
        return redirect(url_for('projects'))

    # Checks if user is subscribed to project TODO

    question_form = QuestionForm()
    if question_form.validate_on_submit():
        name = question_form.name.data
        number = question_form.number.data
        description = question_form.description.data

        # Question is ralated to project id
        project_object = Project.query.filter_by(name=project_name).first()
        id = project_object.id
        question = Question(description=description, name=name, number=number, project=id)

        # Add it into DB
        db.session.add(question)
        db.session.commit()
    
    return redirect(url_for('project', project_name=project_name))

@app.route('/projects/<string:project_name>/delete-question', methods=['POST'])
@login_required
def delete_question(project_name=None):

    question_id = request.form['question_id']
    # Check if question exists
    question_object = Question.query.filter_by(id=question_id).first()
    if question_object:
        # Checks if current user is subscribed
        id = load_user( current_user.id ).id
        project_user = User.query.join(User.projects).filter(Project.name==project_name).filter(User.id==id).all()
        if project_user:
            db.session.delete(question_object)
            db.session.commit()
        
        #else TODO
        # colocar notificação de que não foi possível deletar
        
    return redirect(url_for('project'))

# Project page
@app.route("/projects/<string:project_name>/<int:question_id>", methods=['GET'])
@login_required
def question(project_name=None, question_id=None):
    solution_form = SolutionForm()
    

    # Associated question
    question = Question.query.filter_by(id=question_id).first()
    
    # Solutions to this question
    solutions = Solution.query.filter_by(question=question_id)


    return render_template('question-page.html', form=solution_form, question_id=question_id, 
    project_name=project_name, question=question, solutions=solutions)


@app.route("/projects/<string:project_name>/<int:question_id>/create-solution", methods=['POST'])
@login_required
def create_solution(project_name=None, question_id=None):

    if not project_name or not question_id:
        return redirect(url_for('projects'))

    # Checks if user is subscribed to project TODO

    sulution_form = SolutionForm()
    if sulution_form.validate_on_submit():
        description = sulution_form.description.data
        number = sulution_form.number.data
        id = load_user( current_user.id ).id

        # Project is ralated to question_id
        solution = Solution(description=description, number=number, project=question_id, owner=id)

        # Add it into DB
        db.session.add(solution)
        db.session.commit()

    return redirect(url_for('question', project_name=project_name, question_id=question_id))

@app.route('/projects/<string:project_name>/<int:question_id>/delete-solution', methods=['POST'])
@login_required
def delete_solution(project_name=None):

    solution_id = request.form['question_id']
    # Check if question exists
    solution_object = Solution.query.filter_by(id=solution_id).first()
    if solution_object:
        # Checks if current user owns solution
        id = load_user( current_user.id ).id
        if solution_object.owner == id:
            db.session.delete(solution_object)
            db.session.commit()
        
        #else TODO
        # colocar notificação de que não foi possível deletar
        
    return redirect(url_for('project'))

@app.route('/quill/<string:project_name>/<int:question_id>/', methods=['POST'])
@login_required
def test_post_quill(project_name=None, question_id=None):

    content = request.something['json']

    print(content)
    if content:
        quill = QuillTest(description=content, p_name=project_name, question_id=question_id)
        db.session.add(quill)
        db.session.commit()
    
    #else TODO
    # colocar notificação de que não foi possível deletar
        
    return redirect(url_for('project'))

@app.route('/quill/<string:project_name>/<int:question_id>/', methods=['GET'])
@login_required
def test_get_quill(project_name=None, question_id=None):

    quill = QuillTest.query.filter_by(p_name=project_name, question_id=question_id).first()

    #else TODO
    # colocar notificação de que não foi possível deletar
        
    return redirect(url_for('project'), text_content=quill)