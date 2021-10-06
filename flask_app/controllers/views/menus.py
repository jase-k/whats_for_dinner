from flask import redirect, request, session, render_template
from werkzeug.datastructures import MultiDict
from flask_app import app
from flask_app.models.user import User
from flask_app.models.meal import Meal

@app.route('/menu')
def showMenu():
    user = User.getUserById(session['user_id'])
    enddate = request.args.get('enddate')
    if enddate:
        menu = Meal.getUserFutureMealsByDates(enddate)
    else:
        menu = Meal.getUserFutureWeekMeals(session['user_id'])
    
    return render_template("view_menu.html", user = user, menu_meals = menu)