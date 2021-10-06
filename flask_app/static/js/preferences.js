console.log("Preferences.js Connected")

var favorite_togglers = document.getElementsByClassName("favorite_toggle")

for(var i = 0; i < favorite_togglers.length; i++){
    favorite_togglers[i].addEventListener("click", toggleFavorite)
}

async function toggleFavorite(){
    var url = ''
    if(this.innerHTML == "unfavorite"){
        console.log(this.value)
        url = "/recipes/"+this.value+"/unfavorite"
        this.innerHTML = "favorite"
    }
    else{
        url = "/recipes/"+this.value+"/favorite"
        this.innerHTML = "unfavorite"
    }
    data = {
        "recipe_id": this.value
    }

    results = await fetch(url)
}