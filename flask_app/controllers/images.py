from flask import redirect, request
from flask_app import app
from flask_app.models.image import ProfileImage

@app.route('/delete_photo', methods=["POST"])
def deletPhoto(): 
    id = request.form['profile_image_id']

    ProfileImage.deleteImage(id)
    return redirect('/dashboard')