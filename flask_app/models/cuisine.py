from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request

class Cuisine:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
    
    def is_in_recipe(self, array):
        is_valid = False
        for x in array: 
            if self.id == x.id:
                is_valid = True
        return is_valid

    @classmethod
    def getAllCuisines(cls):
        query = "SELECT * from cuisines"

        db_data = MySQLConnection().query_db(query)

        cuisines = []

        for cuisine in db_data: 
            cuisines.append(cls(cuisine))

        return cuisines
    
    @classmethod
    def getRecipeCuisines(cls, recipe_id):
        query = f'SELECT * FROM cuisines JOIN recipes_cuisines ON cuisines.id = recipes_cuisines.cuisine_id WHERE recipes_cuisines.recipe_id = {recipe_id}'

        db_data = MySQLConnection().query_db(query)

        cuisines = []

        for cuisine in db_data: 
            cuisines.append(cls(cuisine))

        return cuisines

    @classmethod
    def updateRecipesCuisines(cls, recipe_id, cuisine_ids):
        cls.deleteCuisinesFromRecipe(recipe_id)
        for id in cuisine_ids:
            cls.addCuisineToRecipe(recipe_id, id)
        return 0

    @staticmethod
    def addCuisineToRecipe(recipe_id, cuisine_id):
        query = f"INSERT INTO recipes_cuisines (recipe_id, cuisine_id) VALUES({recipe_id}, {cuisine_id})"

        id = MySQLConnection().query_db(query)

        return id
    
    @staticmethod
    def deleteCuisinesFromRecipe(recipe_id):
        query = f"DELETE FROM recipes_cuisines WHERE recipe_id = {recipe_id}"

        MySQLConnection().query_db(query)

        return 0

    