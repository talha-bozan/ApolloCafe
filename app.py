import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from firebase_admin import firestore




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
