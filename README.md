# Nutrition Tracker - Database Project

A PostgreSQL-based nutrition tracking and food database management system.

## 📋 Project Overview

This system enables users to:
- Track dietary intake
- Search nutritional information for foods
- Maintain healthy eating practices
- Browse an extensive food database organized by categories

## 🗄️ Database Schema

**Entities:**
- **USER**: User accounts with credentials
- **CATEGORY**: Food categories (Fruits, Vegetables, Proteins, etc.)
- **FOOD**: Food items database
- **NUTRITION**: Nutritional information per serving
- **FOOD_INFO**: User food consumption logs
- **Belong_to**: Links foods to categories
- **has_nutrition**: Links foods to their nutrition facts

## 🚀 Quick Start for Team Members

### 1. Clone the Repository
```bash
git clone https://github.com/Dhruvina21/nutrition-tracker.git
cd nutrition-tracker
```

### 2. Setup PostgreSQL Database

**Using pgAdmin 4:**
1. Open pgAdmin 4
2. Right-click on "Databases" → Create → Database
3. Name it: `nutrition_tracker`
4. Click "Save"

### 3. Run the Database Schema
1. In pgAdmin, select the `nutrition_tracker` database
2. Open Query Tool (Tools → Query Tool)
3. Open file: `migrations/01_create_tables.sql`
4. Click Execute (▶️ button)

### 4. Run Your Task's SQL File
Once you complete your assigned task (see `docs/phase2_task_division.md`):
1. Save your SQL file in the appropriate folder
2. Run it in pgAdmin Query Tool
3. Verify the data was inserted correctly

## 📁 Project Structure
```
nutrition-tracker/
├── migrations/           # Database schema and data insertion files
│   ├── 01_create_tables.sql
│   ├── 02_insert_categories_and_foods.sql
│   ├── 03_insert_nutrition_facts.sql
│   └── 04_insert_users_and_logs.sql
├── queries/             # Sample SQL queries
│   └── sample_queries.sql
├── docs/               # Documentation
│   ├── setup_guide.md
│   └── phase2_task_division.md
└── README.md          # This file
```

## 📝 Phase II Tasks

**See `docs/phase2_task_division.md` for detailed task assignments:**
- **Task 1:** Categories and Foods (Person 1) - **DO THIS FIRST**
- **Task 2:** Nutrition Facts (Person 2) - **DO THIS SECOND**
- **Task 3:** Users and Food Logs (Person 3) - Can start after Task 1
- **Task 4:** SQL Queries (Person 4) - Do this last

## 🔄 Git Workflow

### Daily Workflow:

**Before starting work:**
```bash
git pull origin main
```

**After completing work:**
```bash
git add .
git commit -m "Descriptive message about your changes"
git push origin main
```

### Good Commit Messages:
- ✅ "Add 8 food categories and 52 food items"
- ✅ "Complete nutrition facts for all fruits and vegetables"
- ✅ "Add 10 sample queries with comments"
- ❌ "update"
- ❌ "done"

## 🧪 Testing Your Work

### In pgAdmin Query Tool:

**Check if your data was inserted:**
```sql
-- See all categories
SELECT * FROM CATEGORY;

-- See all foods
SELECT * FROM FOOD;

-- See all nutrition records
SELECT * FROM NUTRITION;

-- See all users
SELECT * FROM "USER";

-- Count records in each table
SELECT 'Categories' as table_name, COUNT(*) FROM CATEGORY
UNION ALL
SELECT 'Foods', COUNT(*) FROM FOOD
UNION ALL
SELECT 'Nutrition', COUNT(*) FROM NUTRITION
UNION ALL
SELECT 'Users', COUNT(*) FROM "USER";
```

## 📊 Database Requirements (Phase II)

- [x] ER diagram → Relational schema (01_create_tables.sql)
- [ ] 8 food categories
- [ ] 50+ food items
- [ ] 75+ nutrition records
- [ ] 10+ sample users
- [ ] 50+ food log entries
- [ ] 10+ SQL queries

## 🆘 Troubleshooting

### Problem: "relation does not exist"
- **Solution:** Make sure you ran `01_create_tables.sql` first

### Problem: "foreign key constraint violation"
- **Solution:** Insert parent records first (e.g., insert FOOD before inserting into has_nutrition)

### Problem: Git push rejected
- **Solution:** Pull first, then push again
```bash
  git pull origin main
  git push origin main
```

### Problem: Can't see tables in pgAdmin
- **Solution:** Right-click on database → Refresh

## 📚 Helpful SQL Examples

### Insert a Category:
```sql
INSERT INTO CATEGORY (category_name) VALUES ('Fruits');
```

### Insert a Food:
```sql
INSERT INTO FOOD (food_name) VALUES ('Apple');
```

### Link Food to Category:
```sql
-- Assuming Apple has food_id = 1 and Fruits has category_id = 1
INSERT INTO Belong_to (food_id, category_id) VALUES (1, 1);
```

### Insert Nutrition Info:
```sql
INSERT INTO NUTRITION (measure, grams, calories, protein, fat, sat_fat, fiber, carbs) 
VALUES ('1 medium', 182, 95, 0.5, 0.3, 0.1, 4.4, 25);
```

### Search Foods with Nutrition:
```sql
SELECT f.food_name, c.category_name, n.measure, n.calories, n.protein
FROM FOOD f
JOIN Belong_to bt ON f.food_id = bt.food_id
JOIN CATEGORY c ON bt.category_id = c.category_id
JOIN has_nutrition hn ON f.food_id = hn.food_id
JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
WHERE f.food_name = 'Apple';
```

## 👥 Team Collaboration Tips

1. **Communicate frequently** - Use your team chat to coordinate
2. **Follow the task order** - Person 1 must finish before Person 2 starts
3. **Test before committing** - Always run your SQL in pgAdmin first
4. **Pull before starting work** - Avoid merge conflicts
5. **Write clear commit messages** - Help teammates understand your changes
6. **Ask for help** - Don't struggle alone!

## 🎯 Project Goal

Create a fully functional nutrition tracking database with:
- Complete schema implementation
- Realistic sample data
- Working SQL queries demonstrating all features
- Ready for GUI application development (Phase III)

## 📞 Resources

- **Setup Guide:** `docs/setup_guide.md`
- **Task Division:** `docs/phase2_task_division.md`
- **GitHub Repository:** https://github.com/Dhruvina21/nutrition-tracker

---
