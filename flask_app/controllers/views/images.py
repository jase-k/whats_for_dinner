from flask import redirect, request, render_template
from flask.globals import session
from flask_app import app
from flask_app.models.image import ProfileImage, RecipeImage
from flask_app.models.user import User


@app.route('/<int:user_id>/photos')
def showAllPhotos(user_id):
    profile_images = ProfileImage.getImagesByCreator(user_id)
    recipe_images = RecipeImage.getImagesByCreator(user_id)
    user = User.getUserById(user_id)
    session['url'] = request.url
    print(session)
    return render_template('user/user_photos.html', profile_images = profile_images, recipe_images = recipe_images, user = user)