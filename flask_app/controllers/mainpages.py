from flask_app import app

@app.route('/')
def mainPage():
    return "This page is being built"