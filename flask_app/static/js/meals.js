console.log('Meals.js Connected')

//Gets favorite Recipes for the datalist
async function fillDataList(){
    var url = '/recipes/all_favorites'
    var results = await fetch(url)
    var json = await results.json()
    console.log(json)
}
fillDataList()

//Adds Recipe to meal