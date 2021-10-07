from flask import redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.meal import Meal

@app.route('/add_meal', methods=["POST"])
def newMeal():
    data = {
        "user_id" : session['user_id'],
        "date" : request.form['date'],
        "meal_type_id": request.form['meal_type'],
        "recipes" : request.form.getlist('recipes')
    }
    meal_id = Meal.addMealToMenu(data)
    return redirect('/menu')



@app.route('/meals/<int:id>/delete')
def deleteMeal():
    pass

@app.route('/edit_meal', methods=["POST"])
def updateMeal():
    data = {
        "id" : request.form['meal_id'],
        "date" : request.form['date'],
        "meal_type_id" : request.form['meal_type'],
        "recipes" : request.form.getlist('recipes')
    }
    Meal.updateMeal(data)
    return redirect("/menu")