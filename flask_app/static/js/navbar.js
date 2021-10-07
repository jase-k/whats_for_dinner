console.log('javascript connected!')

var profile_pic = document.getElementById('profile_image')
var cancel_button = document.getElementById('cancel_button')
var delete_form = document.getElementById('delete_photo')
var dropdown_menu = document.getElementById('dropdown')
var menu_button = document.getElementById('menu_bar')
console.log(cancel_button)
profile_pic.addEventListener("click", toggleDeleteForm)
menu_button.addEventListener("click", toggleDropDown)


function toggleDeleteForm(){
    delete_form.classList.toggle('hidden')
}

function toggleDropDown(){
    if(dropdown_menu.hidden == true){
        dropdown_menu.hidden = false;
    }
    else{
        dropdown_menu.hidden = true
    }
}
