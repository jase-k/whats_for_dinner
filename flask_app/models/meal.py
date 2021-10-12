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
        self.menu_id = data['menu_id']
        self.date = data['date']
        self.meal_type = MealType.getMealTypeById(data['meal_type_id'])
    
    def to_json(self):
        data = {
            "id" : self.id,
            "recipes" : self.recipes,
            "date" : self.date,
            "meal_type" : self.meal_type.to_json()
        }

        return data

    @classmethod
    def addMealToMenu(cls, data):
        query = f"INSERT INTO meals (created_at, updated_at, meal_type_id, date, menu_id) VALUES (NOW(), NOW(), {data['meal_type_id']}, '{data['date']}', {data['menu_id']})"
        meal_id = MySQLConnection().query_db(query)
        for recipe in data['recipes']:
            cls.connectRecipeToMeal(meal_id, recipe['id'])
        return cls.getMealById(meal_id)
    

    @staticmethod
    def connectRecipeToMeal(meal_id, recipe_id):
        query = f"INSERT INTO meals_recipes (created_at, updated_at, recipe_id, meal_id) VALUES (NOW(), NOW(), {recipe_id}, {meal_id})"
        id = MySQLConnection().query_db(query)
        return id

    @classmethod
    def getMealById(cls, meal_id):
        query = f"SELECT * FROM meals LEFT JOIN meals_recipes ON meals_recipes.meal_id = meals.id WHERE meals.id = {meal_id}"
        db_data = MySQLConnection().query_db(query)

        if db_data:
            data = {
                "id" : db_data[0]['id'],
                "date" : db_data[0]['date'],
                "meal_type_id" : db_data[0]['meal_type_id'],
                "menu_id" : db_data[0]['menu_id'],
                "recipes" : []
            }
            recipe_ids = []
            for row in db_data:
                if row["recipe_id"] not in recipe_ids:
                    data["recipes"].append(Recipe.getRecipeById(row["recipe_id"]))
                    recipe_ids.append(row["recipe_id"])
            return cls(data)
        else:
            return False

    @classmethod
    def getUserFutureWeekMeals(cls, menu_id, daysDisplayed = 7, startdate= datetime.date.today()):

        enddate = startdate + datetime.timedelta(daysDisplayed)

        query = f"SELECT * FROM meals WHERE meals.date >= '{startdate}' AND meals.date < '{enddate}' AND menu_id = {menu_id} ORDER BY meals.date"

        db_data = MySQLConnection().query_db(query)
        meals = []
        for row in db_data:
            meal = cls.getMealById(row['id'])
            weekday = datetime.date.weekday(meal.date)
            meal.date = calendar.day_name[weekday]
            meals.append(meal)

        return meals
    @classmethod
    def getUserFutureMealsByDates(cls, menu_id, enddate = datetime.date.today() + datetime.timedelta(7), startdate= datetime.date.today()):
        query = f"SELECT * FROM meals WHERE meals.date >= '{startdate}' AND meals.date < '{enddate}' AND menu_id = {menu_id} ORDER BY meals.date"
        db_data = MySQLConnection().query_db(query)
        meals = []
        for row in db_data:
            meal = cls.getMealById(row['id'])
            weekday = datetime.date.weekday(meal.date)
            month = meal.date.month
            day = meal.date.day
            meal.date = f"{calendar.month_abbr[month]} {day} ({calendar.day_abbr[weekday]})"
            meals.append(meal)

        return meals
    
    @classmethod
    def updateMeal(cls, meal):
        query = f"UPDATE meals SET date = '{meal['date']}', meal_type_id = {meal['meal_type_id']} WHERE id = {meal['meal_id']}"
        MySQLConnection().query_db(query)

        cls.deleteRecipesFromMeal(meal["meal_id"])

        for recipe in meal['recipes']:
            cls.connectRecipeToMeal(meal['meal_id'], recipe['id'])
        
        meal = cls.getMealById(meal['meal_id'])
        return meal

    @staticmethod
    def deleteMealById(meal_id) -> None:
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