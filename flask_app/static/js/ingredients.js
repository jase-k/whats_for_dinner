console.log('Ingredients is Connected!')

var search_button = document.getElementById('search_ingredients')
search_button.addEventListener('click', searchIngredientList)

var spoonacular_access_key = '8ed850e1602d441a8215de623bacac90'
var search_results_container = document.getElementById('ingredient_search_results')

async function searchIngredientList(){
    query = this.previousElementSibling.value

    url = `https://api.spoonacular.com/food/ingredients/search?apiKey=${spoonacular_access_key}&query=${query}&number=8`
    
    var results = await fetch(url)
    var json = await results.json()
    displayResults(json.results)
}

async function displayResults(results){
    for(var i = 0; i < results.length; i++){
        var child = document.createElement('li')
        child.classList = 'search_result'
        child.value = results[i].id
        child.innerHTML = results[i].name
        child.addEventListener('click', addToList)
        search_results_container.appendChild(child)
    }

}

var search_results = document.getElementsByClassName('search_result')

var table_body = document.getElementById('table_body')
function addToList(){
    console.log(this)
    var row = document.createElement('tr')
    row.innerHTML = `
    <td>0</td>
    <td>${this.innerHTML}</td>
    <td class='hidden'>${this.value}</td>
    `
    table_body.appendChild(row)
}


