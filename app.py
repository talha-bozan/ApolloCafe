import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import firebase_admin
from firebase_admin import credentials, auth, firestore
from pyrebase import pyrebase
from flask import jsonify
import json
import datetime
import time

userApiData = {
    "apiKey": "AIzaSyAhs8VGY6wvs_kG5ujPdNkZAC7DAoTmPN4",
    "type": "service_account",
    "project_id": "web-test-aa01a",
    "private_key_id": "463dc49af4bffe61b8da06997299e01f88829680",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+UgrDIUJMtQnb\npRoaKWF7RoTA5t8eRRxU4VwMeSUU8dtqOseQwLLr+0TcFxXakrgwT3CFRnhhIZqO\nprVOoXZCl56VETmiU9vFilVzar3OvkDKTfM6RWzd72G/ZjjHz3GDXqx4N2sOEKCa\nzZno4YYxqfO/7XUCayKsQgzWSmATSQ6AxQiMGEeU1vxqUqh1RyrgYYCXMjQmK7d3\nb1a3TyHlWUEX8O7XOos1j1Ij7FmOWaEHBkrqs//G5V+jKwS3LmbduhUxRBvWadKE\ntOgAiA4nMYuOIFrcOD5d844I1YZoLgVGxwIFUbUqrj9MMyM0lpwRAGAPmmPABhQA\n5qByNx41AgMBAAECggEATVgXEpSuFnFOR8pxcKdXe9s9MQ3CJ9GLQX1yRIlpBfmC\nI0ou9wcwz1EGe3EQSwrsOonWHvt0CXk4D/f037cjUc2/PzJIW008F6vvrR94cpAD\n0ZNbINe89faGIVwAAEewCGTNr29KHOWp9y9N+IPKXt2D9wAf2LNEXH/dKqsAH2WS\nPhK2Cv9bFRPliScdGhqoVFr+lRB1KIKSwXi5fgBRyz21oSkD+c937fwyoN6V70NC\nnF7nARegWKsEeTwPqLLXNc/pt/nx6bAEx0dM9ONuKyDFvNJM9sgGfQKFQETsWYdk\nBvpIsJEVLEKAtNY0R4QvANO0siJrPPCI0PJ7Rw/9owKBgQDiUMryThu6N4QHNvBK\nhG2kImEIBt7AOYT2zTlxkyDOnrKTyW7v1eJzdQlu/I6fbcQwZtFehjsG9fSmDYJz\nQDRE25TCLaRxvqjXEHAI/PQ1ok1il/t7ZOfrhg0CJ6+6J8x/m3h7Fh2xfboSK3FN\noPCJRt25Py6IgE5amQfwdLkobwKBgQDXSJukvMOuq60VTd5ZX4ACxlUQ/VW0ZtdU\nMFET+mxzB0s5q9pX1LxOAdXC9nLmNsagIu3ff4J9BV67frWn6nDRPNcLUdRs7j7J\n5F9cBABknhqeKfnj66DNSirbJrtR/iDUDlEGS1JQUWrf6DTCLX5D6ot783/BITib\nxbLsDNINmwKBgEa6vVKQ+rVuGEMw9lQzoxiC7hRWIVOuJlIDvYozUzOAAYuSjqtC\nCy3OTA51vBUzdvcxiwmhpdz9DWLAIh7m1+8VOR6eqSArWBUuu/TzKVeBy/GeUig0\nVw8SrAoaYR8qxQy0iCjftpP8GSUIkraSL9qXXUBB8McUYmiKHyMVN7DdAoGBAIOL\nZTdC9FrNocQLwZpgpUqMv7vS4ESMNnTF1TTc5tlekpOZs5/JaIpNyr0Hc+vBepqs\n3SactjIITvtIEF2a/faMM2ZCSQeKiCk69x21gDv6847DXWLsPmRSNl+Uig8utgZ8\n/PtYmOJk7WYFb/9aZvW+4h4KCn0K/JkKMyrTJqKTAoGAMgdmbdGIFWjyHQInV73a\nl1rEWerc5cp/iw1r4XoG+7M1d1t2eWDggWmsH0rgzg/11PsZ5QcVt0S693eUabAz\nQyqmuI5YfZXGTcWFwTesdppTWyh3OW3mst+3YID1AaLmUiDY1xs16HspUt46pZCW\nAoP0fefVApzcfYzR6NSxKmM=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-zqjf3@web-test-aa01a.iam.gserviceaccount.com",
    "client_id": "102011635578896413661",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-zqjf3%40web-test-aa01a.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}


cred = credentials.Certificate(userApiData)

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

    products = db.collection('products').order_by(
        'productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]
    return render_template('userindex.html', coffees=product_list)


@app.route('/')
def index():
    products = db.collection('products').order_by(
        'productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]

    return render_template('index.html', coffees=product_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data_firebase = db.collection('users').where(
            field_path='email', op_string='==', value=email).stream()
        user_data_list = [user_data.to_dict()
                          for user_data in user_data_firebase]
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
        delivery_time = request.form['delivery_time']
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")

        order_data = {
            'userID': user_id,
            'coffee_type': coffee_type,
            'quantity': quantity,
            'delivery_time': delivery_time,
            'date_time': date_time,
            'status': 'pending',
            'orderID': os.urandom(24).hex()
        }

        doc_ref = db.collection('orders').add(order_data)
        order_id = doc_ref[1].id

        order_data['orderID'] = order_id

        return redirect(url_for('confirm_order'))

    products = db.collection('products').stream()
    product_list = [prod.to_dict() for prod in products]

    return render_template('giveorder.html', products=product_list)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    return redirect(url_for('index'))


@app.route('/confirm_order')
def confirm_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    current_orders = db.collection('orders').where(
        'userID', '==', user_id).stream()
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
    current_orders = db.collection('orders').where(
        'userID', '==', user_id).stream()

    for order_snapshot in current_orders:
        order = order_snapshot.to_dict()
        order['status'] = 'confirmed'

        db.collection('current_orders').add(order)

        order_snapshot.reference.delete()

    return jsonify({"message": "Orders confirmed"}), 200


@app.route('/adminindex', methods=['GET', 'POST'])
def adminindex():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['user_role'] != 'ADMIN':
        return redirect(url_for('userindex'))
    products = db.collection('products').order_by(
        'productID', direction=firestore.Query.ASCENDING).stream()
    product_list = [prod.to_dict() for prod in products]

    return render_template('adminindex.html', coffees=product_list)


@app.route('/user_orders', methods=['GET', 'POST'])
def user_orders():
    if 'user_role' in session:
        if session['user_role'] != 'ADMIN':
            return redirect(url_for('userindex'))
    else:
        return redirect(url_for('login'))

    last_ten_orders = db.collection('current_orders').order_by(
        'date_time', direction=firestore.Query.DESCENDING).limit(10).stream()

    current_orders_with_names = []

    for order_snapshot in last_ten_orders:
        order = order_snapshot.to_dict()

        user_id = order['userID']
        user_snapshot = db.collection('users').where(
            'uid', '==', user_id).limit(1).stream()
        user_data = next(user_snapshot, None)

        if user_data:
            user_full_name = user_data.to_dict().get('fullname', 'No name')
            order['user_full_name'] = user_full_name

        current_orders_with_names.append(order)

    print(current_orders_with_names)
    current_orders_with_names.sort(key=lambda x: time.mktime(
        time.strptime(x['date_time'], "%d/%m/%Y %H:%M:%S")), reverse=True)

    return render_template('userorders.html', currentOrderList=current_orders_with_names)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user_role' in session:
        if session['user_role'] != 'ADMIN':
            return redirect(url_for('userindex'))
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

    products = db.collection('products').stream()
    product_list = [prod.to_dict() for prod in products]
    product_list.sort(key=lambda x: int(x['productID']))

    return render_template('addproduct.html', products=product_list)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            return "Password and Confirm Password do not match"
        try:
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
                'role': role,
                'fullname': fullname
            }

            db.collection('users').add(user_data)

            if role == 'ADMIN':
                return redirect(url_for('adminindex'))
            else:
                return redirect(url_for('userindex'))

        except Exception as e:
            return f"Registration failed: {e}"

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
