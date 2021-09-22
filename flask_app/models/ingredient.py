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
        if 'recipe_id' in data:
            self.quantity = Ingredient.getRecipesIngredients(data['recipe_id'], data['id'])['quantity']
            self.quantity_type = Ingredient.getRecipesIngredients(data['recipe_id'], data['id'])['quantity_type']

    @classmethod
    def addIngredient(cls, data):
        # ALLERGY ID is set to NULL until further development
        query = "INSERT INTO ingredients (created_at, updated_at, name, allergy_id, spoonacular_id) VALUES(NOW(), NOW(), %(name)s, NULL, %(spoonacular_id)s)"

        id = MySQLConnection().query_db(query, data)

        return id

    @classmethod
    def getIngredientByName(cls, name):
        query = f'SELECT * from ingredients WHERE name = "{name}"'

        data = MySQLConnection().query_db(query)

        if data:
            print("THIS INGREDIENT EXISTS!")
            return cls(data[0])
        else:
            return {}

    @classmethod
    def addIngredientToRecipe(cls, data):
        query = 'INSERT INTO recipes_ingredients (created_at, updated_at, recipe_id, ingredient_id, quantity, quantity_type) VALUES(NOW(), NOW(), %(recipe_id)s, %(ingredient_id)s,  %(quantity)s, %(quantity_type)s)'

        id = MySQLConnection().query_db(query, data)

        return id
    
    @staticmethod
    def getRecipesIngredients(recipe_id, ingredient_id ):
        query = f"SELECT * FROM recipes_ingredients WHERE recipe_id = {recipe_id} AND ingredient_id = {ingredient_id}"

        results = MySQLConnection().query_db(query)[0]

        return results

