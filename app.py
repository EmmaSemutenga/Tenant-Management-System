import csv
import os
import requests

from flask import Flask, session, render_template, url_for, flash, logging, redirect, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

#imported a data file
from tenants import Tenants

app = Flask(__name__)

Tenants = Tenants()


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgresql://postgres:emz@localhost:5432/rentals')
#engine = create_engine("postgres://ejamgpdjfseyvb:95b220c4f0313c2a1f73784f5a7ac8d8411fe32b58bcc622fb15a46e826be33f@ec2-184-73-250-50.compute-1.amazonaws.com:5432/d4cbchhtnf8tmb")
db = scoped_session(sessionmaker(bind=engine))

#index page
@app.route('/')
def index():
    return render_template('index.html')

class RegisterForm(Form):
    name     = StringField('Name', [validators.Length(min=1, max=50)])
    username     = StringField('Username', [validators.Length(min=4, max=25)])
    email        = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        #get form values
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data)) #we ncrypt before storage

        db.execute("INSERT INTO owners (name, username, email, password) VALUES (:name, :username, :email, :password)",{"name": name, "username": username, "email": email, "password":password})
        db.commit()
        
        flash('You are now registered and can login', 'success')
        
        return redirect(url_for('login'))


    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        #get form fields
        #username = request.form.get("username")
        username = request.form["username"]
        password_candidate = request.form.get("password")


        result = db.execute("SELECT * FROM owners WHERE username = :username", {"username": username}).fetchone()

        if len(result) > 0:
            
            password = result['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password) :
                
                session['logged_in']= True
                session['username'] = result['username']
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else: 
                flash('Password not matched', 'danger')
                return render_template('login.html')
        else:
            flash('USERNAME NOT FOUND', 'danger')
            return render_template('login.html')

    return render_template("login.html")

#check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template("dashboard.html")

#tenants route
@app.route('/tenants', methods = ['GET', 'POST'])
def tenants():
    
    return render_template('tenants.html', tenants=Tenants) 

#tenants route
@app.route('/single_tenant/<string:id>')
def single_tenant():
    return render_template('single_tenant.html')    

