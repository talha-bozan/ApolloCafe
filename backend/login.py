from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required
from user import *

app = Flask(__name__)
app.secret_key = 'secret string'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username == 'admin':
            user = User(1)
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
