from flask_app import app
from flask_app.controllers import mainpages, users, images, recipes, meals, ingredients, shopping_lists


if(__name__ == "__main__"):
    app.run(debug=True)