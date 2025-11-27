"""
Nutrition Tracker Application
Main entry point - shows login then dashboard
"""

import tkinter as tk
from app.database import Database
from app.gui.login_window import LoginWindow
from app.gui.main_window import MainWindow


class NutritionTrackerApp:
    """
    Main Application Controller
    Handles login flow and dashboard display
    """
    
    def __init__(self):
        """Initialize the application"""
        # Initialize database connection
        self.db = Database()
        print("✓ Database connection pool created successfully")
        
        # Current user data (set after login)
        self.current_user = None
        
        # Start with login window
        self.show_login()
    
    def show_login(self):
        """Show the login/register window"""
        login_window = LoginWindow(on_login_success=self.on_login_success)
        login_window.run()
    
    def on_login_success(self, user_data):
        """
        Called when user successfully logs in
        
        Args:
            user_data (dict): User information from login
        """
        self.current_user = user_data
        print(f"✓ User logged in: {user_data['username']}")
        
        # Show main dashboard
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show the main dashboard window"""
        if self.current_user:
            dashboard = MainWindow(user_data=self.current_user)
            dashboard.run()
        else:
            print("Error: No user logged in")
            self.show_login()
    
    def on_logout(self):
        """Called when user logs out"""
        print(f"✓ User logged out: {self.current_user['username']}")
        self.current_user = None
        self.show_login()
    
    def shutdown(self):
        """Clean shutdown of the application"""
        print("\n✓ Shutting down Nutrition Tracker...")
        self.db.close()
        print("✓ All database connections closed")


def main():
    """Main application entry point"""
    try:
        app = NutritionTrackerApp()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()