-- Nutrition Tracker Database Schema
-- Phase II: ER-to-Relational Transformation

-- Drop tables if they exist (for clean testing)
DROP TABLE IF EXISTS FOOD_INFO CASCADE;
DROP TABLE IF EXISTS has_nutrition CASCADE;
DROP TABLE IF EXISTS Belong_to CASCADE;
DROP TABLE IF EXISTS NUTRITION CASCADE;
DROP TABLE IF EXISTS FOOD CASCADE;
DROP TABLE IF EXISTS CATEGORY CASCADE;
DROP TABLE IF EXISTS "USER" CASCADE;

-- Create USER table
CREATE TABLE "USER" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    registration_date DATE DEFAULT CURRENT_DATE
);

-- Create CATEGORY table
CREATE TABLE CATEGORY (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL
);

-- Create FOOD table
CREATE TABLE FOOD (
    food_id SERIAL PRIMARY KEY,
    food_name VARCHAR(100) NOT NULL
);

-- Create NUTRITION table
CREATE TABLE NUTRITION (
    nutrition_id SERIAL PRIMARY KEY,
    measure VARCHAR(50),
    grams DECIMAL(10, 2),
    calories DECIMAL(10, 2),
    protein DECIMAL(10, 2),
    fat DECIMAL(10, 2),
    sat_fat DECIMAL(10, 2),
    fiber DECIMAL(10, 2),
    carbs DECIMAL(10, 2)
);

-- Create Belong_to relationship table (Food belongs to Category)
CREATE TABLE Belong_to (
    food_id INTEGER REFERENCES FOOD(food_id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES CATEGORY(category_id) ON DELETE CASCADE,
    PRIMARY KEY (food_id, category_id)
);

-- Create has_nutrition relationship table (Food has Nutrition)
CREATE TABLE has_nutrition (
    food_id INTEGER REFERENCES FOOD(food_id) ON DELETE CASCADE,
    nutrition_id INTEGER REFERENCES NUTRITION(nutrition_id) ON DELETE CASCADE,
    PRIMARY KEY (food_id, nutrition_id)
);

-- Create FOOD_INFO relationship table (User logs Food)
CREATE TABLE FOOD_INFO (
    user_id INTEGER REFERENCES "USER"(user_id) ON DELETE CASCADE,
    food_id INTEGER REFERENCES FOOD(food_id) ON DELETE CASCADE,
    log_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (user_id, food_id, log_date)
);

-- Success message
SELECT 'Database schema created successfully!' AS status;