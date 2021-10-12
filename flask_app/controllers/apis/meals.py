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
        "menu_id" : request.get_json()['menu_id'],
        "recipes" : request.get_json()['recipes']
    }
    meal = Meal.addMealToMenu(data).to_json()
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

@app.route('/update_meal', methods=["POST"])
def updateMeal():
    data = {
        "user_id" : session['user_id'],
        "meal_id" : request.get_json()['id'],
        "date" : request.get_json()['date'],
        "meal_type_id": request.get_json()['meal_type_id'],
        "recipes" : request.get_json()['recipes']
    }

    meal = Meal.updateMeal(data)
    
    if meal:
        response = {
            "status" : "success",
            "meal_id" : meal.id
        }
        return json.dumps(response)
    else:
        response = {
            "status" : "failed",
            "meal_id" : False
        }
        return json.dumps(response)
