from flask_app import app
from flask_app.controllers.views import mainpages, users, images, recipes, meals, shopping_lists
from flask_app.controllers.apis import users, images, recipes, ingredients


if(__name__ == "__main__"):
    app.run(debug=True)