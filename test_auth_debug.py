"""
Debug test for authentication
"""
from app.auth import Auth
from app.database import Database

print("=" * 60)
print("Debug Authentication Test")
print("=" * 60)

# Test direct database insert
print("\n1. Testing direct database insert...")
db = Database()

# Delete test_user if exists
db.execute_query('DELETE FROM "USER" WHERE username = %s;', ('test_user',))
print("✓ Cleared any existing test_user")

# Try direct insert
query = '''
    INSERT INTO "USER" (username, email, password, registration_date)
    VALUES (%s, %s, %s, CURRENT_DATE)
    RETURNING user_id, username, password;
'''
result = db.execute_query_one(query, ('test_user', 'test@example.com', 'password123'))
print(f"Direct insert result: {result}")

# Check if it's in the database
check_query = 'SELECT user_id, username, email, password FROM "USER" WHERE username = %s;'
check_result = db.execute_query_one(check_query, ('test_user',))
print(f"User in database: {check_result}")

print("\n" + "=" * 60)
print("\n2. Testing Auth.register_user()...")

# Delete test_user2 if exists
db.execute_query('DELETE FROM "USER" WHERE username = %s;', ('test_user2',))

auth = Auth()
success, message = auth.register_user('test_user2', 'test2@example.com', 'password456')
print(f"Registration: {success} - {message}")

# Check if it's in the database
check_result2 = db.execute_query_one(check_query, ('test_user2',))
print(f"User in database: {check_result2}")

print("\n" + "=" * 60)
print("\n3. Testing Auth.login_user()...")

success, message, user_data = auth.login_user('test_user', 'password123')
print(f"Login result: {success} - {message}")
if user_data:
    print(f"User data: {user_data}")

db.close()