# whats_for_dinner

# Next Steps
1. Have the favorite button on view_recipe to toggle favoriting and unfavoriting a recipe
2. Get the favorite recipe button to show up on the browse recipes
Add Cuisine Types to Database and Add/Edit Recipe
Fix Update/Add Recipe Code Structure
Add image to Recipe
Delete image from Recipe if image owner
See all Uploaded images
Add source attribute to recipes: e.g.(Website it comes from vs What's for Dinner Platform)

# Generate Meal Plan for the Week
Add recipe type on Upate and ADD recipe methods
Add recipe type ['main', 'side', 'dessert', 'snack', 'breakfast', 'brunch', 'special occasion'] 
Show Recipe Types and Cuisines on View Recipe View
*Fix Image holder getting added to DB and Server when user doesn't add a file*
Add recipe from spoonacular API into database when favoriting a recipe
Have the browse recipes favorite button save to the database if not already there. 
Show 'unfavorite' button for recipes already in favorites
*Split Controller files up into 'API' vs 'View' Controllers*
Add recipe_types to 'add_recipe'
be able to unfavorite recipe from preferences
Add Meals to Recipe Relationship
Add Meal API route created
Add mealtypes ['lunch', 'dinner', 'snack', etc.]
Show Menu on Dashboard
Render menu based on dates
Edit, View, Menu Meals
Ability to add X number of recipes to meal
Delete Menu Meals
Fix edit.html to update menu Need a new route

# Generate Shopping List
*Generate a new Shopping List if currently not in DB*
Populate a Shopping List based on Meal plan for the week. 
*Show what recipes the ingredient is for
Change quantity_type to a seperate table so it can be referred by id
Change View_recipe.html to generate the name of the quantity instead of id
Change users_meals to menus_meals to support more than one user having the same meals
*fix profile photo preference bug
Fix spoonacular id going to 0
-> 
combine wet and dry ingredients
*Keep Track of what you've gotten and what you need*
*Add Your Own items to Shopping List*
Add Optional Ingredients
If get a substitute of an ingredient, mark that on the recipe that was substituted (This will need to be a new table)
Show (For Dinner on Sat, Oct 14, Recipe: *Recipe.Title*)
Clear List prior to generating a new one

# Auto-Generate a Meal Plan
Add Menu Options to Preferences
Add 'add to meal button' on browse Recipes'
Add User Menu's Functionality (Ability to Swap out Meals or Randomize one)
Be able to generate meal plan for specific dates

# Ingredient/Recipe Details
Food Groups ['vegetables', 'fruits', 'meat', 'grains', 'oils', 'sweets']
Good to Have on Hand: 


# Tag list 
['high protein', 'gluten-free', 'low-calorie', 'on-the-go']
Incorporate Cost Tags for ingredients: ["low-cost", "medium-cost", "high-cost" ]
Let Users generate their own tags and organize them. 

# Images
Be Able to display user images or source images. May have to change the way you store images. Look into flask folder creation and using url_for

# Recipe Sorting / Filing / Searching
Add diet types as a function of recipes
Add Weight Watchers Score
Deal with duplicate Recipe Names
Add Prep time, Cook Time, and make time
Give notification a day prior if meal requires prep work

# Other Features
Be able to plan for company coming over
Premium chef selected meals
sort shopping list by recipe or by grocery aisle