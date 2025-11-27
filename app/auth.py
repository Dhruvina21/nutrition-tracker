"""
Authentication Module
Handles user registration, login, and session management
"""

import re
from datetime import datetime
from app.database import Database


class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass


class Auth:
    """
    Authentication class for user management
    """
    
    def __init__(self):
        """Initialize authentication with database connection"""
        self.db = Database()
        self.current_user = None  # Store current logged-in user
    
    def validate_username(self, username):
        """
        Validate username format
        
        Args:
            username (str): Username to validate
        
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        if not username:
            return False, "Username cannot be empty"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 50:
            return False, "Username must be less than 50 characters"
        
        # Only allow alphanumeric and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, ""
    
    def validate_email(self, email):
        """
        Validate email format
        
        Args:
            email (str): Email to validate
        
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        if not email:
            return False, "Email cannot be empty"
        
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 100:
            return False, "Email must be less than 100 characters"
        
        return True, ""
    
    def validate_password(self, password):
        """
        Validate password strength
        
        Args:
            password (str): Password to validate
        
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 100:
            return False, "Password must be less than 100 characters"
        
        # Check for at least one letter and one number
        if not re.search(r'[a-zA-Z]', password):
            return False, "Password must contain at least one letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        
        return True, ""
    
    def username_exists(self, username):
        """
        Check if username already exists in database
        
        Args:
            username (str): Username to check
        
        Returns:
            bool: True if username exists, False otherwise
        """
        query = 'SELECT user_id FROM "USER" WHERE LOWER(username) = LOWER(%s);'
        result = self.db.execute_query_one(query, (username,))
        return result is not None
    
    def email_exists(self, email):
        """
        Check if email already exists in database
        
        Args:
            email (str): Email to check
        
        Returns:
            bool: True if email exists, False otherwise
        """
        query = 'SELECT user_id FROM "USER" WHERE LOWER(email) = LOWER(%s);'
        result = self.db.execute_query_one(query, (email,))
        return result is not None
    
    def register_user(self, username, email, password):
        """
        Register a new user
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Password (will be stored as plain text for this project)
        
        Returns:
            tuple: (bool, str) - (success, message)
        """
        # Validate username
        valid, error = self.validate_username(username)
        if not valid:
            return False, error
        
        # Validate email
        valid, error = self.validate_email(email)
        if not valid:
            return False, error
        
        # Validate password
        valid, error = self.validate_password(password)
        if not valid:
            return False, error
        
        # Check if username already exists
        if self.username_exists(username):
            return False, "Username already exists"
        
        # Check if email already exists
        if self.email_exists(email):
            return False, "Email already exists"
        
        # Insert new user into database
        try:
            query = '''
                INSERT INTO "USER" (username, email, password, registration_date)
                VALUES (%s, %s, %s, CURRENT_DATE)
                RETURNING user_id;
            '''
            # Note: In production, passwords should be hashed!
            # For this educational project, we're storing plain text
            result = self.db.execute_query_one(query, (username, email, password))
            
            if result:
                return True, "Registration successful!"
            else:
                return False, "Registration failed. Please try again."
                
        except Exception as e:
            print(f"Registration error: {e}")
            return False, "Registration failed. Please try again."
    
    def login_user(self, username, password):
        """
        Authenticate user login
        
        Args:
            username (str): Username
            password (str): Password
        
        Returns:
            tuple: (bool, str, dict) - (success, message, user_data)
        """
        if not username or not password:
            return False, "Username and password are required", None
        
        # Query user from database
        query = '''
            SELECT user_id, username, email, registration_date
            FROM "USER"
            WHERE LOWER(username) = LOWER(%s) AND password = %s;
        '''
        
        try:
            result = self.db.execute_query_one(query, (username, password))
            
            if result:
                # User found - login successful
                user_data = {
                    'user_id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'registration_date': result[3]
                }
                
                # Store current user
                self.current_user = user_data
                
                return True, "Login successful!", user_data
            else:
                return False, "Invalid username or password", None
                
        except Exception as e:
            print(f"Login error: {e}")
            return False, "Login failed. Please try again.", None
    
    def logout_user(self):
        """
        Logout current user
        """
        self.current_user = None
    
    def is_logged_in(self):
        """
        Check if a user is currently logged in
        
        Returns:
            bool: True if user is logged in, False otherwise
        """
        return self.current_user is not None
    
    def get_current_user(self):
        """
        Get current logged-in user data
        
        Returns:
            dict: User data or None if not logged in
        """
        return self.current_user
    
    def get_current_user_id(self):
        """
        Get current user's ID
        
        Returns:
            int: User ID or None if not logged in
        """
        if self.current_user:
            return self.current_user['user_id']
        return None


# Test authentication when module is run directly
if __name__ == "__main__":
    print("Testing Authentication Module...")
    print("=" * 60)
    
    auth = Auth()
    
    # Test 1: Register new user
    print("\nTest 1: User Registration")
    print("-" * 60)
    success, message = auth.register_user("test_user", "test@example.com", "password123")
    print(f"Registration: {message}")
    
    # Test 2: Try duplicate username
    print("\nTest 2: Duplicate Username")
    print("-" * 60)
    success, message = auth.register_user("test_user", "another@example.com", "password123")
    print(f"Duplicate check: {message}")
    
    # Test 3: Login with correct credentials
    print("\nTest 3: Login")
    print("-" * 60)
    success, message, user_data = auth.login_user("test_user", "password123")
    print(f"Login: {message}")
    if user_data:
        print(f"Logged in as: {user_data['username']}")
    
    # Test 4: Login with wrong password
    print("\nTest 4: Wrong Password")
    print("-" * 60)
    success, message, user_data = auth.login_user("test_user", "wrongpassword")
    print(f"Wrong password: {message}")
    
    print("\n" + "=" * 60)
    print("Authentication module tests complete!")