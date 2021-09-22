console.log('javascript connected!')

var profile_pic = document.getElementById('profile_image')
var cancel_button = document.getElementById('cancel_button')
var delete_form = document.getElementById('delete_photo')
var dropdown_menu = document.getElementById('dropdown')
var menu_button = document.getElementById('menu_bar')
console.log(cancel_button)
cancel_button.addEventListener("click", hideDeleteForm)
profile_pic.addEventListener("click", showDeleteForm)
menu_button.addEventListener("click", toggleDropDown)

function showDeleteForm(){
    delete_form.classList = ['']
}

function hideDeleteForm(){
    delete_form.classList = ['hidden']
}

function toggleDropDown(){
    dropdown_menu.classList.toggle("hidden")
}
