from flask import redirect, request
from flask_app import app
from flask_app.models.image import Image

@app.route('/delete_photo', methods=["POST"])
def deletPhoto(): 
    id = request.form['profile_image_id']

    Image.deleteImage(id)
    return redirect('/dashboard')