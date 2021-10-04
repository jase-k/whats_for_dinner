console.log('javascript connected!', user_id)


var spoonacular_access_key = '8ed850e1602d441a8215de623bacac90'

//search button adding click functionality
document.getElementById('search').addEventListener('click', getRecipes)
//Stores favorite recipe_ids:
async function getFavorites(){
        const response = await fetch('/recipes/favorites');
        const results = await response.json(); 
        console.log("Favorites: ", results)
        return results  
 }


async function getRecipes(){
    var cuisine_value = document.getElementById('cuisines').value
    var maxReadyTime_value = document.getElementById('maxReadyTime').value
    console.log(maxReadyTime_value)
    if(!maxReadyTime_value){
        maxReadyTime_value = 1440
    }
    var query = `https://api.spoonacular.com/recipes/complexSearch?apiKey=${spoonacular_access_key}&number=10&instructionsRequired=true&addRecipeNutrition=true&fillIngredients=true&cuisine=${cuisine_value}&maxReadyTime=${maxReadyTime_value}`
    console.log(query)
    results = await fetch(query)
    json = await results.json()
    displayRecipeResults(json.results)
}

async function displayRecipeResults(results){
    console.log(results)
    var res_div = document.getElementById('search_results')
    var favorite_ids = await getFavorites();
    console.log("fave length", favorite_ids.length)
    for (let i = 0; i < results.length; i++) {
        var fave_button = `<button class= "save" type="button">Favorite!</button>`
        for(var j = 0; j < favorite_ids.length; j++){
            console.log("comparing id's: " +results[i].id +" vs. "+favorite_ids[j].spoonacular_id )
            if(results[i].id == favorite_ids[j].spoonacular_id){
                fave_button = `<button class="unsave" type="button"> Unfavorite! </button>`
                break
            }
        }
        res_div.innerHTML += `
        <div class="recipe_container">
            <div class="recipe_image w100">
                <img class="image_for_recipe w100" src="${results[i].image}" alt="">
                <input type="hidden" name="spoonacular_id" value="${results[i].id}"/>
                ${fave_button}
            </div>
        <h3 class="recipe_title">${results[i].title}</h3>
        <div class="recipe_information w100">
            <div class="small_information">
                <div class="ingredients w50">
                    <h5>Ingredients</h5>
                    <table class="w100 ing_table">
                    <tbody>
    
                    </tbody>
                    </table>
                </div>
                <div class="nutrition w50">
                    <h5>Nutrition Information:</h5>
                    <table class="w100 nut_table">
                        <tbody class="nutrient_table">
                        
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
</div>`
        var ingredients_table = document.getElementsByClassName('ing_table')

        for(var j = 0;  j < results[i].nutrition.ingredients.length; j++){
            ingredients_table[i].innerHTML +=` 
            <tr>
            <td class="${results[i].nutrition.ingredients[j].name}">${results[i].nutrition.ingredients[j].name}</td>
            <td class="${results[i].nutrition.ingredients[j].amount} ${results[i].nutrition.ingredients[j].unit}">${results[i].nutrition.ingredients[j].amount} ${results[i].nutrition.ingredients[j].unit}</td>
            </tr>
            `
        }
        var nutrient_table = document.getElementsByClassName('nutrient_table')
        for(var k = 0;  k < 9; k++){
            nutrient_table[i].innerHTML +=` 
            <tr>
            <td class="nutrient_name">${results[i].nutrition.nutrients[k].name}</td>
            <td class="nutrient_amount">${results[i].nutrition.nutrients[k].amount} ${results[i].nutrition.nutrients[k].unit}</td>
            <td>${results[i].nutrition.nutrients[k].percentOfDailyNeeds}%</td>
            </tr>
            `
        }
        
        res_div.innerHTML += `
        `
        
    }
    var favorite_buttons = document.querySelectorAll('.save')
    addFavoriteListener(favorite_buttons);
}

function addFavoriteListener(button_array){
    for(var i = 0; i < button_array.length; i++){
        button_array[i].addEventListener("click", favoriteASpoonacularRecipe)
    }
}

async function favoriteASpoonacularRecipe(){
    console.log("click")
    console.log(this.previousElementSibling.value)
    var id = this.previousElementSibling.value
    var url = `https://api.spoonacular.com/recipes/${id}/information?apiKey=${spoonacular_access_key}&includeNutrition=true`
    console.log(url)
    results = await fetch(url)
    json = await results.json()

    data = {
        'title' : json.title,
        'instructions' : json.instructions,
        'description' : json.summary,
        'source' : json.sourceUrl,
        'cuisines' : json.cuisines, //Array
        'ingredients' : [], //Array of Objects added below
        'image' : json.image,
        'recipe_types' : json.dishTypes, //Array
        'spoonacular_id' : id
    }
    for (var i = 0; i < json.nutrition.ingredients.length; i++){
        ingredient = {
            'name' : json.nutrition.ingredients[i].name,
            'quantity' : json.nutrition.ingredients[i].amount,
            'quantity_type' : json.nutrition.ingredients[i].unit,
            'spoonacular_id' : json.nutrition.ingredients[i].id
        }
        data['ingredients'].push(ingredient)
    }
    response = await addRecipeToDB('/favorite_spoonacular_recipe', data)
    console.log(response)
}

async function addRecipeToDB(url = '', data = {}){
    console.log(data)
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', 
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', 
        headers: {
            'Content-Type': 'application/json'
            },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data)
    });

    return response.json(); // parses JSON response into native JavaScript objects
}
