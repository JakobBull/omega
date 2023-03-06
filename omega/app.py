# Store this code in 'app.py' file
 
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import re
 
from src.field import User, Service, Network
 
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "demo-key"

jwt = JWTManager(app)

mysql = MySQL(app, host="localhost", user="root", password="Jakob@multiplii2021", db="geeklogin", autocommit=True)
mysql.init_app(app)


#setup blockchain etc
user1 = User()
network = Network()
service1 = Service("Facebook", "https://www.facebook.com/")
network.add_key(service1.public_key, service1)
service2 = Service("Omega", "https://omegaauthentication.com/")
network.add_key(service2.public_key, service2)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    print(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
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
        service1 = Service()
        network.add_key(service1.public_key, service1)
        hash = service1.public_key

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            #mysql.connection.commit()
            mysql.connect().commit()
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
        sig = str(service2.sign(msg))
        message = {'msg': msg, 'sig': sig}
        return jsonify(message)  # serialize and use JSON headers
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

if __name__ == "__main__":
    app.run()