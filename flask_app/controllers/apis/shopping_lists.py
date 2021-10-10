from flask import redirect, request, session, render_template
from flask_app import app
from flask_app.models.shopping_list import ShoppingList

@app.route('/generate_list', methods=['POST'])
def getShoppingList() ->object: #JSON
    startdate = request.get_json()['startdate']
    enddate = request.get_json()['enddate']
    listOfIngredients = ShoppingList.getShoppingListInDateRange(session['user_id'], startdate, enddate)
    results = {
        "status" : 200, 
        "results" : listOfIngredients
    }
    return results