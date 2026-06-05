
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    default_unit VARCHAR NOT NULL,
    image_path VARCHAR NOT NULL,
    description VARCHAR
);

CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS storage_locations (
    location_id INTEGER PRIMARY KEY,
    location_name VARCHAR UNIQUE NOT NULL,
    temperature_type VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS stores (
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR UNIQUE NOT NULL,
    store_type VARCHAR
);

CREATE TABLE IF NOT EXISTS fridge_items (
    item_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    location_id INTEGER NOT NULL REFERENCES storage_locations(location_id),
    quantity DOUBLE NOT NULL CHECK(quantity >= 0),
    unit VARCHAR NOT NULL,
    expiry_date DATE NOT NULL,
    status VARCHAR NOT NULL DEFAULT '보관',
    memo VARCHAR
);

CREATE TABLE IF NOT EXISTS ingredient_categories (
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    PRIMARY KEY (ingredient_id, category_id)
);

CREATE TABLE IF NOT EXISTS purchase_records (
    purchase_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES fridge_items(item_id),
    store_id INTEGER REFERENCES stores(store_id),
    purchase_date DATE NOT NULL,
    price INTEGER NOT NULL DEFAULT 0 CHECK(price >= 0)
);

CREATE TABLE IF NOT EXISTS item_consumptions (
    consumption_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES fridge_items(item_id),
    consumed_quantity DOUBLE NOT NULL CHECK(consumed_quantity > 0),
    consumption_date DATE NOT NULL,
    memo VARCHAR
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id INTEGER PRIMARY KEY,
    tag_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredient_tags (
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    tag_id INTEGER NOT NULL REFERENCES tags(tag_id),
    PRIMARY KEY (ingredient_id, tag_id)
);

CREATE TABLE IF NOT EXISTS allergens (
    allergen_id INTEGER PRIMARY KEY,
    allergen_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredient_allergens (
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    allergen_id INTEGER NOT NULL REFERENCES allergens(allergen_id),
    PRIMARY KEY (ingredient_id, allergen_id)
);

CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY,
    recipe_name VARCHAR UNIQUE NOT NULL,
    description VARCHAR
);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER NOT NULL REFERENCES recipes(recipe_id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    required_quantity DOUBLE,
    unit VARCHAR,
    PRIMARY KEY (recipe_id, ingredient_id)
);

CREATE TABLE IF NOT EXISTS meal_plans (
    plan_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    recipe_id INTEGER NOT NULL REFERENCES recipes(recipe_id),
    plan_date DATE NOT NULL,
    meal_type VARCHAR
);

CREATE TABLE IF NOT EXISTS waste_records (
    waste_id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES fridge_items(item_id),
    waste_date DATE NOT NULL,
    quantity DOUBLE NOT NULL CHECK(quantity > 0),
    reason VARCHAR
);

CREATE TABLE IF NOT EXISTS favorite_ingredients (
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, ingredient_id)
);
