from flask_app.models.recipe import Recipe
from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes/<int:id>')
def displayRecipe(id):
    recipe = Recipe.getRecipeById(id)
    user = User.getUserById(session['user_id'])

    creator = User.getUserById(recipe.creator_id)

    if recipe: 
        return render_template('view_recipe.html', recipe = recipe, user = user, creator = creator) 
    else:
        return 'False'

@app.route('/recipes/<int:recipe_id>/favorite')
def favoriteARecipe(recipe_id):
    data = {
        'user_id' : session['user_id'],
        'recipe_id': recipe_id
    }
    Recipe.favoriteARecipe(data)

    return redirect(f'/recipes/{recipe_id}')

@app.route('/recipes/<int:recipe_id>/unfavorite')
def unfavoriteARecipe(recipe_id):
    data = {
        'user_id' : session['user_id'],
        'recipe_id': recipe_id
    }
    Recipe.unfavoriteARecipe(data)

    return redirect(f'/recipes/{recipe_id}')

@app.route('/add_recipe')
def showAddRecipePage():
    user = User.getUserById(session['user_id'])
    return render_template('add_recipe.html', user = user)

@app.route('/add_recipe/new', methods=['POST'])
def addRecipeToDB():
    print('FORM', request.form)
    data = {
        'user_id': session['user_id'],
        'title' : request.form['title'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'ingredients' : request.form.getlist('ingredient_list'),
        'quantity' : request.form.getlist('quantity'),
        'premium' : request.form['premium'],
        'quantity_type' : request.form.getlist('quantity_type'),
        'spoonacular_id' : request.form.getlist('spoonacular_id')
    }
    print('DATA', data)

    is_valid = Recipe.validateRecipe(data)
    if is_valid:
        id = Recipe.addRecipe(data)
        return redirect(f'/recipes/{id}')
    if not is_valid:
        return redirect('/add_recipe')
    
    

@app.route('/browse_recipes')
def showBrowse_Recipes():
    user = User.getUserById(session['user_id'])
    return render_template('browse_recipes.html', user = user)

@app.route('/edit_recipe/<int:id>')
def showEditRecipe(id):
    user = User.getUserById(session['user_id'])
    recipe = Recipe.getRecipeById(id)
    return render_template('edit_recipe.html', user = user, recipe = recipe)

@app.route('/update_recipe', methods=['POST'])
def updateRecipe():
    data ={
        'user_id': session['user_id'],
        'recipe_id' : request.form['recipe_id'],
        'title' : request.form['title'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'ingredients' : request.form.getlist('ingredient_list'),
        'quantity' : request.form.getlist('quantity'),
        'premium' : request.form['premium'],
        'quantity_type' : request.form.getlist('quantity_type'),
        'spoonacular_id' : request.form.getlist('spoonacular_id')
    }
    print('DATA', data)
    is_valid = Recipe.validateRecipe(data)
    print("ISVALID: ", is_valid)
    if is_valid:
        Recipe.updateRecipe(data)
        return redirect(f'/recipes/{data["recipe_id"]}')
    if not is_valid:
        return redirect(f"/edit_recipe/{data['recipe_id']}")