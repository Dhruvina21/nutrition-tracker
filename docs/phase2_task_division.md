# Phase II - Task Division

## Project: Nutrition Tracker Database

**Team Members:** 4 people
**Deadline:** 24th oct, 2025

---

## Task 1: Categories and Sample Foods (Person 1: Sonakshi)

**Responsibility:** Create and populate CATEGORY and FOOD tables

### Files to Create:

- `migrations/02_insert_categories_and_foods.sql`

### Requirements:

1. Insert 8 food categories into CATEGORY table:

   - Fruits
   - Vegetables
   - Proteins
   - Grains
   - Dairy
   - Nuts & Seeds
   - Beverages
   - Snacks

2. Insert 50+ food items into FOOD table (at least 6 foods per category)

3. Insert records into Belong_to table to link each food to its category

### Example SQL Structure:

```sql
-- Insert Categories
INSERT INTO CATEGORY (category_name) VALUES
('Fruits'),
('Vegetables'),
-- ... add all 8 categories

-- Insert Foods
INSERT INTO FOOD (food_name) VALUES
('Apple'),
('Banana'),
-- ... add 50+ foods

-- Link Foods to Categories
INSERT INTO Belong_to (food_id, category_id) VALUES
(1, 1),  -- Apple belongs to Fruits
(2, 1),  -- Banana belongs to Fruits
-- ... link all foods to their categories
```

### Deliverables:

- ✅ SQL file with all INSERT statements
- ✅ At least 8 categories
- ✅ At least 50 food items
- ✅ All foods linked to appropriate categories

---

## Task 2: Nutrition Facts (Person 2: Dhruvina)

**Responsibility:** Create and populate NUTRITION table and link to foods

### Files to Create:

- `migrations/03_insert_nutrition_facts.sql`

### Requirements:

1. Insert 75+ nutrition records into NUTRITION table

   - Some foods should have multiple serving sizes
   - Example: Apple (1 medium = 182g, 1 cup sliced = 125g)

2. Insert records into has_nutrition table to link each nutrition record to its food

3. Use USDA nutritional guidelines for realistic data

### Example SQL Structure:

```sql
-- Insert Nutrition Facts
INSERT INTO NUTRITION (measure, grams, calories, protein, fat, sat_fat, fiber, carbs) VALUES
('1 medium', 182, 95, 0.5, 0.3, 0.1, 4.4, 25),  -- Apple
('1 cup sliced', 125, 65, 0.3, 0.2, 0.0, 3.0, 17),  -- Apple
-- ... add 75+ nutrition records

-- Link Nutrition to Foods
INSERT INTO has_nutrition (food_id, nutrition_id) VALUES
(1, 1),  -- Apple - 1 medium
(1, 2),  -- Apple - 1 cup sliced
-- ... link all nutrition records to foods
```

### Deliverables:

- ✅ SQL file with all INSERT statements
- ✅ At least 75 nutrition records
- ✅ Multiple serving sizes for at least 10 foods
- ✅ All nutrition records linked to foods
- ✅ Realistic nutritional values

---

## Task 3: Sample Users and Food Logs (Person 3: Manya)

**Responsibility:** Create and populate USER table and FOOD_INFO table

### Files to Create:

- `migrations/04_insert_users_and_logs.sql`

### Requirements:

1. Insert 10+ sample users into USER table

   - Use realistic usernames and emails
   - Vary registration dates

2. Insert sample food logs into FOOD_INFO table
   - Each user should have at least 5 food entries
   - Use different log dates
   - Show realistic eating patterns

### Example SQL Structure:

```sql
-- Insert Users
INSERT INTO "USER" (username, email, registration_date) VALUES
('john_doe', 'john@example.com', '2024-01-15'),
('jane_smith', 'jane@example.com', '2024-02-20'),
-- ... add 10+ users

-- Insert Food Logs
INSERT INTO FOOD_INFO (user_id, food_id, log_date) VALUES
(1, 5, '2024-10-01'),  -- john_doe ate food_id 5 on Oct 1
(1, 12, '2024-10-01'),  -- john_doe ate food_id 12 on Oct 1
(1, 3, '2024-10-02'),  -- john_doe ate food_id 3 on Oct 2
-- ... add logs for all users (50+ total entries)
```

### Deliverables:

- ✅ SQL file with all INSERT statements
- ✅ At least 10 users
- ✅ At least 50 food log entries
- ✅ Varied log dates showing realistic patterns

---

## Task 4: SQL Queries (Person 4: Ashna)

**Responsibility:** Create example SQL queries demonstrating the application

### Files to Create:

- `queries/sample_queries.sql`

### Requirements:

Create at least 10 SQL queries that cover:

1. **Search Queries (SELECT):**

   - Search for a food by name and show its nutritional info
   - Show all foods in a specific category
   - Find foods high in protein (> 20g)
   - Show all foods a user has logged
   - Find the total calories consumed by a user on a specific date

2. **Aggregation Queries:**

   - Count foods per category
   - Calculate average calories across all foods
   - Show user's total protein intake for the week

3. **Complex Queries (JOINs):**

   - Show all information about a food (name, category, nutrition facts)
   - Show user's food log with complete nutrition details
   - Find users who logged foods from a specific category

4. **Data Modification (INSERT/UPDATE/DELETE):**
   - Insert a new food entry for a user
   - Update a user's email
   - Delete a food log entry

### Example Query Structure:

```sql
-- Query 1: Search for food by name with complete info
SELECT f.food_name, c.category_name, n.measure, n.calories, n.protein, n.fat, n.carbs
FROM FOOD f
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
JOIN has_nutrition hn ON f.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE f.food_name ILIKE '%apple%';

-- Query 2: Show all foods in 'Fruits' category
-- ... add your query

-- ... add at least 10 queries total
```

### Deliverables:

- ✅ SQL file with at least 10 queries
- ✅ Each query has a comment explaining what it does
- ✅ Queries demonstrate all major application features
- ✅ Include SELECT, INSERT, UPDATE, DELETE examples
- ✅ Test all queries to ensure they work

---

## Workflow Guidelines

### Before Starting Work:

```bash
git pull origin main
```

### After Completing Your Task:

```bash
git add .
git commit -m "Complete Task X: [description]"
git push origin main
```

### Communication:

- Test your SQL file in pgAdmin before committing
- If you encounter issues, ask the team for help
- Coordinate with other team members to avoid conflicts

### Testing Your Work:

1. Run your SQL file in pgAdmin
2. Verify data was inserted correctly
3. Check for any errors
4. Make sure foreign key relationships work

---

## Important Notes:

- **Person 1 should complete their task FIRST** (categories and foods must exist before others can reference them)
- **Person 2 should complete SECOND** (nutrition facts reference foods)
- **Person 3 can work in parallel after Person 1** (users and logs reference foods)
- **Person 4 can start once Persons 1-3 have pushed their data** (queries need data to work with)

## Final Deliverable Checklist:

- [ ] All 4 SQL files created and pushed to GitHub
- [ ] Database contains:
  - [ ] 8 categories
  - [ ] 50+ foods
  - [ ] 75+ nutrition records
  - [ ] 10+ users
  - [ ] 50+ food logs
- [ ] 10+ working SQL queries
- [ ] All team members have tested the complete database
- [ ] Ready for demonstration to instructor/TA

**Good luck, team! 🚀**
