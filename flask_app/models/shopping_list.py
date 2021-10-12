from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request
from flask_app.models.ingredient import QuantityType
from flask_app.models.meal import Meal, MealType
from flask_app.models.user import User
from datetime import date
import datetime
import calendar

class ShoppingList: 
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.items = [] #List of items
        # {
        #     "quantity" : ______,
        #     "quantity_type" : ______,
        #     "item" : ______{},
        #     "meal" : ______,
        #     "recipe" : ______,
        # }

    def to_json(self):
        pass

    @classmethod
    def getShoppingListInDateRange(cls, user_id, startdate, enddate, clearList = False) -> object:
        #clearList determines whether items in the shopping list should be deleted before adding to the list
        #returns JavaScript
        user = User.getUserById(user_id, False)
        if not user.shopping_list_id:
            user.shopping_list_id = cls.addNewShoppingToDB()
            #####SHOULD UPDATE TO MENU -> MENU AUTO IS CONNECTED TO THE SHOPPING LIST



        ingredientList = cls.getIngredientList(user_id, startdate, enddate)
        ingredientList = cls.consolodateIngredientList(ingredientList)
        #consolodate ingredients
        # cls.addItems(listOfIngredients)
        #create a ShoppingList Instance
        
        #Return JavaScript Object
        return ingredientList

    @staticmethod
    def consolodateIngredientList(listOfIngredients):
        x = 0 
        while x is not len(listOfIngredients):
            if(listOfIngredients[x]['id'] == listOfIngredients[x-1]['id']) and (listOfIngredients[x]['quantity_type'] == listOfIngredients[x-1]['quantity_type']):
                listOfIngredients[x]['total'] += listOfIngredients[x-1]['total']

                #if meal already listed on the ingredient. Don't add. else add to recipes list
                for meal in listOfIngredients[x-1]['meals']:
                    # print("MEAL", listOfIngredients)
                    if(meal["id"] == listOfIngredients[x]["meals"][0]["id"]):
                        print("STOP", listOfIngredients[x]['meals'][0]['recipes'][0])
                        if(any(recipe['id'] == listOfIngredients[x]['meals'][0]['recipes'][0]['id'] for recipe in meal["recipes"])):
                            #add recipe to current ListOfIngredients meal
                            listOfIngredients[x]['meals'][0]['recipes'] += meal['recipes']
                    else:
                        listOfIngredients[x]['meals'].append(meal)
                        
                del listOfIngredients[x-1]
            else:
                x += 1
        
        return listOfIngredients

    @staticmethod
    def getIngredientList(user_id, startdate, enddate):
        ingredientList = []
        query = f"SELECT * FROM ingredients LEFT JOIN recipes_ingredients ON ingredients.id = recipes_ingredients.ingredient_id LEFT JOIN recipes ON recipes.id = recipes_ingredients.recipe_id LEFT JOIN meals_recipes ON meals_recipes.recipe_id = recipes.id LEFT JOIN meals ON meals.id = meals_recipes.meal_id JOIN users_meals ON users_meals.meal_id = meals.id LEFT JOIN users ON users.id = users_meals.user_id WHERE users.id = {user_id} AND meals.date > '{startdate}' AND meals.date < '{enddate}' ORDER BY ingredients.name ASC, recipes_ingredients.quantity_type ASC"

        db_data = MySQLConnection().query_db(query)
        print(db_data)
        for row in db_data:
            weekday = datetime.date.weekday(row['date'])
            month = row['date'].month
            day = row['date'].day
            row['date']= f"{calendar.month_abbr[month]} {day} ({calendar.day_abbr[weekday]})"

            ingredient = {
                "id" : row["id"],
                "name" : row["name"],
                "total" : row['quantity'],
                "quantity_type" : row['quantity_type'],
                "meals" : [ {
                    "id": row['meals.id'],
                    "date" : row['date'],
                    "type" : MealType.getMealTypeById(row['meal_type_id']).to_json(),
                    "recipes" : [ {
                        "id" : row['recipes.id'],
                        "title" : row['title'],
                        "quantity" : row['quantity'],
                        "quantity_type" : row['quantity_type'],
                    } ]
                }
                ]
            }
            ingredientList.append(ingredient)
        return ingredientList

    @classmethod
    def addItems(listOfItems):
        #Create a new table f
        pass


    @staticmethod
    def addNewShoppingToDB() -> int:
        query = "INSERT INTO shopping_lists (created_at, updated_at) VALUES(NOW(), NOW())"
        shopping_list_id = MySQLConnection().query_db(query)
        return shopping_list_id
    
    @staticmethod
    def addUserToShoppingList(user_id, list_id) -> None:
        query = f"UPDATE users SET shopping_list_id = {list_id} WHERE id = {user_id}"
        MySQLConnection().query_db(query)


class ShoppingListItems:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.quantity = data["quantity"]
        self.quantity_type = QuantityType.getQuantityTypeById(data['quantity_type_id'])
        self.name = data['name']
        self.boughten = data['boughten'] #Boolean
        self.meal_id = data["meal_id"]
        self.recipe_id = data["recipe_id"]