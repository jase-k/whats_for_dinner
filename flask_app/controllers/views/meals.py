from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User

@app.route('/record_meal')
def showRecord_Meal():
    user = User.getUserById(session['user_id'])
    return render_template('record_meal.html', user = user)

@app.route('/new_meal')
def showNewMeal():
    user = User.getUserById(session['user_id'])
    return render_template('new_meal.html', user = user)