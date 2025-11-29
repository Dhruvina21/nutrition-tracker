# Nutrition Tracker - Complete Database & GUI Application

A comprehensive nutrition tracking system built with **PostgreSQL database** and **Python Tkinter GUI**, enabling users to track dietary intake, search foods, view nutritional information, and analyze eating patterns through detailed reports.

---

## Project Overview
This full-stack nutrition tracking application allows users to:

- **Register/Login** with secure authentication
- **Search foods** by name or browse by category
- **Log daily food consumption** with serving sizes
- **View detailed reports** (Daily, Weekly, Monthly analytics)
- **Manage profile** (update email, change password)
- **Track nutrition trends** with interactive charts

---

## 🎯 Features Completed

### ✅ Phase 1-3: Foundation

- Database schema design and implementation
- PostgreSQL connection pooling
- Data population (8 categories, 64+ foods, 71+ nutrition records)

### ✅ Phase 4: Authentication System

- User registration with validation
- Secure login
- Password hashing
- Session management
- Modern split-screen UI design

### ✅ Phase 5: Main Dashboard

- Welcome panel with user info
- Quick actions cards
- Today's nutrition summary
- Real-time calorie/macro tracking
- Navigation to all features

### ✅ Phase 6: Food Search

- Search by food name
- Browse by category (8 categories)
- Detailed nutrition facts display
- Multiple serving size options
- Category filtering

### ✅ Phase 7: Food Logging

- Date-based food logging
- Serving size selection
- Daily totals calculation
- Food log history table
- Delete log entries
- Notes/comments support

### ✅ Phase 8: Reports & Analytics

- **Daily Summary:** Nutrition cards, pie charts, foods list
- **Weekly Summary:** Average stats, calorie bar chart, most logged foods
- **Monthly Overview:** Trend line graphs, category distribution
- Interactive matplotlib visualizations

### ✅ Phase 9: User Profile

- View profile information
- Update email address
- Change password
- Account statistics (foods logged, days active)
- Registration date tracking

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8+**
- **PostgreSQL 17+**
- **pgAdmin 4** (recommended)

### Step-by-Step Installation:

```bash
# 1. Clone repository
git clone https://github.com/Dhruvina21/nutrition-tracker.git
cd nutrition-tracker

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure database connection
cp config/db_config_template.py config/db_config.py
# Edit config/db_config.py with your PostgreSQL password

# 6. Setup database in pgAdmin
# - Create database: nutrition_tracker
# - Run migrations/01_create_tables.sql
# - Run migrations/02_insert_categories_and_foods.sql
# - Run migrations/03_insert_nutrition_facts.sql
# - Run migrations/04_insert_users_and_logs.sql

# 7. Run the application
python3 -m app.main
```

---

## Using the Application

### First Time:

1. Click **Register** tab
2. Create account (username, email, password)
3. Login with your credentials

### Features:

- **🏠 Home** - Dashboard with today's summary
- **🔍 Search Foods** - Find nutritional information
- **📝 Log Food** - Track daily intake
- **📊 My Reports** - View analytics (Daily/Weekly/Monthly)
- **👤 Profile** - Manage account settings

---

## 📁 Project Structure

```
nutrition-tracker/
├── app/
│   ├── main.py                  # Application entry
│   ├── database.py              # DB connection
│   ├── auth.py                  # Authentication
│   └── gui/
│       ├── login_window.py      # Login/Register
│       ├── main_window.py       # Dashboard
│       ├── search_window.py     # Food search
│       ├── log_window.py        # Food logging
│       ├── report_window.py     # Reports
│       └── profile_window.py    # Profile
├── config/
│   └── db_config.py            # Database config
├── migrations/                  # SQL scripts
├── requirements.txt
└── README.md
```

---

## Technical Stack

- **Language:** Python 3.8+
- **GUI:** Tkinter
- **Database:** PostgreSQL 17
- **Connector:** psycopg2
- **Visualization:** matplotlib
- **Data:** pandas
- **Widgets:** tkcalendar

---

## Database Schema

**Tables:**

- USER (user accounts)
- CATEGORY (8 food categories)
- FOOD (64+ food items)
- NUTRITION (71+ nutrition records)
- FOOD_INFO (food consumption logs)
- Belong_to (foods ↔ categories)
- has_nutrition (foods ↔ nutrition)

---

## Educational Purpose

Database course project demonstrating:

- ER → Relational schema conversion
- Database normalization
- Complex SQL queries
- Full-stack development
- Team collaboration with Git

---

Enjoy tracking your nutrition!
