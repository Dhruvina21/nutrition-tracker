"""
Database Connection Handler
Manages PostgreSQL database connections and provides query execution methods
"""

import psycopg2
from psycopg2 import pool, Error
from config.db_config import DB_CONFIG
import sys


class DatabaseConnection:
    """
    Singleton class to manage database connection pool
    """
    _instance = None
    _connection_pool = None
    
    def __new__(cls):
        """Ensure only one instance of DatabaseConnection exists"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize connection pool if not already created"""
        if self._connection_pool is None:
            try:
                self._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    1,  # minimum connections
                    10,  # maximum connections
                    **DB_CONFIG
                )
                if self._connection_pool:
                    print("✓ Database connection pool created successfully")
            except Error as e:
                print(f"✗ Error creating connection pool: {e}")
                sys.exit(1)
    
    def get_connection(self):
        """
        Get a connection from the pool
        
        Returns:
            connection: PostgreSQL connection object
        """
        try:
            connection = self._connection_pool.getconn()
            if connection:
                return connection
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            return None
    
    def return_connection(self, connection):
        """
        Return a connection to the pool
        
        Args:
            connection: PostgreSQL connection object to return
        """
        if connection:
            self._connection_pool.putconn(connection)
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self._connection_pool:
            self._connection_pool.closeall()
            print("✓ All database connections closed")


class Database:
    """
    Database operations class
    Provides methods for executing queries
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.db_connection = DatabaseConnection()
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Execute a SQL query
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters (optional)
            fetch (bool): Whether to fetch results (True for SELECT queries)
        
        Returns:
            list: Query results if fetch=True, None otherwise
        """
        connection = None
        cursor = None
        
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                return None
                
        except Error as e:
            if connection:
                connection.rollback()
            print(f"Database error: {e}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.db_connection.return_connection(connection)
    
    def execute_query_one(self, query, params=None):
        """
        Execute a query and fetch one result
        
        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters (optional)
        
        Returns:
            tuple: Single result row, or None if no results
        """
        connection = None
        cursor = None
        
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchone()
            return result
            
        except Error as e:
            print(f"Database error: {e}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.db_connection.return_connection(connection)
    
    def execute_many(self, query, data_list):
        """
        Execute a query with multiple parameter sets (bulk insert/update)
        
        Args:
            query (str): SQL query to execute
            data_list (list): List of parameter tuples
        
        Returns:
            bool: True if successful, False otherwise
        """
        connection = None
        cursor = None
        
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            
            cursor.executemany(query, data_list)
            connection.commit()
            return True
            
        except Error as e:
            if connection:
                connection.rollback()
            print(f"Database error: {e}")
            return False
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.db_connection.return_connection(connection)
    
    def close(self):
        """Close all database connections"""
        self.db_connection.close_all_connections()


# Test connection when module is imported
if __name__ == "__main__":
    print("Testing database connection...")
    db = Database()
    
    # Test query
    result = db.execute_query_one("SELECT version();")
    if result:
        print(f"✓ Connection successful!")
        print(f"PostgreSQL version: {result[0]}")
    else:
        print("✗ Connection failed!")
    
    db.close()