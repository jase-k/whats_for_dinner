console.log('Meals.js Connected')
var recipe_list = []
//Gets favorite Recipes for the datalist
async function fillDataList(){
    var url = '/recipes/all_favorites'
    var results = await fetch(url)
    var json = await results.json()
    console.log(json)
}
fillDataList()

//Adds Recipe to meal
var add_button = document.getElementById('add_button')
add_button.addEventListener("click", addRecipeToMeal)
async function addRecipeToMeal(){
    
    var recipe_select = document.getElementById("recipe_list").value
    var recipe = await fetch(`/api/recipe/${recipe_select}`)
    var json = await recipe.json()
    console.log(json)

    //Add to global variable to send to the DB upon 'saving' the meal
    recipe_list.push(json)
    //Add to ul
    var ul = document.getElementById('recipe_ul')
    var nn = document.createElement('li')
    ul.appendChild(nn)

    //Add more details as needed
    nn.innerHTML = `
    <details>
        <summary>${json.title}</summary>
            <details>
                <summary>Description</summary>
                <p>
                    ${json.description}
                </p>
            </details>
            <details>
                <summary>Types</summary>
                <p>
                    ${json.recipe_types[0].name}
                </p>
            </details>
    </details> `

}
var submitButton = document.getElementById('submit')
submitButton.addEventListener("click", submitMeal)
async function submitMeal(){
    //Collect Form Data
    var date = document.getElementById('date').value
    if(date == ""){
        alert("Must Select a Date!")
        return
    }
    data = {
        "date" : date,
        "meal_type_id": document.getElementById('meal_type').value,
        "recipes" : recipe_list
    }
    
    var response =  await addMealToDB(data)
    await redirectPage(response)
}

async function addMealToDB(data = {}){
    console.log(data)
    // Default options are marked with *
    const response = await fetch('/add_meal', {
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

    return response.json(); 
}

async function redirectPage(response){
    if(response.status == "success"){
        location.replace("menu")
    }
    else{
        alert("Failded to Add to Menu", response.status)
    }
}

