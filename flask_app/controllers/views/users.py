import re
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.meal import Meal
from flask_app.models.user import User
import os

@app.route('/dashboard')
def displayUserDashboard():
    if not 'user_id' in session:
        return redirect('/')
    
    user = User.getUserById(session['user_id'])
    meals = Meal.getUserFutureWeekMeals(session['user_id'])

    print("Current User:",user)

    return render_template('dashboard.html', user = user, menu_meals = meals)



@app.route('/preferences')
def showPreferences():
    if not 'user_id' in session:
        return redirect('/')
    user = User.getUserById(session['user_id'])

    return render_template('preferences.html', user = user)



@app.route('/find_friends')
def showFind_Friends():
    user = User.getUserById(session['user_id'])
    return render_template('find_friends.html', user = user)

