from flask_app.models.image import Image
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request, session
from flask_app.models.ingredient import Ingredient
from flask_app.models.image import Image
from flask_app.models.user import User

class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = {}
        self.title = data['title']
        self.instructions = data['instructions']
        self.description = data['description']
        self.premium = data['premium']
        self.ingredients = []
        self.creator = []

    @staticmethod
    def addRecipe(data):
        query = "INSERT INTO recipes (created_at, updated_at, creator_id, title, instructions, premium, description) VALUES(NOW(), NOW(), %(user_id)s, %(title)s, %(instructions)s, %(premium)s, %(description)s)"

        recipe_id = MySQLConnection().query_db(query, data)

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
        query = f"SELECT * FROM recipes LEFT JOIN recipes_ingredients ON recipes.id = recipes_ingredients.recipe_id LEFT JOIN ingredients ON recipes_ingredients.ingredient_id = ingredients.id LEFT JOIN users ON recipes.creator_id = users.id LEFT JOIN images ON users.profile_image_id = images.id WHERE recipes.id = {id}"
        
        raw_data = MySQLConnection().query_db(query)

        if raw_data: 
            recipe = cls(raw_data[0])
            user = {  
                'id' : raw_data[0]['users.id'],
                'first_name' : raw_data[0]['first_name'],
                'last_name' : raw_data[0]['last_name'],
                'email' : raw_data[0]['email'],
                'phone' : raw_data[0]['phone'],
                'password' : raw_data[0]['password'], #will come from the database hashed,
                'created_at' : raw_data[0]['users.created_at'],
                'updated_at' : raw_data[0]['users.updated_at'],
                'menu_id' : raw_data[0]['menu_id'],
                'shopping_list_id' : raw_data[0]['shopping_list_id'],
                'profile_image_id' : raw_data[0]['profile_image_id']
                    }
            recipe.creator = User(user)
            image = {
                'id' : raw_data[0]['images.id'],
                'created_at' : raw_data[0]['images.created_at'],
                'updated_at' : raw_data[0]['images.updated_at'],
                'owner_user_id' : raw_data[0]['owner_user_id'],
                'file_path' : raw_data[0]['file_path']
            }
            recipe.creator[0].profile_image = (Image(image))
            print("THIS IS THE IMAGE: ", recipe.creator[0].profile_image)

            for row in raw_data:
                ingredient = {
                    'id' : row['ingredients.id'],
                    'created_at' : row['ingredients.created_at'],
                    'updated_at' : row['ingredients.updated_at'],
                    'name' : row['name'],
                    'allergy_id' : row['allergy_id'],
                    'spoonacular_id' : row['spoonacular_id'],
                    'recipe_id': recipe.id
                }
                recipe.ingredients.append(Ingredient(ingredient))


            # print(raw_data)
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


