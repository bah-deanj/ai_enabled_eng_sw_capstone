INSERT INTO users (username, email, password_hash) VALUES
	('alice', 'alice@example.com', 'hash1'),
	('bob', 'bob@example.com', 'hash2'),
	('carol', 'carol@example.com', 'hash3');

-- Recipes (ingredients as JSON string)
INSERT INTO recipes (user_id, title, description, instructions, ingredients) VALUES
	(1, 'Classic Pancakes', 'Fluffy pancakes perfect for breakfast.', '1. Mix dry ingredients. 2. Add wet ingredients. 3. Cook on griddle.',
	 '[{"name": "Eggs", "quantity": "2"}, {"name": "Flour", "quantity": "1.5 cups"}, {"name": "Milk", "quantity": "1 cup"}, {"name": "Sugar", "quantity": "2 tbsp"}, {"name": "Salt", "quantity": "1/2 tsp"}, {"name": "Butter", "quantity": "2 tbsp"}]'),
	(2, 'Garlic Chicken', 'Simple garlic chicken breast.', '1. Season chicken. 2. Sauté garlic in oil. 3. Cook chicken until done.',
	 '[{"name": "Chicken Breast", "quantity": "2 breasts"}, {"name": "Olive Oil", "quantity": "2 tbsp"}, {"name": "Garlic", "quantity": "3 cloves"}, {"name": "Salt", "quantity": "1/4 tsp"}]');

-- User Favorites
INSERT INTO user_favorites (user_id, recipe_id) VALUES
	(1, 2), -- Alice likes Garlic Chicken
	(2, 1); -- Bob likes Pancakes