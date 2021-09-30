console.log("view_recipe.js is connected")

var recipe_photos = document.getElementsByClassName('recipe_photo');
for(var i = 0; i < recipe_photos.length; i++){
    recipe_photos[i].addEventListener("click", toggleRecipeDeleteForm);
}

function toggleRecipeDeleteForm(){
    this.nextElementSibling.classList.toggle('hidden');
}
