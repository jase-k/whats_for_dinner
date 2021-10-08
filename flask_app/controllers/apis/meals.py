from flask import redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.meal import Meal
import json

@app.route('/add_meal', methods=["POST"])
def newMeal():
    data = {
        "user_id" : session['user_id'],
        "date" : request.get_json()['date'],
        "meal_type_id": request.get_json()['meal_type_id'],
        "recipes" : request.get_json()['recipes']
    }
    print("Sending Data", data)
    meal = Meal.addMealToMenu(data).to_json()
    print("Meal Added with Id: ", meal["id"])
    if meal:
        response = {
            "status" : "success",
            "meal_id" : meal["id"]
        }
        return json.dumps(response)
    else:
        response = {
            "status" : "failed",
            "meal_id" : False
        }
        return json.dumps(response)



@app.route('/meals/<int:id>/delete')
def deleteMeal(id):
    Meal.deleteMealById(id)
    return redirect(session["url"])

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