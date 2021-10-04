from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request, session
from flask_app.models.ingredient import Ingredient
from flask_app.models.image import Image, RecipeImage, SpoonacularImage
from flask_app.models.cuisine import Cuisine
from abc import ABC, abstractclassmethod, abstractmethod

class Recipe(ABC):
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.title = data['title']
        self.instructions = data['instructions']
        self.description = data['description']
        self.premium = data['premium']
        self.source = data['source']
        self.cuisines = Cuisine.getRecipeCuisines(data['id'])
        self.ingredients = Ingredient.getAllRecipeIngredients(data['id']) #Returns an array of ingredient instance with the quantity and unit variables
        self.images = RecipeImage.getRecipeImages(data['id'])
        self.recipe_types = Recipe.getRecipesTypes(data['id'])
        self.spoonacular_id = data['spoonacular_id']


    def __str__(self) -> str:
        return f"id: {self.id}, created_at: {self.created_at}, updated_at: {self.updated_at}, creator_id: {self.creator_id}, title: {self.title}, instructions: {self.instructions}, description: {self.description}, premium: {self.premium}, ingredients: {self.ingredients}, cuisines: {self.cuisines}, images: {self.images}, recipe_types: {self.recipe_types}"
    
    def is_favorite(self, array):
        is_valid = False
        for x in array: 
            if self.id == x.id:
                is_valid = True
        return is_valid
    
    def has_recipe_type(self, type):
        for recipe_type in self.recipe_types:
            if type['name'] == recipe_type['name']:
                return True
        return False

    @classmethod
    def addRecipe(cls, data):
        query = "INSERT INTO recipes (created_at, updated_at, creator_id, title, instructions, premium, description, source) VALUES(NOW(), NOW(), %(user_id)s, %(title)s, %(instructions)s, %(premium)s, %(description)s, %(source)s)"

        recipe_id = MySQLConnection().query_db(query, data)

        if recipe_id:
            for cuisine in data['cuisines']:
                Cuisine.addCuisineToRecipe(recipe_id, cuisine)

            for x in range(len(data['ingredients'])):
                ingredient_id = Ingredient.findIngredientElseAdd(data['ingredients'][x])
        
                details = {
                    'recipe_id' : recipe_id,
                    'ingredient_id' : ingredient_id,
                    'quantity' : data['quantity'][x],
                    'quantity_type' : data['quantity_type'][x]
                }
                    
                Ingredient.addIngredientToRecipe(details)
        
            cls.addImagesToRecipe(data['images'], data['user_id'], recipe_id)

        return recipe_id

    @classmethod
    def updateRecipe(cls, data):
        #Updates the Recipe
        query = "UPDATE recipes SET updated_at = NOW(),  title = %(title)s, instructions= %(instructions)s, premium = %(premium)s, description =%(description)s  WHERE id = %(recipe_id)s"

        MySQLConnection().query_db(query, data)
        #Deletes Old Rows of Ingredient Connections
        query = f"DELETE FROM recipes_ingredients WHERE recipe_id = {data['recipe_id']}"
        MySQLConnection().query_db(query)

        Cuisine.updateRecipesCuisines(data['recipe_id'], data['cuisines'])
        Ingredient.updateRecipeIngredients(data)
        cls.addImagesToRecipe(data['images'], data['user_id'], data['recipe_id'])
        cls.addRecipeTypesToRecipe(data['recipe_types'], data['recipe_id']) #recipe_types is an array
    
        return 0

    @classmethod
    def addImagesToRecipe(cls, image_array, user_id, recipe_id):
        image_array = RecipeImage.validateImages(image_array)
        for image in image_array:
            image_id = RecipeImage.insertImageToDB(user_id, recipe_id, image)

        return 0

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
                "source" : row['source'],
                "spoonacular_id" : row['spoonacular_id']
            }

            recipes.append(cls(data))

        return recipes

    @staticmethod
    def getAllRecipeTypes():
        query = "SELECT * FROM recipe_types"

        return MySQLConnection().query_db(query)

    @staticmethod
    def getRecipesTypes(recipe_id):
        query = f"SELECT * FROM recipes_recipe_types LEFT JOIN recipe_types ON recipe_type_id = recipe_types.id WHERE recipe_id = {recipe_id}"

        db_data = MySQLConnection().query_db(query)
        recipe_types = []

        for row in db_data:
            recipe_type = {
                'name' : row['name'],
                'description' : row['description']
            }
            recipe_types.append(recipe_type)

        return recipe_types

    @staticmethod
    def addRecipeTypesToRecipe(type_array , recipe_id):
        query = f"DELETE FROM recipes_recipe_types WHERE recipe_id = {recipe_id}"
        MySQLConnection().query_db(query)
        
        ids = []
        for type_id in type_array:
            query = f"INSERT INTO recipes_recipe_types (recipe_id, recipe_type_id) VALUES ({recipe_id}, {type_id})"

            id = MySQLConnection().query_db(query)
            ids.append(id)

        return ids

class UserRecipe(Recipe):
    def __init__(self, data):
        super().__init__(data)
    


class SpoonacularRecipe(Recipe):
    def __init__(self, data):
        super().__init__(data)
        self.spoonacular_id = data['spoonacular_id']
    

    @classmethod
    def addRecipe(cls, data):
        #Check for Spoonacular Recipe in DB
        existing_recipe = cls.getRecipeBySpoonacularId(data['spoonacular_id'])
        if existing_recipe:
            return existing_recipe.id
        
        data['description'] = data['description'].replace("'", "`")
        
        query = f"INSERT INTO recipes (created_at, updated_at, creator_id, title, instructions, premium, description, source, spoonacular_id) VALUES(NOW(), NOW(), 1, '{data['title']}', '{data['instructions']}', '0', '{data['description']}', '{data['source']}', {data['spoonacular_id']})"
        print("Running query: ", query)
        recipe_id = MySQLConnection().query_db(query)

        if recipe_id:
            for cuisine in data['cuisines']:
                Cuisine.addCuisineToRecipe(recipe_id, Cuisine.getCuisineIdByName(cuisine))

            for ingredient in data['ingredients']:
                ingredient_id = Ingredient.findIngredientElseAdd(ingredient['name'], ingredient['spoonacular_id'])
        
                details = {
                    'recipe_id' : recipe_id,
                    'ingredient_id' : ingredient_id,
                    'quantity' : ingredient['quantity'],
                    'quantity_type' : ingredient['quantity_type']
                }
                    
                Ingredient.addIngredientToRecipe(details)
        
            SpoonacularImage.insertImageToDB(recipe_id, data['image'])
        
        #Add Recipe_Type
        recipe_types = cls.convertRecipeIds(data["recipe_types"])
        cls.addRecipeTypesToRecipe(recipe_types, recipe_id)

        #Add Recipe to Favorites
        details = {
            'user_id' : session['user_id'],
            'recipe_id': recipe_id
        }
        super().favoriteARecipe(details)

        return recipe_id

    @staticmethod
    def addRecipeTypesToRecipe(type_array , recipe_id):
        query = f"DELETE FROM recipes_recipe_types WHERE recipe_id = {recipe_id}"
        MySQLConnection().query_db(query)
        
        ids = []
        for type_id in type_array:
            query = f"INSERT INTO recipes_recipe_types (recipe_id, recipe_type_id) VALUES ({recipe_id}, {type_id})"

            id = MySQLConnection().query_db(query)
            ids.append(id)

        return ids

    @staticmethod
    def convertRecipeIds(type_array):
        type_ids = []
        for type in type_array:
            if "main" in type or "lunch" in type or "dinner" in type: 
                type = "main"
            if "side" in type: 
                type = "side"
            
            query = f"SELECT * FROM recipe_types WHERE name = '{type}'"
            db_data = MySQLConnection().query_db(query)
            if db_data:
                type_ids.append(db_data[0]['id'])
        

        return type_ids

    @classmethod
    def getRecipeBySpoonacularId(cls, id):
        query = f"SELECT * FROM recipes WHERE spoonacular_id = {id}"
        
        raw_data = MySQLConnection().query_db(query)

        if raw_data: 
            recipe = cls(raw_data[0])
            return recipe
        else:
            return False