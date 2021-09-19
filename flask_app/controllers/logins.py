from flask_app import app

@app.route("/login")
def login():
    return "This is the Login in Page"
