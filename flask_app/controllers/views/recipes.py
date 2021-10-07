from os import path
from flask_app.models.recipe import Recipe, SpoonacularRecipe
from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.cuisine import Cuisine
from flask_app.models.image import RecipeImage
import json



@app.route('/recipes/<int:id>')
def displayRecipe(id):
    recipe = Recipe.getRecipeById(id)
    user = User.getUserById(session['user_id'])

    creator = User.getUserById(recipe.creator_id)
    session['url'] = request.url

    recipe_types = Recipe.getAllRecipeTypes()
    print("RECIPE ", recipe)
    if recipe: 
        return render_template('recipe/view_recipe.html', recipe = recipe, user = user, creator = creator, recipe_types = recipe_types) 
    else:
        return 'False'


@app.route('/add_recipe')
def showAddRecipePage():
    user = User.getUserById(session['user_id'])
    cuisines = Cuisine.getAllCuisines()
    recipe_types = Recipe.getAllRecipeTypes()
    return render_template('recipe/add_recipe.html', user = user, cuisines = cuisines, recipe_types = recipe_types)

@app.route('/browse_recipes')
def showBrowse_Recipes():
    user = User.getUserById(session['user_id'])
    cuisines = Cuisine.getAllCuisines()

    return render_template('recipe/browse_recipes.html', user = user, cuisines = cuisines)

@app.route('/edit_recipe/<int:id>')
def showEditRecipe(id):
    user = User.getUserById(session['user_id'])
    recipe = Recipe.getRecipeById(id)
    cuisines = Cuisine.getAllCuisines()
    recipe_types = Recipe.getAllRecipeTypes()

    print(recipe)

    return render_template('recipe/edit_recipe.html', user = user, recipe = recipe, cuisines = cuisines, recipe_types = recipe_types)
