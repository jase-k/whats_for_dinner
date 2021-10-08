from werkzeug.utils import redirect
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request
from datetime import date
import datetime
import calendar
from flask_app.models.recipe import Recipe


class Meal:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.recipes = data['recipes']
        self.users = data['users']
        self.date = data['date']
        self.meal_type = MealType.getMealTypeById(data['meal_type_id'])
    
    def to_json(self):
        data = {
            "id" : self.id,
            "recipes" : self.recipes,
            "users" : self.users,
            "date" : self.date,
            "meal_type" : self.meal_type.to_json()
        }

        return data

    @classmethod
    def addMealToMenu(cls, data):
        query = f"INSERT INTO meals (created_at, updated_at, meal_type_id, date) VALUES (NOW(), NOW(), {data['meal_type_id']}, '{data['date']}')"
        meal_id = MySQLConnection().query_db(query)
        cls.connectMealToUser(meal_id, data['user_id'])
        for recipe in data['recipes']:
            cls.connectRecipeToMeal(meal_id, recipe['id'])
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
                "meal_type_id" : db_data[0]['meal_type_id'],
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
            return cls(data)
        else:
            return False

    @classmethod
    def getUserFutureWeekMeals(cls, user_id, daysDisplayed = 7, startdate= datetime.date.today()):

        enddate = startdate + datetime.timedelta(daysDisplayed)

        query = f"SELECT * FROM users_meals JOIN meals ON meal_id = meals.id WHERE meals.date >= '{startdate}' AND meals.date < '{enddate}' AND user_id = {user_id} ORDER BY meals.date"
        db_data = MySQLConnection().query_db(query)
        meals = []
        for row in db_data:
            meal = cls.getMealById(row['meal_id'])
            weekday = datetime.date.weekday(meal.date)
            meal.date = calendar.day_name[weekday]
            meals.append(meal)

        return meals
    @classmethod
    def getUserFutureMealsByDates(cls, user_id, enddate = datetime.date.today() + datetime.timedelta(7), startdate= datetime.date.today()):
        query = f"SELECT * FROM users_meals JOIN meals ON meal_id = meals.id WHERE meals.date >= '{startdate}' AND meals.date < '{enddate}' AND user_id = {user_id} ORDER BY meals.date"
        db_data = MySQLConnection().query_db(query)
        meals = []
        for row in db_data:
            meal = cls.getMealById(row['meal_id'])
            weekday = datetime.date.weekday(meal.date)
            month = meal.date.month
            day = meal.date.day
            meal.date = f"{calendar.month_abbr[month]} {day} ({calendar.day_abbr[weekday]})"
            meals.append(meal)

        return meals
    
    @classmethod
    def updateMeal(cls, meal):
        query = "UPDATE meals SET date = %(date)s, meal_type_id = %(meal_type_id)s WHERE id = %(id)s"
        MySQLConnection().query_db(query, meal)

        cls.deleteRecipesFromMeal(meal["id"])

        for recipe_id in meal['recipes']:
            cls.connectRecipeToMeal(meal['id'], recipe_id)
        
        meal = cls.getMealById(meal['id'])
        return meal

    @staticmethod
    def deleteRecipesFromMeal(meal_id)-> None:
        query = f"DELETE FROM meals_recipes WHERE meal_id = {meal_id}"
        MySQLConnection().query_db(query)
        return None
    
    @staticmethod
    def deleteUsersFromMeal(meal_id)-> None:
        query = f"DELETE FROM users_meals WHERE meal_id = {meal_id}"
        MySQLConnection().query_db(query)
        return None
    
    @classmethod
    def deleteMealById(cls, meal_id) -> None:
        cls.deleteRecipesFromMeal(meal_id)
        cls.deleteUsersFromMeal(meal_id)
        query = f"DELETE FROM meals WHERE id = {meal_id}"
        MySQLConnection().query_db(query)


class MealType:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
    
    def to_json(self):
        data = {
            "id" : self.id,
            "name" : self.name,
            "description" : self.description
        }
        return data
    
    @classmethod
    def getMealTypeById(cls, id):
        query = f"SELECT * FROM meal_types WHERE id = {id}"
        db_data = MySQLConnection().query_db(query)
        if db_data:
            mealType = cls(db_data[0])
            return mealType
        
        else:
            return None
    
    @classmethod
    def getMealAllMealTYpes(cls):
        query = f"SELECT * FROM meal_types"
        db_data = MySQLConnection().query_db(query)
        mealTypes = []
        if db_data:
            for row in db_data:
                mealTypes.append(cls(row))
            return mealTypes
        
        else:
            return None