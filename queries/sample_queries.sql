-- Query 1: Search for food by name with complete nutritional information
-- Purpose: Allows users to find detailed information about a specific food
SELECT 
    f.food_name,
    c.category_name,
    n.measure,
    n.grams,
    n.calories,
    n.protein,
    n.fat,
    n.sat_fat,
    n.fiber,
    n.carbs
FROM FOOD f
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
JOIN has_nutrition hn ON f.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE f.food_name ILIKE '%apple%';


-- Query 2: Show all foods in a specific category
-- Purpose: Browse all foods within a particular category (e.g., Fruits, Proteins)
SELECT 
    f.food_id,
    f.food_name,
    c.category_name
FROM FOOD f
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
WHERE c.category_name = 'Fruits'
ORDER BY f.food_name;


-- Query 3: Find high-protein foods (> 20g per serving)
-- Purpose: Help users identify protein-rich foods for their diet
SELECT 
    f.food_name,
    c.category_name,
    n.protein,
    n.calories,
    n.measure
FROM FOOD f
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
JOIN has_nutrition hn ON f.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE n.protein > 20
ORDER BY n.protein DESC;


-- Query 4: Show all foods a specific user has logged
-- Purpose: View a user's complete food history
SELECT 
    u.username,
    f.food_name,
    fi.log_date,
    c.category_name
FROM "USER" u
JOIN FOOD_INFO fi ON u.user_id = fi.user_id
JOIN FOOD f ON fi.food_id = f.food_id
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
WHERE u.username = 'benjamin_mccoy'
ORDER BY fi.log_date DESC;


-- Query 5: Calculate total calories consumed by a user on a specific date
-- Purpose: Track daily caloric intake for a user
SELECT 
    u.username,
    fi.log_date,
    SUM(n.calories) AS total_calories,
    COUNT(DISTINCT fi.food_id) AS foods_logged
FROM "USER" u
JOIN FOOD_INFO fi ON u.user_id = fi.user_id
JOIN has_nutrition hn ON fi.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE u.username = 'benjamin_mccoy' 
    AND fi.log_date = '2025-10-06'
GROUP BY u.username, fi.log_date;

-- Query 6: Count the number of foods in each category
-- Purpose: Provide statistics about database composition
SELECT 
    c.category_name,
    COUNT(bt.food_id) AS food_count
FROM CATEGORY c
LEFT JOIN Belong_to bt ON c.category_id = bt.category_id
GROUP BY c.category_name
ORDER BY food_count DESC;


-- Query 7: Calculate average nutritional values across all foods
-- Purpose: Get baseline nutritional statistics for the database
SELECT 
    ROUND(AVG(n.calories), 2) AS avg_calories,
    ROUND(AVG(n.protein), 2) AS avg_protein,
    ROUND(AVG(n.fat), 2) AS avg_fat,
    ROUND(AVG(n.carbs), 2) AS avg_carbs,
    ROUND(AVG(n.fiber), 2) AS avg_fiber
FROM NUTRITION n;


-- Query 8: Show a user's total nutritional intake for a specific week
-- Purpose: Calculate weekly nutrition summary for progress tracking
SELECT 
    u.username,
    DATE_TRUNC('week', fi.log_date) AS week_start,
    ROUND(SUM(n.calories), 2) AS total_calories,
    ROUND(SUM(n.protein), 2) AS total_protein,
    ROUND(SUM(n.fat), 2) AS total_fat,
    ROUND(SUM(n.carbs), 2) AS total_carbs,
    ROUND(SUM(n.fiber), 2) AS total_fiber,
    COUNT(DISTINCT fi.food_id) AS unique_foods_eaten
FROM "USER" u
JOIN FOOD_INFO fi ON u.user_id = fi.user_id
JOIN has_nutrition hn ON fi.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE u.username = 'benjamin_mccoy'
    AND fi.log_date >= '2025-10-01'
    AND fi.log_date <= '2025-10-07'
GROUP BY u.username, DATE_TRUNC('week', fi.log_date);


-- Query 9: Find the most frequently logged foods across all users
-- Purpose: Identify popular foods in the database
SELECT 
    f.food_name,
    c.category_name,
    COUNT(*) AS log_count,
    COUNT(DISTINCT fi.user_id) AS unique_users
FROM FOOD f
JOIN FOOD_INFO fi ON f.food_id = fi.food_id
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
GROUP BY f.food_name, c.category_name
ORDER BY log_count DESC
LIMIT 10;

-- Query 10: Complete food information profile
-- Purpose: Get all available information about a specific food in one query
SELECT 
    f.food_id,
    f.food_name,
    c.category_name,
    n.measure,
    n.grams,
    n.calories,
    n.protein,
    n.fat,
    n.sat_fat,
    n.fiber,
    n.carbs,
    COUNT(DISTINCT fi.user_id) AS users_who_logged,
    COUNT(fi.log_date) AS total_logs
FROM FOOD f
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
JOIN has_nutrition hn ON f.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
LEFT JOIN FOOD_INFO fi ON f.food_id = fi.food_id
WHERE f.food_name = 'Chicken Breast'
GROUP BY f.food_id, f.food_name, c.category_name, n.measure, n.grams, 
         n.calories, n.protein, n.fat, n.sat_fat, n.fiber, n.carbs;


-- Query 11: User's complete food log with detailed nutrition information
-- Purpose: Generate a comprehensive nutrition report for a user
SELECT 
    u.username,
    u.email,
    fi.log_date,
    f.food_name,
    c.category_name,
    n.measure,
    n.calories,
    n.protein,
    n.fat,
    n.carbs,
    n.fiber
FROM "USER" u
JOIN FOOD_INFO fi ON u.user_id = fi.user_id
JOIN FOOD f ON fi.food_id = f.food_id
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
JOIN has_nutrition hn ON f.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE u.username = 'vivek_sharma'
ORDER BY fi.log_date DESC, f.food_name;


-- Query 12: Find all users who have logged foods from a specific category
-- Purpose: Identify users with dietary preferences or restrictions
SELECT DISTINCT
    u.user_id,
    u.username,
    u.email,
    c.category_name,
    COUNT(DISTINCT fi.food_id) AS foods_from_category,
    MIN(fi.log_date) AS first_log,
    MAX(fi.log_date) AS most_recent_log
FROM "USER" u
JOIN FOOD_INFO fi ON u.user_id = fi.user_id
JOIN FOOD f ON fi.food_id = f.food_id
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
WHERE c.category_name = 'Proteins'
GROUP BY u.user_id, u.username, u.email, c.category_name
ORDER BY foods_from_category DESC;


-- Query 13: Compare nutritional intake between multiple users
-- Purpose: Generate comparative analytics for user groups
SELECT 
    u.username,
    COUNT(DISTINCT fi.food_id) AS total_foods_logged,
    ROUND(AVG(n.calories), 2) AS avg_calories_per_food,
    ROUND(AVG(n.protein), 2) AS avg_protein_per_food,
    ROUND(SUM(n.calories), 2) AS total_calories,
    ROUND(SUM(n.protein), 2) AS total_protein
FROM "USER" u
JOIN FOOD_INFO fi ON u.user_id = fi.user_id
JOIN has_nutrition hn ON fi.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE fi.log_date >= '2025-10-01'
GROUP BY u.username
ORDER BY total_calories DESC;

-- Query 14: Insert a new food log entry for a user
-- Purpose: Record when a user consumes a food item
INSERT INTO FOOD_INFO (user_id, food_id, log_date) 
VALUES (
    (SELECT user_id FROM "USER" WHERE username = 'benjamin_mccoy'),
    (SELECT food_id FROM FOOD WHERE food_name = 'Apple'),
    '2025-10-23'
);


-- Query 15: Update a user's email address
-- Purpose: Allow users to update their contact information
UPDATE "USER"
SET email = 'benjamin.new.email@gmail.com'
WHERE username = 'benjamin_mccoy';


-- Query 16: Delete a specific food log entry
-- Purpose: Remove incorrect or unwanted food log entries
DELETE FROM FOOD_INFO
WHERE user_id = (SELECT user_id FROM "USER" WHERE username = 'benjamin_mccoy')
    AND food_id = (SELECT food_id FROM FOOD WHERE food_name = 'Apple')
    AND log_date = '2025-10-23';


-- Query 17: Insert a new user into the system
-- Purpose: Register a new user account
INSERT INTO "USER" (username, email, registration_date)
VALUES ('john_doe', 'john.doe@example.com', CURRENT_DATE);


