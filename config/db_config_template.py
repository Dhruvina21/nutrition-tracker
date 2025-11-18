"""
Database Configuration Template
Copy this file to db_config.py and update with your actual credentials
"""

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'nutrition_tracker',
    'user': 'postgres',          # UPDATE: Your PostgreSQL username
    'password': 'your-password'  # UPDATE: Your PostgreSQL password
}

# Connection pool settings (optional - for advanced use)
POOL_CONFIG = {
    'minconn': 1,
    'maxconn': 10
}