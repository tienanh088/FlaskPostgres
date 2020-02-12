import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgres://mmrjwjfwsanysj:3ffd144041d1362720cd1aa27fad3c74256f66b99f85e4bbb0ff8eb1c50ad9ca@ec2-3-234-169-147.compute-1.amazonaws.com:5432/dbse72pe3srp6v'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    gender = db.Column(db.String(200))
    pin = db.Column(db.String(10))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/add', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            addfname = request.form.get('firstname')
            addlname = request.form.get('lastname')
            addaddr = request.form.get('address')
            addcity = request.form.get('city')
            addgender = request.form.get('gender')
            addpin = request.form.get('pin')

            user = Users(firstname = addfname, lastname = addlname, address = addaddr, city = addcity, gender = addgender, pin = addpin)
            db.session.add(user)
            db.session.commit()

            msg = "Record was successfully added"
        except:
            msg = "Error in insert operation"
        finally:
            return render_template('result.html', msg = msg)

@app.route('/list')
def list():
    return render_template('list.html', users = Users.query.all())