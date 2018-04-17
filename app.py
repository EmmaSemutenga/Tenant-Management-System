import csv
import os
import requests #used with apis

from flask import Flask, session, render_template, url_for, flash, logging, redirect, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, PasswordField, validators, IntegerField, BooleanField
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SECRET_KEY"] = "jfjfjfkdkdncdkdcd"

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




# Set up database
engine = create_engine('postgresql://postgres:12345@localhost:5432/rentals')
#engine = create_engine("postgres://ejamgpdjfseyvb:95b220c4f0313c2a1f73784f5a7ac8d8411fe32b58bcc622fb15a46e826be33f@ec2-184-73-250-50.compute-1.amazonaws.com:5432/d4cbchhtnf8tmb")
db = scoped_session(sessionmaker(bind=engine))

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


class RegisterForm(FlaskForm):
    name     = StringField('Name', [validators.Length(min=1, max=50)])
    username     = StringField('Username', [validators.Length(min=4, max=25)])
    email        = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route("/register", methods=["POST", "GET"])
@is_logged_in
def register():
    #form = RegisterForm(request.form)
    form = RegisterForm()
    #if request.method == "POST" and form.validate():
    if form.validate_on_submit():#checks for post requests and also that the form is valid

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

@app.route('/', methods=['GET', 'POST'])
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

class HouseForm(FlaskForm):
    house_no     = StringField('House Number', [validators.Length(min=1, max=50)])
    type_of_house    = StringField('Type of House', [validators.Length(min=1, max=25)])
    location    = StringField('Location', [validators.Length(min=1, max=25)])
    rent_amount    = IntegerField('Rent Amount')
    status        = BooleanField('Status')
    #image    = StringField('Image', [validators.Length(min=1, max=25)])
    image = FileField("House Photo", validators=[FileRequired()])

@app.route('/add_house', methods=['GET','POST'])
@is_logged_in
def add_house():
    #form = HouseForm(request.form)
    form = HouseForm()
    #if request.method == "POST" and form.validate():
    if form.validate_on_submit():
        #get form values
        house_no     = form.house_no.data
        type_of_house    = form.type_of_house.data
        location    = form.location.data
        rent_amount    = form.rent_amount.data
        status = form.status.data
        #image = form.image.data
        f = form.image.data
        imagename = secure_filename(f.filename)#image name
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))


        db.execute("INSERT INTO houses (house_no, type_of_house, location, rent_amount, status, image) VALUES (:house_no, :type_of_house, :location, :rent_amount, :status, :image)",{"house_no":house_no, "type_of_house":type_of_house, "location":location, "rent_amount":rent_amount, "status":status, "image":imagename})
        db.commit()

        flash('House has been registered', 'success')

        return redirect(url_for('dashboard'))


    return render_template('add_house.html', form = form)

@app.route('/houses')
@is_logged_in
def houses():
    result = db.execute("SELECT * FROM houses").fetchall()
    if len(result) > 0:
        return render_template("houses.html", houses = result)
    else:
        flash('No Houses found', 'danger')
        return render_template('dashboard.html', houses = result)

@app.route('/house/<int:house_id>')
def house(house_id):
    result = db.execute("SELECT * FROM houses where id=:house_id", {'house_id':house_id}).fetchone()

    return render_template('house.html', house = result)