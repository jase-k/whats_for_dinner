from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User

@app.route('/shopping_list')
def showShopping_List():
    user = User.getUserById(session['user_id'])
    return render_template('shopping_list.html', user = user)