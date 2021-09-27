from flask_app.models.image import Image
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request, session
from flask_app.models.ingredient import Ingredient
from flask_app.models.image import Image
from flask_app.models.cuisine import Cuisine

class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.title = data['title']
        self.instructions = data['instructions']
        self.description = data['description']
        self.premium = data['premium']
        self.cuisines = Cuisine.getRecipeCuisines(data['id'])
        self.ingredients = Ingredient.getAllRecipeIngredients(data['id']) #Returns an array of ingredient instance with the quantity and unit variables

    def __str__(self) -> str:
        return f"id: {self.id}, created_at: {self.created_at}, updated_at: {self.updated_at}, creator_id: {self.creator_id}, title: {self.title}, instructions: {self.instructions}, description: {self.description}, premium: {self.premium}, ingredients: {self.ingredients}, cuisines: {self.cuisines}"
    
    def is_favorite(self, array):
        is_valid = False
        for x in array: 
            if self.id == x.id:
                is_valid = True
        return is_valid
        

    @staticmethod
    def addRecipe(data):
        query = "INSERT INTO recipes (created_at, updated_at, creator_id, title, instructions, premium, description) VALUES(NOW(), NOW(), %(user_id)s, %(title)s, %(instructions)s, %(premium)s, %(description)s)"

        recipe_id = MySQLConnection().query_db(query, data)

        for cuisine in data['cuisines']:
            Cuisine.addCuisineToRecipe(recipe_id, cuisine)

        if recipe_id:
            for x in range(len(data['ingredients'])):
                ingredient = Ingredient.getIngredientByName(data['ingredients'][x])
                if not ingredient:
                    info = {
                        'name' : data['ingredients'][x],
                        'spoonacular_id' : data['spoonacular_id'][x]
                    }
                    new_ingredient_id = Ingredient.addIngredient(info)
                    
                
                details = {
                    'recipe_id' : recipe_id,
                    'quantity' : data['quantity'][x],
                    'quantity_type' : data['quantity_type'][x]
                }
                if ingredient:
                    details['ingredient_id'] = ingredient.id
                else: 
                    details['ingredient_id'] = new_ingredient_id
                    
                Ingredient.addIngredientToRecipe(details)

                print(data['ingredients'][x])
                print(data['quantity'][x])
                print(data['quantity_type'][x])

        return recipe_id

    @staticmethod
    def updateRecipe(data):
        #Updates the Recipe
        query = "UPDATE recipes SET updated_at = NOW(),  title = %(title)s, instructions= %(instructions)s, premium = %(premium)s, description =%(description)s  WHERE id = %(recipe_id)s"

        MySQLConnection().query_db(query, data)
        #Deletes Old Rows of Ingredient Connections
        query = f"DELETE FROM recipes_ingredients WHERE recipe_id = {data['recipe_id']}"
        MySQLConnection().query_db(query)

        Cuisine.updateRecipesCuisines(data['recipe_id'], data['cuisines'])

        #Adds new Ingredient connections
        for x in range(len(data['ingredients'])):
            ingredient = Ingredient.getIngredientByName(data['ingredients'][x])
            if not ingredient:
                info = {
                    'name' : data['ingredients'][x],
                    'spoonacular_id' : data['spoonacular_id'][x]
                }
                new_ingredient_id = Ingredient.addIngredient(info)
                
            
            details = {
                'recipe_id' : data['recipe_id'],
                'quantity' : data['quantity'][x],
                'quantity_type' : data['quantity_type'][x]
            }
            
            if ingredient:
                details['ingredient_id'] = ingredient.id
            else: 
                details['ingredient_id'] = new_ingredient_id
                
            Ingredient.addIngredientToRecipe(details)

            print(data['ingredients'][x])
            print(data['quantity'][x])
            print(data['quantity_type'][x])

        return 1
    
    @classmethod
    def getRecipeById(cls, id):
        #Join User info, reviews
        query = f"SELECT * FROM recipes WHERE recipes.id = {id}"
        
        raw_data = MySQLConnection().query_db(query)

        if raw_data: 
            recipe = cls(raw_data[0])

            print("THIS IS A RECIPE", recipe)
            return recipe
        else:
            return False

    @classmethod
    def validateRecipe(cls, data):
        is_valid = True

        #Validate text areas
        if(len(data['instructions']) < 20):
            flash("Uh Oh! Looks like your instructions are not long enough to follow! Please add complete instructions. ", 'instructions')
            is_valid = False
        if(len(data['description']) < 20):
            flash("Please add a longer description", 'description')
            is_valid = False
        if(len(data['description']) > 255):
            flash("Description needs to be less than 250 characters", 'description')
            is_valid = False
        
        #ingredient list comes as an array
        if(len(data['ingredients']) < 2):
            flash("Ingredient List must contain at least 2 ingredients", 'ingredients')
            is_valid = False
        if(len(data['ingredients']) > 30):
            flash("Whoa there! Looks like this is a complicated recipe. If your recipe requires over 30 ingredients, please contact us", 'ingredients')
            is_valid = False

        #title validation = Add stripping of white Space
        if(len(data['title']) < 3):
            flash("Recipe title must be at least 3 letters", 'title')
            is_valid = False
        if(len(data['title']) > 45):
            flash("Recipe title must be less than 45 characters", 'title')
            is_valid = False

        if not is_valid:
            session['title'] = data['title']
            session['description'] = data['description']
            session['instructions'] = data['instructions']
        else:
            if 'title' in session:
                session.pop('title')
            if 'description' in session:
                session.pop('description')
            if 'instructions' in session:
                session.pop('instructions')
            

        return is_valid


    @staticmethod
    def favoriteARecipe(data):
        # Data object should include: 'user_id' and 'recipe_id' keys
        query = "INSERT INTO favorites_recipes (updated_at, user_id, recipe_id) VALUES (NOW(), %(user_id)s, %(recipe_id)s)"
        
        id = MySQLConnection().query_db(query, data)

        if id: 
            flash('A Server error occured when trying to favorite a recipe. Please contact us if problem persists.')
            return id
        else:
            return False

    @staticmethod
    def unfavoriteARecipe(data):
        query = "DELETE FROM favorites_recipes WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s"

        MySQLConnection().query_db(query, data)

        return 1

    @classmethod
    def getFavoriteRecipes(cls,user_id):
        query = f"SELECT * from favorites_recipes LEFT JOIN recipes ON  recipe_id = recipes.id WHERE user_id = {user_id}"
        
        db_data = MySQLConnection().query_db(query)

        recipes = []
        for row in db_data:
            data = {
                "id" : row['recipe_id'],
                "created_at" : row['recipes.created_at'],
                "updated_at" : row['recipes.updated_at'],
                "creator_id" : row['creator_id'],
                "title" : row['title'],
                "instructions" : row['instructions'],
                "description" : row['description'],
                "premium" : row['premium'],
            }

            recipes.append(cls(data))

        return recipes
