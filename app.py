import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
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
app.secret_key = os.urandom(24)
db = firestore.client()

@app.route('/')
def index():
    products = db.collection('products').order_by('productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]
    #split list into two
    product_list1 = product_list[:len(product_list)//2]
    product_list2 = product_list[len(product_list)//2:]

    return render_template('home.html', products1=product_list1, products2=product_list2)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data_firebase = db.collection('users').where(field_path='email', op_string='==', value=email).stream()
        user_data_list = [user_data.to_dict() for user_data in user_data_firebase]
        if not user_data_list:
            return "User not found"
        user_role = user_data_list[0]['role']
        try:            
            user = auth.get_user_by_email(email)
            if user:
                auth1.sign_in_with_email_and_password(email, password)
                print("Successfully signed in")
                session['user_role'] = user_role
                session['user_id'] = user.uid
                print(session['user_role'])
                return redirect(url_for('dashboard'))
        except Exception as e:
            return f"Login failed: {e}"
    return render_template('login.html')

@app.route('/give_order', methods=['GET', 'POST'])
def give_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        product_id = request.form['product']
        quantity = request.form['quantity']
        user_id = session['user_id']

        # Logic to process the order...
        # This can involve storing the order in the database, calculating prices, etc.

        return "Order placed successfully!"

    # Load products to display in the form
    products = db.collection('products').order_by('productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]
    
    return render_template('give_order.html', products=product_list)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print("Method:", request.method)
    print("Form Data:", request.form)

    if 'user_role' in session:
        if session['user_role'] != 'ADMIN':
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

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
            user_data = {
                'uid': user.uid,
                'username': username,
                'email': email,
                'password': password,
                'role': role  
            }
            
            db.collection('users').add(user_data)

            return "Registration successful"  # You can redirect to another page if registration is successful
        except Exception as e:
            return f"Registration failed: {e}"

    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
