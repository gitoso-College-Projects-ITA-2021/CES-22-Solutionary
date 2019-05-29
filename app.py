from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/project/')
def red_search():
    return redirect(url_for('search'))

@app.route('/project/<project_id>')
def project(project_id):
    return render_template('')
