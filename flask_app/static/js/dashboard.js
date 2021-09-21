console.log('javascript connected!')

var profile_pic = document.getElementById('profile_image')
var cancel_button = document.getElementById('cancel_button')
var delete_form = document.getElementById('delete_photo')
console.log(cancel_button)
cancel_button.addEventListener("click", hideDeleteForm)
profile_pic.addEventListener("click", showDeleteForm)

function showDeleteForm(){
    delete_form.classList = ['']
}

function hideDeleteForm(){
    delete_form.classList = ['hidden']
}

