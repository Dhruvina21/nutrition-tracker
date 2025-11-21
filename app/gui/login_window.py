"""
Login/Register Window - Cross-Platform Design
Works beautifully on both Mac and Windows
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.auth import Auth
import platform


class LoginWindow:
    """
    Cross-platform Login and Registration Window
    """
    
    def __init__(self, on_login_success):
        """
        Initialize login window
        
        Args:
            on_login_success: Callback function when login is successful
        """
        self.on_login_success = on_login_success
        self.auth = Auth()
        
        # Detect OS for platform-specific adjustments
        self.is_windows = platform.system() == "Windows"
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Nutrition Tracker")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")
        
        # Center window
        self.center_window(900, 650)
        
        # Create UI
        self.create_ui()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Branding
        left_frame = tk.Frame(main_frame, bg="#4CAF50", width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        left_frame.pack_propagate(False)
        
        self.create_left_panel(left_frame)
        
        # Right panel - Forms
        right_frame = tk.Frame(main_frame, bg="#ffffff", width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)
        
        self.create_right_panel(right_frame)
    
    def create_left_panel(self, parent):
        """Create the left branding panel"""
        container = tk.Frame(parent, bg="#4CAF50")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo - using text emoji works on all platforms
        logo = tk.Label(
            container,
            text="🥗",
            font=("Arial", 100, "bold"),
            bg="#4CAF50"
        )
        logo.pack(pady=(0, 20))
        
        # App name
        app_name = tk.Label(
            container,
            text="Nutrition Tracker",
            font=("Arial", 28, "bold"),
            bg="#4CAF50",
            fg="white"
        )
        app_name.pack(pady=(0, 10))
        
        # Tagline
        tagline = tk.Label(
            container,
            text="Track your meals, achieve your goals",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="#E8F5E9"
        )
        tagline.pack(pady=(0, 30))
        
        # Features with unicode symbols (cross-platform compatible)
        features = [
            "• Search 1000+ foods",
            "• Track daily nutrition", 
            "• View detailed reports",
            "• Set and achieve goals"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                container,
                text=feature,
                font=("Arial", 11),
                bg="#4CAF50",
                fg="white",
                anchor=tk.W,
                justify=tk.LEFT
            )
            feature_label.pack(pady=5, padx=40, anchor=tk.W)
    
    def create_right_panel(self, parent):
        """Create the right form panel"""
        container = tk.Frame(parent, bg="#ffffff")
        container.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Tab buttons with better styling
        tab_frame = tk.Frame(container, bg="#ffffff")
        tab_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Use Canvas for better button rendering on Windows
        self.login_tab_btn = tk.Button(
            tab_frame,
            text="Login",
            font=("Arial", 13, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.RAISED,
            bd=0,
            cursor="hand2",
            command=self.show_login_form,
            width=13,
            height=2
        )
        self.login_tab_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.register_tab_btn = tk.Button(
            tab_frame,
            text="Register",
            font=("Arial", 13),
            bg="#e8e8e8",
            fg="#666666",
            activebackground="#d0d0d0",
            activeforeground="#666666",
            relief=tk.RAISED,
            bd=0,
            cursor="hand2",
            command=self.show_register_form,
            width=13,
            height=2
        )
        self.register_tab_btn.pack(side=tk.LEFT)
        
        # Forms container
        self.forms_container = tk.Frame(container, bg="#ffffff")
        self.forms_container.pack(fill=tk.BOTH, expand=True)
        
        # Create forms
        self.login_form = self.create_login_form(self.forms_container)
        self.register_form = self.create_register_form(self.forms_container)
        
        # Show login by default
        self.show_login_form()
    
    def create_styled_entry(self, parent, show_password=False):
        """Create a styled entry widget with frame border"""
        # Outer frame for border effect
        frame = tk.Frame(parent, bg="#cccccc", bd=0)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # Inner frame for padding
        inner_frame = tk.Frame(frame, bg="#ffffff", bd=0)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Entry widget
        entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            relief=tk.FLAT,
            bg="#ffffff",
            fg="#333333",
            bd=0,
            highlightthickness=0
        )
        entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=12)
        
        if show_password:
            entry.config(show="*")
        
        # Focus effects
        def on_focus_in(e):
            frame.config(bg="#4CAF50")
        
        def on_focus_out(e):
            frame.config(bg="#cccccc")
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def create_login_form(self, parent):
        """Create login form"""
        form = tk.Frame(parent, bg="#ffffff")
        
        # Welcome message
        welcome = tk.Label(
            form,
            text="Welcome Back!",
            font=("Arial", 22, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        welcome.pack(pady=(0, 5))
        
        subtitle = tk.Label(
            form,
            text="Enter your credentials to continue",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#999999"
        )
        subtitle.pack(pady=(0, 30))
        
        # Username field
        tk.Label(
            form,
            text="Username",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
            anchor=tk.W
        ).pack(fill=tk.X, pady=(10, 5))
        
        self.login_username_entry = self.create_styled_entry(form)
        self.login_username_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Password field
        tk.Label(
            form,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
            anchor=tk.W
        ).pack(fill=tk.X, pady=(10, 5))
        
        self.login_password_entry = self.create_styled_entry(form, show_password=True)
        self.login_password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Login button
        login_btn = tk.Button(
            form,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.RAISED,
            bd=0,
            cursor="hand2",
            command=self.handle_login,
            height=2
        )
        login_btn.pack(fill=tk.X, pady=(25, 0))
        
        return form
    
    def create_register_form(self, parent):
        """Create registration form"""
        form = tk.Frame(parent, bg="#ffffff")
        
        # Welcome message
        welcome = tk.Label(
            form,
            text="Create Account",
            font=("Arial", 22, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        welcome.pack(pady=(0, 5))
        
        subtitle = tk.Label(
            form,
            text="Join us to start tracking your nutrition",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#999999"
        )
        subtitle.pack(pady=(0, 25))
        
        # Username field
        tk.Label(
            form,
            text="Username",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
            anchor=tk.W
        ).pack(fill=tk.X, pady=(5, 5))
        
        self.register_username_entry = self.create_styled_entry(form)
        self.register_username_entry.bind('<Return>', lambda e: self.handle_register())
        
        # Email field
        tk.Label(
            form,
            text="Email",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
            anchor=tk.W
        ).pack(fill=tk.X, pady=(5, 5))
        
        self.register_email_entry = self.create_styled_entry(form)
        self.register_email_entry.bind('<Return>', lambda e: self.handle_register())
        
        # Password field
        tk.Label(
            form,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
            anchor=tk.W
        ).pack(fill=tk.X, pady=(5, 5))
        
        self.register_password_entry = self.create_styled_entry(form, show_password=True)
        self.register_password_entry.bind('<Return>', lambda e: self.handle_register())
        
        # Hint
        tk.Label(
            form,
            text="Min 6 characters, include letters and numbers",
            font=("Arial", 9),
            bg="#ffffff",
            fg="#999999"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Register button
        register_btn = tk.Button(
            form,
            text="Create Account",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.RAISED,
            bd=0,
            cursor="hand2",
            command=self.handle_register,
            height=2
        )
        register_btn.pack(fill=tk.X, pady=(15, 0))
        
        return form
    
    def show_login_form(self):
        """Show login form"""
        self.register_form.pack_forget()
        self.login_form.pack(fill=tk.BOTH, expand=True)
        
        # Update button styles
        self.login_tab_btn.config(
            bg="#4CAF50",
            fg="white",
            font=("Arial", 13, "bold")
        )
        self.register_tab_btn.config(
            bg="#e8e8e8",
            fg="#666666",
            font=("Arial", 13)
        )
    
    def show_register_form(self):
        """Show register form"""
        self.login_form.pack_forget()
        self.register_form.pack(fill=tk.BOTH, expand=True)
        
        # Update button styles
        self.register_tab_btn.config(
            bg="#4CAF50",
            fg="white",
            font=("Arial", 13, "bold")
        )
        self.login_tab_btn.config(
            bg="#e8e8e8",
            fg="#666666",
            font=("Arial", 13)
        )
    
    def handle_login(self):
        """Handle login"""
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        success, message, user_data = self.auth.login_user(username, password)
        
        if success:
            messagebox.showinfo("Success", f"Welcome back, {user_data['username']}!")
            self.root.destroy()
            self.on_login_success(user_data)
        else:
            messagebox.showerror("Login Failed", message)
            self.login_password_entry.delete(0, tk.END)
    
    def handle_register(self):
        """Handle register"""
        username = self.register_username_entry.get().strip()
        email = self.register_email_entry.get().strip()
        password = self.register_password_entry.get()
        
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = self.auth.register_user(username, email, password)
        
        if success:
            messagebox.showinfo("Success", f"Account created successfully!\n\nWelcome {username}! You can now login.")
            self.register_username_entry.delete(0, tk.END)
            self.register_email_entry.delete(0, tk.END)
            self.register_password_entry.delete(0, tk.END)
            self.show_login_form()
            self.login_username_entry.insert(0, username)
        else:
            messagebox.showerror("Registration Failed", message)
    
    def run(self):
        """Run the login window"""
        self.root.mainloop()


if __name__ == "__main__":
    def on_success(user_data):
        print(f"Login successful! User: {user_data['username']}")
    
    login_window = LoginWindow(on_login_success=on_success)
    login_window.run()