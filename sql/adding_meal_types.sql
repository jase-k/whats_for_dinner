-- Create table meal_types (id int not null, created_at datetime, updated_at datetime, name varchar(60), description varchar(255))
INSERT INTO meal_types (created_at, updated_at, name, description) VALUES(NOW(), NOW(), "breakfast", "First meal of the day");
INSERT INTO meal_types (created_at, updated_at, name, description) VALUES(NOW(), NOW(), "lunch", "Main meal around midday");
INSERT INTO meal_types (created_at, updated_at, name, description) VALUES(NOW(), NOW(), "dinner", "Main meal in the evening");
INSERT INTO meal_types (created_at, updated_at, name, description) VALUES(NOW(), NOW(), "snack", "Eaten throughout the day. Typically easy to make");
INSERT INTO meal_types (created_at, updated_at, name, description) VALUES(NOW(), NOW(), "special occasion", "Eating with friends and family or need to impress");