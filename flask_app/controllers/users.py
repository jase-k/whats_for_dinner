import re
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
import os


@app.route('/register/newuser', methods=['POST'])
def addUserToDB():


    print("Request Form: ", request.form)
    #sets a mutable dicitonary from for so password can be hashed through registerUser()
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'phone' : request.form['phone'],
        'country_code' : request.form['country_code'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password']
    }
    #returns id if valid, else returns false
    id = User.registerUser(data)

    if id:
        return redirect('/dashboard')
    else:
        return redirect('/register')

@app.route('/login/existing_user', methods=['POST'])
def loginInUser():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }
    is_vaild = User.validateLogin(data)
    print("RETURNED USER ", is_vaild)

    if is_vaild:
        return redirect('/dashboard')
    else:
        return redirect('/login')

@app.route('/dashboard')
def displayUserDashboard():
    if not 'user_id' in session:
        return redirect('/')
    
    user = User.getUserById(session['user_id'])

    print("Current User:",user)

    return render_template('dashboard.html', user = user)

#Need to update to be able to edit one thing at a time. 
@app.route('/users/update', methods=['POST'])
def updateUser():
    print("Request Files: ", request.files)

    data = {
        'id' : request.form['user_id'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'profile_picture': request.files['profile_picture']
    }

    User.updateUser(data)
    return redirect('/dashboard')

@app.route('/preferences')
def showPreferences():
    if not 'user_id' in session:
        return redirect('/')
    user = User.getUserById(session['user_id'])

    return render_template('preferences.html', user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/find_friends')
def showFind_Friends():
    user = User.getUserById(session['user_id'])
    return render_template('find_friends.html', user = user)

