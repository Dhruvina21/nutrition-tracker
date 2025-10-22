# Nutrition Tracker - Team Setup Guide

## Prerequisites

- PostgreSQL installed on your computer
- Git installed
- VS Code (recommended) or any code editor
- GitHub account

## Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/Dhruvina21/nutrition-tracker.git
cd nutrition-tracker
```

## Step 2: Verify PostgreSQL Installation

Check if PostgreSQL is installed:

```bash
psql --version
```

You should see something like: `psql (PostgreSQL) 14.x` or similar.

## Step 3: Create the Database

Connect to PostgreSQL and create the database:

```bash
psql -U postgres
```

Then in the PostgreSQL prompt, run:

```sql
CREATE DATABASE nutrition_tracker;
\q
```

## Step 4: Working with the Project

### Running SQL Files

To run a SQL file in the database:

```bash
psql -U postgres -d nutrition_tracker -f migrations/01_create_tables.sql
```

### Daily Workflow

1. **Before starting work, pull latest changes:**

```bash
   git pull origin main
```

2. **After making changes, commit and push:**

```bash
   git add .
   git commit -m "Description of what you changed"
   git push origin main
```

## Project Structure

```
nutrition-tracker/
├── migrations/          # SQL files for creating tables
├── queries/            # SQL files for sample queries
├── docs/              # Documentation
└── README.md          # Project overview
```

## Important Notes

- Always pull before starting work to get the latest changes
- Write clear commit messages
- Test your SQL files before committing
- Ask for help if you encounter any issues!
