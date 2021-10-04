Create Table recipe_types (id INT, created_at datetime, updated_at datetime, name VARCHAR(45), description VARCHAR(255));
INSERT INTO recipe_types (name, description) VALUES("main", "Main focus of the meail. May be complimented with a few sides or a stand alone meal");
INSERT INTO recipe_types (name, description) VALUES("side", "Not ideal for the a full meal, but compliments the main course. Could possibly be used as a snack");
INSERT INTO recipe_types (name, description) VALUES("dessert", "Indulgence after the meal. (Or before if you wish) Typically not as filling and sweeter than sides.");
INSERT INTO recipe_types (name, description) VALUES("snack", "Something quick to eat inbetween meal times. Usually bought or prepared ahead of time");
INSERT INTO recipe_types (name, description) VALUES("breakfast", "Ate in the morning or as first meal of the day... but let's be real there is no shame in having breakfast for dinner");
INSERT INTO recipe_types (name, description) VALUES("brunch", "Typically heavier meal than breakfast, but eaten later in the morning.");
INSERT INTO recipe_types (name, description) VALUES("special occasion", "Recipes that are harder to make and reserved for special occasions like holidays or friend/family gatherings");
INSERT INTO recipe_types (name, description) VALUES("appetizer", "Typically eaten prior to the main course. Made ahead of the full meal to enjoy.");
INSERT INTO recipe_types (name, description) VALUES("bread", "Any recipe made into a loaf (except for meatloaf)");
INSERT INTO recipe_types (name, description) VALUES("salad", "Recipes that contains raw ingredients mixed altogether");
INSERT INTO recipe_types (name, description) VALUES("soup", "Served in a bowl with broth");
INSERT INTO recipe_types (name, description) VALUES("beverage", "Anything you drink in a cup!");
INSERT INTO recipe_types (name, description) VALUES("sauce", "Made for dipping or pour over");
INSERT INTO recipe_types (name, description) VALUES("marinade", "A sauce, typically made of oil, vinegar, spices, and herbs, in which meat, fish, or other food is soaked before cooking in order to flavor or soften it.");
INSERT INTO recipe_types (name, description) VALUES("fingerfood", "Recipes that don't require silverware to eat!");
-- main course
-- side dish
-- dessert
-- breakfast
-- snack

-- appetizer
-- salad
-- bread
-- soup
-- beverage
-- sauce
-- marinade
-- fingerfood
-- drink