from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User
from flask_app.models.meal import Meal, MealType

@app.route('/record_meal')
def showRecord_Meal():
    user = User.getUserById(session['user_id'])
    return render_template('meal/record_meal.html', user = user)

@app.route('/new_meal')
def showNewMeal():
    user = User.getUserById(session['user_id'])
    meal_types = MealType.getMealAllMealTYpes()
    return render_template('meal/new_meal.html', user = user, meal_types = meal_types)

@app.route('/meals/<int:id>')
def viewMeal(id):
    meal = Meal.getMealById(id)
    user = User.getUserById(session['user_id'])
    meal_types = MealType.getMealAllMealTYpes()
    return render_template('meal/view_meal.html', user = user, meal = meal, meal_types = meal_types)

@app.route('/meals/<int:id>/edit')
def editMeal(id):
    meal = Meal.getMealById(id)
    user = User.getUserById(session['user_id'])
    meal_types = MealType.getMealAllMealTYpes()
    return render_template('meal/edit_meal.html', user = user, meal = meal, meal_types = meal_types)
