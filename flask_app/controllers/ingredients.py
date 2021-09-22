from flask import redirect, request, session, render_template
from flask_app import app
import os
import urllib.request


@app.route('/search_ingredients')
def searchSpoonacularDatabase():
    access_key = os.getenv('spoonacular_access_key')
    query = 'banana'
    url = f"https://api.spoonacular.com/food/ingredients/search?apiKey={access_key}&query={query}&number=8"

    with urllib.request.urlopen(url) as response:
        html = response.read()
        print(html)

    result = {
        'number' : 8000,
        'os' : access_key,
        'html' : html
    }
    return result
