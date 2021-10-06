from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request
from datetime import date
from flask_app.models.recipe import Recipe


class Meal:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.recipes = []
        self.users = []
        self.date = data['date']

    @classmethod
    def addMealToMenu(cls, data):
        query = "INSERT INTO meals (created_at, updated_at, meal_type_id, date) VALUES (NOW(), NOW(), %(meal_type_id)s, %(date)s)"
        meal_id = MySQLConnection().query_db(query, data)
        cls.connectMealToUser(meal_id, data['user_id'])
        for recipe_id in data['recipes']:
            cls.connectRecipeToMeal(meal_id, recipe_id)
        return cls.getMealById(meal_id)
    
    @staticmethod
    def connectMealToUser(meal_id, user_id):
        query = f"INSERT INTO users_meals (created_at, updated_at, user_id, meal_id) VALUES (NOW(), NOW(), {user_id}, {meal_id})"
        id = MySQLConnection().query_db(query)
        return id

    @staticmethod
    def connectRecipeToMeal(meal_id, recipe_id):
        query = f"INSERT INTO meals_recipes (created_at, updated_at, recipe_id, meal_id) VALUES (NOW(), NOW(), {recipe_id}, {meal_id})"
        id = MySQLConnection().query_db(query)
        return id

    @classmethod
    def getMealById(cls, meal_id):
        query = f"SELECT * FROM meals LEFT JOIN meals_recipes ON meals_recipes.meal_id = meals.id LEFT JOIN users_meals ON users_meals.meal_id = meals.id WHERE meals.id = {meal_id}"
        db_data = MySQLConnection().query_db(query)

        if db_data:
            data = {
                "id" : db_data[0]['id'],
                "date" : db_data[0]['date'],
                "recipes" : [],
                "users" : []
            }
            recipe_ids = []
            user_ids = []
            for row in db_data:
                if row["recipe_id"] not in recipe_ids:
                    data["recipes"].append(Recipe.getRecipeById(row["recipe_id"]))
                    recipe_ids.append(row["recipe_id"])
                if row["user_id"] not in user_ids:
                    data["users"].append(row["user_id"])
                    user_ids.append(row["user_id"])
            print(data)
            return cls(data)
        else:
            return False

    @classmethod
    def getUserFutureMeals(cls, user_id, enddate, startdate= date.today()):
        print(startdate)
        pass