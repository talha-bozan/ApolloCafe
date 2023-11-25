import os
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("KEYS\\user-api.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(username)  # Assuming you use email as the username
            auth.verify_password(password, user.password_hash)
            return "Login successful"  # You can redirect to another page if login is successful
        except Exception as e:
            return f"Login failed: {e}"

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
