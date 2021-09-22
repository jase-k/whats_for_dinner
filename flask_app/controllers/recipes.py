from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User

@app.route('/add_recipe/8')
def test():
    return '8000'

@app.route('/add_recipe')
def showAddRecipePage():
    user = User.getUserById(session['user_id'])
    return render_template('add_recipe.html', user = user)

@app.route('/add_recipe/new', methods=['POST'])
def addRecipeToDB():
    pass

@app.route('/browse_recipes')
def showBrowse_Recipes():
    user = User.getUserById(session['user_id'])
    return render_template('browse_recipes.html', user = user)