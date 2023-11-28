import os
from flask import Flask, render_template, request, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, auth, firestore
from pyrebase import pyrebase
from flask import jsonify


# Initialize Firebase Admin SDK
cred = credentials.Certificate("KEYS\\user-api.json")
firebase_admin.initialize_app(cred)

firebase_config = {
  "apiKey": "AIzaSyAhs8VGY6wvs_kG5ujPdNkZAC7DAoTmPN4",
  "authDomain": "web-test-aa01a.firebaseapp.com",
  "databaseURL": "https://web-test-aa01a-default-rtdb.firebaseio.com",
  "projectId": "web-test-aa01a",
  "storageBucket": "web-test-aa01a.appspot.com",
  "messagingSenderId": "319219619955",
  "appId": "1:319219619955:web:0a44e3866f9c3c5ee93206",
  "measurementId": "G-WCJEGP2Z1G"
}


firebase = pyrebase.initialize_app(firebase_config)

auth1 = firebase.auth()

app = Flask(__name__)
db = firestore.client()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = auth.get_user_by_email(email)
        #check email and password from firestore
        try:            
            user = auth.get_user_by_email(email)
            if user:
                auth1.sign_in_with_email_and_password(email, password)
                return redirect(url_for('dashboard'))
        except:
            return "Invalid email or password"
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print("Method:", request.method)
    print("Form Data:", request.form)

    if request.method == 'POST':
        product_name = request.form['inputName']
        product_id = request.form['inputID']
        large_price = request.form['largePrice']
        small_price = request.form['smallPrice']
        product_data = {
            'name': product_name,
            'productID': product_id,
            'smallPrice': small_price,
            'largePrice': large_price
        }
        db.collection('products').add(product_data)
        return redirect(url_for('dashboard')) 

    products = db.collection('products').order_by('productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]
    return render_template('dashboard.html', products=product_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']  # Get the selected role from the form

        if password != confirm_password:
            return "Password and Confirm Password do not match"
        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                email_verified=False,
                password=password,
                display_name=username
            )
            # Save additional user information to Firestore database
            user_data = {
                'uid': user.uid,
                'username': username,
                'email': email,
                'password': password,
                'role': role  # Save the selected role to the database
                # Add more user data fields as needed
            }
            
            db.collection('users').add(user_data)

            return "Registration successful"  # You can redirect to another page if registration is successful
        except Exception as e:
            return f"Registration failed: {e}"

    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
