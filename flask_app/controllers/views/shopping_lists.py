from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User
from flask_app.models.meal import Meal

@app.route('/shopping_list')
def showShopping_List():
    user = User.getUserById(session['user_id'])
    meals = Meal.getUserFutureMealsByDates(user.id)
    return render_template('shopping_list.html', user = user, meals = meals)

