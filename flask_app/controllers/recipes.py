from os import path
from flask_app.models.recipe import Recipe
from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.cuisine import Cuisine
from flask_app.models.image import RecipeImage



@app.route('/recipes/<int:id>')
def displayRecipe(id):
    recipe = Recipe.getRecipeById(id)
    user = User.getUserById(session['user_id'])

    creator = User.getUserById(recipe.creator_id)

    recipe_types = Recipe.getAllRecipeTypes()
    print("RECIPE ", recipe)
    if recipe: 
        return render_template('view_recipe.html', recipe = recipe, user = user, creator = creator, recipe_types = recipe_types) 
    else:
        return 'False'

@app.route('/recipes/<int:recipe_id>/delete_photo', methods = ["POST"])
def deletePhotoFromRecipe(recipe_id):
    photo_id = request.form['photo_id']
    RecipeImage.deleteImage(photo_id)
    if 'url' in session: 
        return redirect(session['url'])
    return redirect(f'/recipes/{recipe_id}')

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
    cuisines = Cuisine.getAllCuisines()
    return render_template('add_recipe.html', user = user, cuisines = cuisines)

@app.route('/add_recipe/new', methods=['POST'])
def addRecipeToDB():
    print('FORM', request.form)
    data = {
        'user_id': session['user_id'],
        'title' : request.form['title'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'cuisines' : request.form.getlist('cuisines'),
        'ingredients' : request.form.getlist('ingredient_list'),
        'quantity' : request.form.getlist('quantity'),
        'premium' : request.form['premium'],
        'quantity_type' : request.form.getlist('quantity_type'),
        'spoonacular_id' : request.form.getlist('spoonacular_id'), 
        'images' : request.files.getlist('image'),
        'source' : "What's For Dinner User Original"
    }
    for image in data['images']:
        print('one image')
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
    cuisines = Cuisine.getAllCuisines()

    return render_template('browse_recipes.html', user = user, cuisines = cuisines)

@app.route('/edit_recipe/<int:id>')
def showEditRecipe(id):
    user = User.getUserById(session['user_id'])
    recipe = Recipe.getRecipeById(id)
    cuisines = Cuisine.getAllCuisines()
    recipe_types = Recipe.getAllRecipeTypes()

    print(recipe)

    return render_template('edit_recipe.html', user = user, recipe = recipe, cuisines = cuisines, recipe_types = recipe_types)

@app.route('/update_recipe', methods=['POST'])
def updateRecipe():
    data = {
        'user_id': session['user_id'],
        'recipe_id' : request.form['recipe_id'],
        'title' : request.form['title'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'cuisines' : request.form.getlist('cuisines'),
        'ingredients' : request.form.getlist('ingredient_list'),
        'quantity' : request.form.getlist('quantity'),
        'premium' : request.form['premium'],
        'quantity_type' : request.form.getlist('quantity_type'),
        'spoonacular_id' : request.form.getlist('spoonacular_id'),
        'images' : request.files.getlist('image'),
        'recipe_types' : request.form.getlist('recipe_types')
    }

    print('DATA', data)
    is_valid = Recipe.validateRecipe(data)
    print("ISVALID: ", is_valid)
    if is_valid:
        Recipe.updateRecipe(data)
        return redirect(f'/recipes/{data["recipe_id"]}')
    if not is_valid:
        return redirect(f"/edit_recipe/{data['recipe_id']}")