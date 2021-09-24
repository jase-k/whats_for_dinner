console.log('javascript connected!')

var spoonacular_access_key = '8ed850e1602d441a8215de623bacac90'

//search button adding click functionality
document.getElementById('search').addEventListener('click', getRecipes)

//Adds cuisine options to the form on browse_recipes.html
function addCuisines(){
    var selectElement = document.getElementById('cuisines')
    var listOfCuisines = ['African', 'American', 'British', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Irish', 'Italian', 'Japanese', 'Jewish', 'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Southern', 'Spanish', 'Thai', 'Vietnamese']
    for(var i = 0; i < listOfCuisines.length; i++){
        var child = document.createElement('option')
        child.value = listOfCuisines[i]
        child.innerHTML = listOfCuisines[i]
        // console.log(child)
        selectElement.appendChild(child)
    }
}
addCuisines()

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

function displayRecipeResults(results){
    console.log(results)
    var res_div = document.getElementById('search_results')

    for (let i = 0; i < results.length; i++) {
        res_div.innerHTML += `
        <div class="recipe_container">
            <div class="recipe_image w100">
                <img class="image_for_recipe w100" src="${results[i].image}" alt="">
                <img class= "heart_image" src="" alt="">
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
        console.log(res_div)
        res_div.innerHTML += `
        `
        console.log("hey there", i)
    }
}
