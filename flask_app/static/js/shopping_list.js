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
    
    for(var i = 0; i < ing_list.results.length; i++){
        table.innerHTML += `
        <tr>
            <td><input type="checkbox" name="ingredients" id="${ing_list.results[i].name}_${ing_list.results[i].quantity_type}"></td>
            <td>${ing_list.results[i].total} ${ing_list.results[i].quantity_type}</td>
            <td><label for="${ing_list.results[i].name}_${ing_list.results[i].quantity_type}" >${ing_list.results[i].name}</label></td>
            <td class="subs">Substitutions</td>
            <td>For Recipe: {{recipe.title}}</td>
        </tr>
        `
    }
}