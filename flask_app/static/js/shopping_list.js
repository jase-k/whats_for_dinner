console.log("ShoppingList JS connected")
generate_button = document.getElementById('generate_list')

generate_button.addEventListener("click", showList)

async function showList(){
    var url = "/generate_list"
    data = {
        "startdate": document.getElementById('startdate').value,
        "enddate": document.getElementById('enddate').value
    }
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
    var ing_list = await response.json()
    
    console.log(ing_list)
    var table = document.getElementById('shopping_list_table')
    var ing_list = ing_list.results
    
    for(var i = 0; i < ing_list.length; i++){
        var recipeHtmlString = "" //Resets the recipe html string
        //Loops through the meals the ingredient is apart of
        for(var j = 0; j < ing_list[i].meals.length; j++){
            var meal = ing_list[i].meals
            console.log(meal)
            //loops through the recipes in the meal
            for(var k = 0; k < meal[j].recipes.length; k++){
                var recipe = meal[j].recipes[k]
                var recipeHtmlString = `${recipeHtmlString} <a href="/recipes/${recipe.id}">${recipe.title}</a> on ${meal[j].date} <br>`
            }
            
        }

        table.innerHTML += `
        <tr>
            <td><input type="checkbox" name="ingredients" id="${ing_list[i].name}_${ing_list[i].quantity_type.name}"></td>
            <td>${ing_list[i].total} ${ing_list[i].quantity_type.name}</td>
            <td><label for="${ing_list[i].name}_${ing_list[i].quantity_type.name}" >${ing_list[i].name}</label></td>
            <td class="subs">Substitutions</td>
            <td class="for_recipe">For Recipe: <br> ${recipeHtmlString} </td>
        </tr>
        `
        
    }
}