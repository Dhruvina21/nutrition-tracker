"""
Login/Register Window - Modern Design
Beautiful GUI for user authentication
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.auth import Auth


class LoginWindow:
    """
    Modern Login and Registration Window
    """
    
    def __init__(self, on_login_success):
        """
        Initialize login window
        
        Args:
            on_login_success: Callback function when login is successful
                             Should accept user_data dict as parameter
        """
        self.on_login_success = on_login_success
        self.auth = Auth()
        
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
        
        # Left side - Branding section
        left_frame = tk.Frame(main_frame, bg="#4CAF50", width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        left_frame.pack_propagate(False)
        
        self.create_left_panel(left_frame)
        
        # Right side - Form section
        right_frame = tk.Frame(main_frame, bg="#ffffff", width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)
        
        self.create_right_panel(right_frame)
    
    def create_left_panel(self, parent):
        """Create the left branding panel"""
        container = tk.Frame(parent, bg="#4CAF50")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo
        logo = tk.Label(
            container,
            text="🥗",
            font=("Arial", 120),
            bg="#4CAF50"
        )
        logo.pack(pady=(0, 20))
        
        # App name
        app_name = tk.Label(
            container,
            text="Nutrition Tracker",
            font=("Arial", 32, "bold"),
            bg="#4CAF50",
            fg="white"
        )
        app_name.pack(pady=(0, 10))
        
        # Tagline
        tagline = tk.Label(
            container,
            text="Track your meals, achieve your goals",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="#E8F5E9"
        )
        tagline.pack(pady=(0, 40))
        
        # Features
        features = [
            "🍎 Search 1000+ foods",
            "📊 Track daily nutrition",
            "📈 View detailed reports",
            "🎯 Set and achieve goals"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                container,
                text=feature,
                font=("Arial", 12),
                bg="#4CAF50",
                fg="white",
                anchor=tk.W
            )
            feature_label.pack(pady=5, padx=40)
    
    def create_right_panel(self, parent):
        """Create the right form panel"""
        container = tk.Frame(parent, bg="#ffffff")
        container.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Tab buttons
        tab_frame = tk.Frame(container, bg="#ffffff")
        tab_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.login_tab_btn = tk.Button(
            tab_frame,
            text="Login",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_login_form,
            width=12,
            height=2
        )
        self.login_tab_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.register_tab_btn = tk.Button(
            tab_frame,
            text="Register",
            font=("Arial", 14),
            bg="#f5f5f5",
            fg="#666666",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_register_form,
            width=12,
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
    
    def create_login_form(self, parent):
        """Create login form"""
        form = tk.Frame(parent, bg="#ffffff")
        
        welcome = tk.Label(
            form,
            text="Welcome Back! 👋",
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        welcome.pack(pady=(0, 10))
        
        subtitle = tk.Label(
            form,
            text="Enter your credentials to continue",
            font=("Arial", 11),
            bg="#ffffff",
            fg="#999999"
        )
        subtitle.pack(pady=(0, 40))
        
        # Username
        tk.Label(form, text="Username", font=("Arial", 11, "bold"), bg="#ffffff", fg="#333333", anchor=tk.W).pack(fill=tk.X, pady=(15, 5))
        
        username_frame = tk.Frame(form, bg="#e0e0e0", height=50)
        username_frame.pack(fill=tk.X, pady=(0, 5))
        username_frame.pack_propagate(False)
        
        self.login_username_entry = tk.Entry(username_frame, font=("Arial", 12), relief=tk.FLAT, bg="#ffffff", fg="#333333")
        self.login_username_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.login_username_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Password
        tk.Label(form, text="Password", font=("Arial", 11, "bold"), bg="#ffffff", fg="#333333", anchor=tk.W).pack(fill=tk.X, pady=(15, 5))
        
        password_frame = tk.Frame(form, bg="#e0e0e0", height=50)
        password_frame.pack(fill=tk.X, pady=(0, 5))
        password_frame.pack_propagate(False)
        
        self.login_password_entry = tk.Entry(password_frame, font=("Arial", 12), relief=tk.FLAT, bg="#ffffff", fg="#333333", show="●")
        self.login_password_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.login_password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Login button
        login_btn = tk.Button(
            form,
            text="Login →",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.handle_login,
            height=2
        )
        login_btn.pack(fill=tk.X, pady=(30, 0))
        login_btn.bind('<Enter>', lambda e: login_btn.config(bg="#45a049"))
        login_btn.bind('<Leave>', lambda e: login_btn.config(bg="#4CAF50"))
        
        return form
    
    def create_register_form(self, parent):
        """Create registration form"""
        form = tk.Frame(parent, bg="#ffffff")
        
        welcome = tk.Label(
            form,
            text="Create Account 🚀",
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        welcome.pack(pady=(0, 10))
        
        subtitle = tk.Label(
            form,
            text="Join us to start tracking your nutrition",
            font=("Arial", 11),
            bg="#ffffff",
            fg="#999999"
        )
        subtitle.pack(pady=(0, 30))
        
        # Username
        tk.Label(form, text="Username", font=("Arial", 11, "bold"), bg="#ffffff", fg="#333333", anchor=tk.W).pack(fill=tk.X, pady=(15, 5))
        
        username_frame = tk.Frame(form, bg="#e0e0e0", height=50)
        username_frame.pack(fill=tk.X, pady=(0, 5))
        username_frame.pack_propagate(False)
        
        self.register_username_entry = tk.Entry(username_frame, font=("Arial", 12), relief=tk.FLAT, bg="#ffffff", fg="#333333")
        self.register_username_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.register_username_entry.bind('<Return>', lambda e: self.handle_register())
        
        # Email
        tk.Label(form, text="Email", font=("Arial", 11, "bold"), bg="#ffffff", fg="#333333", anchor=tk.W).pack(fill=tk.X, pady=(15, 5))
        
        email_frame = tk.Frame(form, bg="#e0e0e0", height=50)
        email_frame.pack(fill=tk.X, pady=(0, 5))
        email_frame.pack_propagate(False)
        
        self.register_email_entry = tk.Entry(email_frame, font=("Arial", 12), relief=tk.FLAT, bg="#ffffff", fg="#333333")
        self.register_email_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.register_email_entry.bind('<Return>', lambda e: self.handle_register())
        
        # Password
        tk.Label(form, text="Password", font=("Arial", 11, "bold"), bg="#ffffff", fg="#333333", anchor=tk.W).pack(fill=tk.X, pady=(15, 5))
        
        password_frame = tk.Frame(form, bg="#e0e0e0", height=50)
        password_frame.pack(fill=tk.X, pady=(0, 5))
        password_frame.pack_propagate(False)
        
        self.register_password_entry = tk.Entry(password_frame, font=("Arial", 12), relief=tk.FLAT, bg="#ffffff", fg="#333333", show="●")
        self.register_password_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.register_password_entry.bind('<Return>', lambda e: self.handle_register())
        
        # Hint
        tk.Label(form, text="💡 Min 6 chars, use letters and numbers", font=("Arial", 9), bg="#ffffff", fg="#999999").pack(anchor=tk.W, pady=(5, 0))
        
        # Register button
        register_btn = tk.Button(
            form,
            text="Create Account →",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.handle_register,
            height=2
        )
        register_btn.pack(fill=tk.X, pady=(20, 0))
        register_btn.bind('<Enter>', lambda e: register_btn.config(bg="#45a049"))
        register_btn.bind('<Leave>', lambda e: register_btn.config(bg="#4CAF50"))
        
        return form
    
    def show_login_form(self):
        """Show login form"""
        self.register_form.pack_forget()
        self.login_form.pack(fill=tk.BOTH, expand=True)
        self.login_tab_btn.config(bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
        self.register_tab_btn.config(bg="#f5f5f5", fg="#666666", font=("Arial", 14))
    
    def show_register_form(self):
        """Show register form"""
        self.login_form.pack_forget()
        self.register_form.pack(fill=tk.BOTH, expand=True)
        self.register_tab_btn.config(bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
        self.login_tab_btn.config(bg="#f5f5f5", fg="#666666", font=("Arial", 14))
    
    def handle_login(self):
        """Handle login"""
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        success, message, user_data = self.auth.login_user(username, password)
        
        if success:
            messagebox.showinfo("✅ Success", f"Welcome back, {user_data['username']}!")
            self.root.destroy()
            self.on_login_success(user_data)
        else:
            messagebox.showerror("❌ Login Failed", message)
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
            messagebox.showinfo("✅ Success", f"Account created!\n\nWelcome {username}! You can now login.")
            self.register_username_entry.delete(0, tk.END)
            self.register_email_entry.delete(0, tk.END)
            self.register_password_entry.delete(0, tk.END)
            self.show_login_form()
            self.login_username_entry.insert(0, username)
        else:
            messagebox.showerror("❌ Registration Failed", message)
    
    def run(self):
        """Run the login window"""
        self.root.mainloop()


if __name__ == "__main__":
    def on_success(user_data):
        print(f"✅ Login successful! User: {user_data['username']}")
    
    login_window = LoginWindow(on_login_success=on_success)
    login_window.run()