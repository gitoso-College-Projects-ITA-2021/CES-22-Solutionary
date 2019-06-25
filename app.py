# Import Libraries
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# Configure app
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'replace later'

# Start Bootstrap
Bootstrap(app)

# Start database
db = SQLAlchemy(app)

# Import routes
from routes import *

# Start app
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

