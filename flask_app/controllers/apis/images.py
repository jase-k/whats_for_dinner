from flask import redirect, request, render_template
from flask.globals import session
from flask_app import app
from flask_app.models.image import ProfileImage

@app.route('/delete_photo', methods=["POST"])
def deletPhoto(): 
    id = request.form['photo_id']

    ProfileImage.deleteImage(id)
    if 'url' in session: 
        return redirect(session['url'])
    return redirect('/dashboard')
