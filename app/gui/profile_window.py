"""
Phase 9: User Profile Management - DHRUVINA
Features:
- View profile information
- Update email
- Change password  
- Account statistics
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from app.database import Database
from app.auth import Auth


class ProfileWindow:
    """
    User Profile Management Window
    """
    
    def __init__(self, user_data):
        """
        Initialize profile window
        
        Args:
            user_data (dict): Current user's data
        """
        self.user_data = user_data
        self.db = Database()
        self.auth = Auth()
        
        # Create window
        self.root = tk.Tk()
        self.root.title("User Profile - Nutrition Tracker")
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        # Center window
        self.center_window(700, 750)
        
        # Create UI
        self.create_ui()
        
        # Load statistics
        self.load_statistics()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_ui(self):
        """Create the user interface"""
        # Header
        header = tk.Frame(self.root, bg="#4CAF50", height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="👤 My Profile",
            font=("Arial", 24, "bold"),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=30)
        
        # Main content
        content = tk.Frame(self.root, bg="#f5f5f5")
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Profile Info Section
        self.create_profile_info(content)
        
        # Statistics Section
        self.create_statistics(content)
        
        # Update Email Section
        self.create_email_update(content)
        
        # Change Password Section
        self.create_password_change(content)
    
    def create_profile_info(self, parent):
        """Create profile information display"""
        section = tk.LabelFrame(
            parent,
            text="Profile Information",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333",
            padx=20,
            pady=15
        )
        section.pack(fill=tk.X, pady=(0, 15))
        
        # Username
        info_frame = tk.Frame(section, bg="white")
        info_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            info_frame,
            text="Username:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#666666",
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        tk.Label(
            info_frame,
            text=self.user_data['username'],
            font=("Arial", 11),
            bg="white",
            fg="#333333"
        ).pack(side=tk.LEFT)
        
        # Email
        info_frame = tk.Frame(section, bg="white")
        info_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            info_frame,
            text="Email:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#666666",
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        tk.Label(
            info_frame,
            text=self.user_data['email'],
            font=("Arial", 11),
            bg="white",
            fg="#333333"
        ).pack(side=tk.LEFT)
        
        # Registration Date
        info_frame = tk.Frame(section, bg="white")
        info_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            info_frame,
            text="Member Since:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#666666",
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        reg_date = self.user_data['registration_date']
        if isinstance(reg_date, str):
            date_str = reg_date
        else:
            date_str = reg_date.strftime("%B %d, %Y")
        
        tk.Label(
            info_frame,
            text=date_str,
            font=("Arial", 11),
            bg="white",
            fg="#333333"
        ).pack(side=tk.LEFT)
    
    def create_statistics(self, parent):
        """Create statistics display"""
        section = tk.LabelFrame(
            parent,
            text="Account Statistics",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333",
            padx=20,
            pady=15
        )
        section.pack(fill=tk.X, pady=(0, 15))
        
        # Stats container
        stats_container = tk.Frame(section, bg="white")
        stats_container.pack(fill=tk.X)
        
        # Total Foods Logged
        self.total_foods_label = tk.Label(
            stats_container,
            text="Total Foods Logged: Loading...",
            font=("Arial", 11),
            bg="white",
            fg="#333333"
        )
        self.total_foods_label.pack(anchor=tk.W, pady=3)
        
        # Days Active
        self.days_active_label = tk.Label(
            stats_container,
            text="Days Active: Loading...",
            font=("Arial", 11),
            bg="white",
            fg="#333333"
        )
        self.days_active_label.pack(anchor=tk.W, pady=3)
        
        # First Log Date
        self.first_log_label = tk.Label(
            stats_container,
            text="First Log Date: Loading...",
            font=("Arial", 11),
            bg="white",
            fg="#333333"
        )
        self.first_log_label.pack(anchor=tk.W, pady=3)
    
    def create_email_update(self, parent):
        """Create email update section"""
        section = tk.LabelFrame(
            parent,
            text="Update Email",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333",
            padx=20,
            pady=15
        )
        section.pack(fill=tk.X, pady=(0, 15))
        
        # New Email Entry
        email_frame = tk.Frame(section, bg="white")
        email_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            email_frame,
            text="New Email:",
            font=("Arial", 11),
            bg="white",
            fg="#666666",
            width=12,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.new_email_entry = tk.Entry(
            email_frame,
            font=("Arial", 11),
            bg="#f9f9f9",
            fg="#333333",
            width=30
        )
        self.new_email_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            email_frame,
            text="Update Email",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED,
            cursor="hand2",
            command=self.update_email,
            width=12
        ).pack(side=tk.LEFT)
    
    def create_password_change(self, parent):
        """Create password change section"""
        section = tk.LabelFrame(
            parent,
            text="Change Password",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333",
            padx=20,
            pady=15
        )
        section.pack(fill=tk.X)
        
        # Current Password
        pass_frame = tk.Frame(section, bg="white")
        pass_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            pass_frame,
            text="Current Password:",
            font=("Arial", 10),
            bg="white",
            fg="#666666",
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.current_pass_entry = tk.Entry(
            pass_frame,
            font=("Arial", 10),
            bg="#f9f9f9",
            fg="#333333",
            show="*",
            width=25
        )
        self.current_pass_entry.pack(side=tk.LEFT, padx=10)
        
        # New Password
        pass_frame = tk.Frame(section, bg="white")
        pass_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            pass_frame,
            text="New Password:",
            font=("Arial", 10),
            bg="white",
            fg="#666666",
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.new_pass_entry = tk.Entry(
            pass_frame,
            font=("Arial", 10),
            bg="#f9f9f9",
            fg="#333333",
            show="*",
            width=25
        )
        self.new_pass_entry.pack(side=tk.LEFT, padx=10)
        
        # Confirm Password
        pass_frame = tk.Frame(section, bg="white")
        pass_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            pass_frame,
            text="Confirm Password:",
            font=("Arial", 10),
            bg="white",
            fg="#666666",
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.confirm_pass_entry = tk.Entry(
            pass_frame,
            font=("Arial", 10),
            bg="#f9f9f9",
            fg="#333333",
            show="*",
            width=25
        )
        self.confirm_pass_entry.pack(side=tk.LEFT, padx=10)
        
        # Change Password Button
        tk.Button(
            section,
            text="Change Password",
            font=("Arial", 11, "bold"),
            bg="#FF9800",
            fg="white",
            relief=tk.RAISED,
            cursor="hand2",
            command=self.change_password,
            width=20,
            height=2
        ).pack(pady=(15, 0))
    
    def load_statistics(self):
        """Load user statistics from database"""
        try:
            # Total foods logged
            query = """
                SELECT COUNT(*) 
                FROM FOOD_INFO 
                WHERE user_id = %s;
            """
            result = self.db.execute_query_one(query, (self.user_data['user_id'],))
            total_foods = result[0] if result else 0
            
            self.total_foods_label.config(text=f"Total Foods Logged: {total_foods}")
            
            # Days active (distinct dates)
            query = """
                SELECT COUNT(DISTINCT log_date) 
                FROM FOOD_INFO 
                WHERE user_id = %s;
            """
            result = self.db.execute_query_one(query, (self.user_data['user_id'],))
            days_active = result[0] if result else 0
            
            self.days_active_label.config(text=f"Days Active: {days_active}")
            
            # First log date
            query = """
                SELECT MIN(log_date) 
                FROM FOOD_INFO 
                WHERE user_id = %s;
            """
            result = self.db.execute_query_one(query, (self.user_data['user_id'],))
            
            if result and result[0]:
                first_log = result[0].strftime("%B %d, %Y")
                self.first_log_label.config(text=f"First Log Date: {first_log}")
            else:
                self.first_log_label.config(text="First Log Date: No logs yet")
                
        except Exception as e:
            print(f"Error loading statistics: {e}")
            messagebox.showerror("Error", f"Failed to load statistics:\n{e}")
    
    def update_email(self):
        """Update user's email"""
        new_email = self.new_email_entry.get().strip()
        
        if not new_email:
            messagebox.showerror("Error", "Please enter a new email address")
            return
        
        # Validate email
        if not self.auth.validate_email(new_email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Check if email already exists
        if self.auth.email_exists(new_email):
            messagebox.showerror("Error", "This email is already in use")
            return
        
        # Update email in database
        try:
            query = """
                UPDATE "USER" 
                SET email = %s 
                WHERE user_id = %s;
            """
            self.db.execute_query(query, (new_email, self.user_data['user_id']))
            
            # Update local user_data
            self.user_data['email'] = new_email
            
            messagebox.showinfo("Success", "Email updated successfully!")
            self.new_email_entry.delete(0, tk.END)
            
            # Refresh profile display
            self.root.destroy()
            ProfileWindow(self.user_data).run()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update email:\n{e}")
    
    def change_password(self):
        """Change user's password"""
        current_pass = self.current_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        
        if not current_pass or not new_pass or not confirm_pass:
            messagebox.showerror("Error", "Please fill in all password fields")
            return
        
        # Verify current password
        success, _, _ = self.auth.login_user(self.user_data['username'], current_pass)
        if not success:
            messagebox.showerror("Error", "Current password is incorrect")
            return
        
        # Validate new password
        if not self.auth.validate_password(new_pass):
            messagebox.showerror("Error", "New password must be at least 6 characters\nand contain both letters and numbers")
            return
        
        # Check passwords match
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New passwords do not match")
            return
        
        # Update password in database
        try:
            query = """
                UPDATE "USER" 
                SET password = %s 
                WHERE user_id = %s;
            """
            self.db.execute_query(query, (new_pass, self.user_data['user_id']))
            
            messagebox.showinfo("Success", "Password changed successfully!")
            
            # Clear fields
            self.current_pass_entry.delete(0, tk.END)
            self.new_pass_entry.delete(0, tk.END)
            self.confirm_pass_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password:\n{e}")
    
    def run(self):
        """Run the profile window"""
        self.root.mainloop()


# Test standalone
if __name__ == "__main__":
    # Test data
    test_user = {
        'user_id': 23,
        'username': 'john_doe',
        'email': 'john@example.com',
        'registration_date': datetime(2024, 1, 15).date()
    }
    
    profile = ProfileWindow(user_data=test_user)    
    profile.run()
