import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import firebase_admin
from firebase_admin import credentials, auth, firestore
from pyrebase import pyrebase
from flask import jsonify
import json
import datetime
import time



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

@app.route('/userindex')
def userindex():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    products = db.collection('products').order_by('productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]
    return render_template('userindex.html', coffees = product_list)

@app.route('/')
def index():
    products = db.collection('products').order_by('productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]
    
    return render_template('index.html', coffees = product_list)

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
                session['user_role'] = user_role
                session['user_id'] = user.uid
                return redirect(url_for('adminindex'))
        except Exception as e:
            return f"Login failed: {e}"
    return render_template('login.html')

@app.route('/give_order', methods=['GET', 'POST'])
def give_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    if request.method == 'POST':
        coffee_type = request.form['coffee_type']
        quantity = request.form['quantity']
        delivery_time = request.form['delivery_time']  # Example: "now", "in 35 minutes", etc.
        #add date and time
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")

        order_data = {
            'userID': user_id,
            'coffee_type': coffee_type,
            'quantity': quantity,
            'delivery_time': delivery_time,
            'date_time': date_time,
            'status' : 'pending',
            'orderID': os.urandom(24).hex()
        }
        
        # Add the order to the Firestore database and get the document reference
        doc_ref = db.collection('orders').add(order_data)
        order_id = doc_ref[1].id

        order_data['orderID'] = order_id

        # Get the ID of the newly created document
        
        return redirect(url_for('confirm_order'))

    products = db.collection('products').stream()
    product_list = [prod.to_dict() for prod in products]
    
    return render_template('giveorder.html', products=product_list)



@app.route('/confirm_order')
def confirm_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))
   
    user_id = session['user_id']
    current_orders = db.collection('orders').where('userID', '==', user_id).stream()
    orders_list = [order.to_dict() for order in current_orders]

    empty_list = []
    if orders_list:
        return render_template('orders.html', order_list=orders_list)
    else:
        return render_template('orders.html', order_list=empty_list)

@app.route('/confirm_orders', methods=['POST'])
def confirm_orders():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session['user_id']
    current_orders = db.collection('orders').where('userID', '==', user_id).stream()
    
    for order_snapshot in current_orders:
        order = order_snapshot.to_dict()
        order['status'] = 'confirmed'
        
        # Add the order to 'current_orders' collection
        db.collection('current_orders').add(order)

        # Delete the order from the original 'orders' collection
        order_snapshot.reference.delete()

    return jsonify({"message": "Orders confirmed"}), 200

@app.route('/adminindex', methods=['GET', 'POST'])
def adminindex():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['user_role'] != 'ADMIN':
        return redirect(url_for('login'))
    products = db.collection('products').order_by('productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]

    return render_template('adminindex.html', coffees = product_list)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user_role' in session:
        if session['user_role'] != 'ADMIN':
            return redirect(url_for('userindex'))
    else:
        return redirect(url_for('adminindex'))

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
    #change below to sort by date and time
    last_ten_orders = db.collection('orders').order_by('date_time', direction=firestore.Query.DESCENDING).stream()
    current_orders_list = [order.to_dict() for order in last_ten_orders]
    #sort the current list by date_time
    current_orders_list.sort(key=lambda x: time.mktime(time.strptime(x['date_time'], "%d/%m/%Y %H:%M:%S")), reverse=True)

    products = db.collection('products').order_by('productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]
    return render_template('dashboard.html', products=product_list, currentOrderList = current_orders_list )

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

    return render_template('signup.html')

@app.route('/thank_you')
def thank_you():
    #fetch user email, uid, username from firebase
    user = auth.get_user(session['user_id'])
    user_email = user.email
    user_name = user.display_name
    user_id = user.uid

    user_data = {
        'uid': user_id,
        'username': user_name,
        'email': user_email,
    }

    user_data_firebase = db.collection('users').where(field_path='email', op_string='==', value=user_email).stream()
    user_data_list = [user_data.to_dict() for user_data in user_data_firebase]
    return render_template('thank_you.html', user_data=user_data)


@app.route('/card')
def card():
    return render_template('card.html')
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
