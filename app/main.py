"""
Nutrition Tracker - Main Application Entry Point
Phase III: GUI Application
"""

import sys
import tkinter as tk
from tkinter import messagebox
from app.database import Database


class NutritionTrackerApp:
    """
    Main Application Class
    Entry point for the Nutrition Tracker GUI application
    """
    
    def __init__(self):
        """Initialize the application"""
        self.db = None
        self.root = None
        
    def initialize_database(self):
        """Initialize database connection"""
        try:
            print("Initializing database connection...")
            self.db = Database()
            
            # Test connection
            result = self.db.execute_query_one("SELECT COUNT(*) FROM category;")
            if result:
                print(f"✓ Database connected successfully")
                print(f"✓ Found {result[0]} food categories")
                return True
            else:
                print("✗ Database connection test failed")
                return False
                
        except Exception as e:
            print(f"✗ Error initializing database: {e}")
            return False
    
    def create_main_window(self):
        """Create the main application window"""
        self.root = tk.Tk()
        self.root.title("Nutrition Tracker")
        self.root.geometry("800x600")
        
        # Center window on screen
        self.center_window(800, 600)
        
        # Create welcome screen (temporary - will be replaced in Phase 4)
        self.create_welcome_screen()
        
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_welcome_screen(self):
        """Create temporary welcome screen"""
        # Main container
        container = tk.Frame(self.root, bg="#f0f0f0")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome_frame = tk.Frame(container, bg="#f0f0f0")
        welcome_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        title = tk.Label(
            welcome_frame,
            text="🥗 Nutrition Tracker",
            font=("Arial", 32, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title.pack(pady=20)
        
        subtitle = tk.Label(
            welcome_frame,
            text="Phase 2: Project Structure Setup Complete!",
            font=("Arial", 16),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        subtitle.pack(pady=10)
        
        status = tk.Label(
            welcome_frame,
            text="✓ Database Connected\n✓ GUI Framework Initialized",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#27ae60",
            justify=tk.LEFT
        )
        status.pack(pady=20)
        
        info = tk.Label(
            welcome_frame,
            text="Ready for Phase 3: Authentication System",
            font=("Arial", 11, "italic"),
            bg="#f0f0f0",
            fg="#95a5a6"
        )
        info.pack(pady=10)
        
        # Exit button
        exit_btn = tk.Button(
            welcome_frame,
            text="Exit Application",
            command=self.quit_application,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        exit_btn.pack(pady=20)
    
    def quit_application(self):
        """Safely quit the application"""
        if messagebox.askokcancel("Quit", "Do you want to exit the application?"):
            if self.db:
                self.db.close()
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Run the application"""
        print("=" * 60)
        print("Nutrition Tracker - Starting Application")
        print("=" * 60)
        print()
        
        # Initialize database
        if not self.initialize_database():
            messagebox.showerror(
                "Database Error",
                "Failed to connect to database.\n\n"
                "Please check:\n"
                "1. PostgreSQL is running\n"
                "2. Database 'nutrition_tracker' exists\n"
                "3. Credentials in config/db_config.py are correct"
            )
            sys.exit(1)
        
        # Create and run GUI
        print("\nStarting GUI...")
        self.create_main_window()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_application)
        
        print("✓ Application started successfully!")
        print()
        self.root.mainloop()


def main():
    """Main function to start the application"""
    try:
        app = NutritionTrackerApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()