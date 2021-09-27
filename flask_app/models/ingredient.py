from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request

#Call getIngredientById with the data['recipe'] to get the quantity fields of ingredient in accordance with the recipe. 

class Ingredient:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.allergy_id = data['allergy_id']
        #API Spoonacular_id. Used to call for information
        self.spoonacular_id = data['spoonacular_id']
        if 'quantity' in data:
            self.quantity = data['quantity']
        if 'quantity_type' in data:
            self.quantity_type = data['quantity_type']

    def __str__(self) -> str:
        str = f"id: {self.id}, created_at: {self.created_at}, updated_at: {self.updated_at}, name: {self.name}, allergy_id: {self.allergy_id}, spoonacular_id: {self.spoonacular_id}"

        if 'quantity' in self:
            str += f", quantity: {self.quantity}"
        if 'quantity_type' in self:
            str += f", quantity_type: {self.quantity_type}"
        
        return str

    @classmethod
    def addIngredient(cls, data):
        # ALLERGY ID is set to NULL until further development
        query = "INSERT INTO ingredients (created_at, updated_at, name, allergy_id, spoonacular_id) VALUES(NOW(), NOW(), %(name)s, NULL, %(spoonacular_id)s)"

        id = MySQLConnection().query_db(query, data)

        return id

    @classmethod
    def findIngredientElseAdd(cls, ingredient_name, spoonacular_id = 0) -> int:
        id = cls.getIngredientByName(ingredient_name)
        if not id:

            info = {
                'name' : ingredient_name,
                'spoonacular_id' : spoonacular_id
            }
            id = cls.addIngredient(info)
        return id

    @classmethod
    def getIngredientByName(cls, name):
        query = f'SELECT * from ingredients WHERE name = "{name}"'

        data = MySQLConnection().query_db(query)
        print("INGREDIENT FOUND: ", data)

        if data:
            return data[0]['id']
        else:
            return False

    @classmethod
    def addIngredientToRecipe(cls, data):
        query = 'INSERT INTO recipes_ingredients (created_at, updated_at, recipe_id, ingredient_id, quantity, quantity_type) VALUES(NOW(), NOW(), %(recipe_id)s, %(ingredient_id)s,  %(quantity)s, %(quantity_type)s)'

        id = MySQLConnection().query_db(query, data)

        return id

    @classmethod
    def getAllRecipeIngredients(cls, recipe_id):
        query = f"SELECT * FROM ingredients JOIN recipes_ingredients ON recipes_ingredients.ingredient_id = ingredients.id WHERE recipe_id = {recipe_id}"

        db_results = MySQLConnection().query_db(query)

        ingredients = []

        if db_results:
            for row in db_results:
                ingredients.append(cls(row))
        return ingredients
    
    @classmethod
    def updateRecipeIngredients(cls, data):
        cls.deleteRecipeIngrients(data['recipe_id'])
        
        for x  in range(len(data['ingredients'])):
            #Adds Ingredient to our database if not currently there
            ingredient_id = cls.findIngredientElseAdd(data['ingredients'][x], data['spoonacular_id'][x])
            
            ing_data = {
                "recipe_id" : data['recipe_id'],
                "ingredient_id" : ingredient_id,
                'quantity' : data['quantity'][x],
                'quantity_type' : data['quantity_type'][x]
            }

            cls.addIngredientToRecipe(ing_data)
        
        return 0

    @staticmethod
    def deleteRecipeIngrients(recipe_id):
        query = f"DELETE FROM recipes_ingredients WHERE recipe_id = {recipe_id}"

        MySQLConnection().query_db(query)

        return 0
