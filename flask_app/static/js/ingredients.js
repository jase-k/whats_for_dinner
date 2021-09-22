console.log('Ingredients is Connected!')

var search_button = document.getElementById('search_ingredients')
var search_input = document.getElementById('ingredients')
search_button.addEventListener('click', searchIngredientList)

var spoonacular_access_key = '8ed850e1602d441a8215de623bacac90'
var search_results_container = document.getElementById('ingredient_search_results')

async function searchIngredientList(){
    query = search_input.value

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
    <td><input name = 'quantity' class = 'quantity' type='float'><td>
    <td>
        <select name = 'quantity_type'>
            <option value = 'tbsp'>tbsp</option>
            <option value = 'tsp'>tsp</option>
            <option value = 'c'>c</option>
            <option value = 'ml'>ml</option>
            <option value = 'l'>l</option>
            <option value = 'oz'>oz</option>
            <option value = 'g'>g</option>
            <option value = 'whole'>whole</option>
            <option value = 'slice'>slice</option>
        </select>
    </td>
    <td><input type="text" value="${this.innerHTML}" class='readonly' name='ingredient_list' readonly></td>
    <td><button class='remove_ingredient' type='button'>remove</button></td>
    <td class='hidden'><input type='text' name='spoonacular_id' class='hidden' value=${this.value} ></td>
    `
    console.log(row)
    table_body.appendChild(row)
    hidelist()
    createRemoveButtons()
    search_input.value = ''
}

var ingredient_list_form = document.getElementById('ingredient_list')


function hidelist(){
    var list = document.getElementById('ingredient_search_results')
    list.innerHTML = ''
}

function createRemoveButtons(){
    var buttons = document.getElementsByClassName('remove_ingredient')
    for(var i = 0 ; i < buttons.length; i++){
        buttons[i].addEventListener('click', removeParent)
    }
}
//Calls the function once to set the existing ingredients on the page to dynamically remove themselves
createRemoveButtons()

function removeParent(){
    console.log(this)
    this.parentElement.parentElement.remove()
}
