#!/usr/bin/env python3
"""
Test script to verify PostgreSQL database connection
IMPORTANT: Update the credentials below before running
"""

import psycopg2
from psycopg2 import Error

def test_database_connection():
    """Test connection to nutrition_tracker database"""
    
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    print()
    
    # Database configuration
    # ⚠️ IMPORTANT: Update these values with your actual credentials
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'nutrition_tracker',
        'user': 'postgres',          # ← UPDATE: Your PostgreSQL username
        'password': 'your_password'  # ← UPDATE: Your PostgreSQL password
    }
    
    print("Attempting to connect to PostgreSQL...")
    print(f"Host: {db_config['host']}")
    print(f"Port: {db_config['port']}")
    print(f"Database: {db_config['database']}")
    print(f"User: {db_config['user']}")
    print()
    
    connection = None
    cursor = None
    
    try:
        # Attempt connection
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        print("✓ Successfully connected to PostgreSQL database!")
        print()
        
        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"PostgreSQL version: {db_version[0]}")
        print()
        
        # Check if required tables exist
        # Note: PostgreSQL stores unquoted table names in lowercase
        # Some tables might be created with quotes (case-sensitive)
        tables = {
            'user': 'USER',
            'category': 'CATEGORY',
            'food': 'FOOD',
            'nutrition': 'NUTRITION',
            'belong_to': 'Belong_to',
            'has_nutrition': 'has_nutrition',
            'food_info': 'FOOD_INFO'
        }
        
        print("Checking database tables:")
        print("-" * 60)
        
        all_tables_exist = True
        
        for table_lower, table_display in tables.items():
            # First try lowercase (standard PostgreSQL)
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{table_lower}'
                );
            """)
            exists = cursor.fetchone()[0]
            
            # If not found, try with quotes (case-sensitive)
            table_query = table_lower
            if not exists and table_lower == 'user':
                # USER might be quoted, try "USER"
                try:
                    cursor.execute(f'SELECT COUNT(*) FROM "USER";')
                    count = cursor.fetchone()[0]
                    exists = True
                    table_query = '"USER"'
                except:
                    exists = False
            
            if exists:
                # Count rows in table
                if table_query == '"USER"':
                    cursor.execute(f'SELECT COUNT(*) FROM {table_query};')
                else:
                    cursor.execute(f'SELECT COUNT(*) FROM {table_lower};')
                count = cursor.fetchone()[0]
                print(f"✓ {table_display:20} - Exists ({count} rows)")
            else:
                print(f"✗ {table_display:20} - NOT FOUND")
                all_tables_exist = False
        
        print()
        print("=" * 60)
        
        if all_tables_exist:
            print("✅ Database setup COMPLETE!")
            print()
            print("Your database is ready for the GUI application!")
        else:
            print("❌ Database setup INCOMPLETE!")
            print()
            print("Please run your SQL migration files in pgAdmin:")
            print("   1. migrations/01_create_tables.sql")
            print("   2. migrations/02_insert_categories_and_foods.sql")
            print("   3. migrations/03_insert_nutrition_facts.sql")
            print("   4. migrations/04_insert_users_and_logs.sql")
        
        print("=" * 60)
        
    except Error as e:
        print("❌ Error connecting to PostgreSQL database!")
        print()
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check your username and password in db_config")
        print("   3. Verify database 'nutrition_tracker' exists")
        print("   4. Check if PostgreSQL is running on port 5432")
        
    finally:
        # Close connections
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print()
            print("Database connection closed.")

if __name__ == "__main__":
    test_database_connection()