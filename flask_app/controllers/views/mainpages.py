from flask_app import app
from flask import render_template

@app.route('/')
def mainPage():
    return "This page is being built"

@app.route('/register')
def registrationPage():
    return render_template('main/registration.html')

@app.route('/login')
def loginPage():
    return render_template('main/login.html')

