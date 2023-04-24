# Store this code in 'app.py' file
 
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import re
 
from omega.src.field import User, Service, Network
from omega.src.models import Website

app = Flask(__name__)
app.config["SECRET_KEY"] = "demo-key"
app.config["JWT_SECRET_KEY"] = "demo-key"

jwt = JWTManager(app)

backend = Website(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    print(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = backend.check_login(username, password)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            access_token = create_access_token(identity=username)
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg, hash='#0xhgfujhee')
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    hash = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = backend.check_account(username)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            backend.create_account(username, password, email)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg, hash=hash)

@app.route('/index', methods = ['GET', 'POST'])
@jwt_required()
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        msg = 'change-later'
        return jsonify(msg)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Success', 200

@app.route('/verify', methods=['GET', 'POST'])
def verifyfn():
    # GET request
    if request.method == 'GET':
        message = {'hash': '0xhjdhfd'}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print("APP:", request.get_json())  # parse as JSON
        #return 'Success', 200
        return jsonify(request.get_json())
    
@app.route('/requestStatus', methods=['GET', 'POST'])
def status_request():
    request_data = request.get_json()
    # GET request
    if request.method == 'POST':
        # request : {public_key, signed_approval}
        #check that public key matches signature
        return None, 200  # serialize and use JSON headers
    # POST request
    if request.method == 'GET':
        #request has public key of customer account, use this to send encrypted data
        return_data = jsonify({"website_name": "example_name"})        #return 'Success', 200
        return return_data, 200

if __name__ == "__main__":
    app.run()