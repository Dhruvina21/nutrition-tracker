import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from app.database import Database
from app.gui.search_window import SearchWindow
from app.gui.log_window import LogWindow
from app.gui.search_window import SearchWindow
from app.gui.log_window import LogWindow
from app.gui.profile_window import ProfileWindow



class MainWindow:
    """
    Main Dashboard Window
    Shows user's nutrition tracking dashboard with:
    - Top Menu Bar
    - Welcome Panel with user info and date
    - Quick Actions buttons
    - Today's Summary Card with nutrition stats
    """
    
    def __init__(self, user_data):
        """
        Initialize main dashboard window
        
        Args:
            user_data (dict): Logged-in user's data
        """
        self.user_data = user_data
        self.db = Database()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Nutrition Tracker - Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f5f5f5")
        
        # Center window
        self.center_window(1200, 800)
        
        # Create UI
        self.create_ui()
        
        # Load today's data
        self.load_today_stats()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_ui(self):
        """Create the complete user interface"""
        # Create top menu bar
        self.create_menu_bar()
        
        # Main content area
        content_frame = tk.Frame(self.root, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Welcome Panel
        self.create_welcome_panel(content_frame)
        
        # Quick Actions
        self.create_quick_actions(content_frame)
        
        # Today's Summary Card
        self.create_summary_card(content_frame)
    
    def create_menu_bar(self):
        """Create top menu bar"""
        menu_frame = tk.Frame(self.root, bg="#4CAF50", height=60)
        menu_frame.pack(fill=tk.X)
        menu_frame.pack_propagate(False)
        
        # Left side - App name
        left_frame = tk.Frame(menu_frame, bg="#4CAF50")
        left_frame.pack(side=tk.LEFT, padx=30)
        
        tk.Label(
            left_frame,
            text="🥗 Nutrition Tracker",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=15)
        
        # Right side - Menu items
        right_frame = tk.Frame(menu_frame, bg="#4CAF50")
        right_frame.pack(side=tk.RIGHT, padx=30)
        
        menu_items = [
            ("🏠 Home", self.go_home),
            ("🔍 Search Foods", self.search_foods),
            ("📝 Log Food", self.log_food),
            ("📊 My Reports", self.view_reports),
            ("👤 Profile", self.view_profile),
            ("🚪 Logout", self.logout)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                right_frame,
                text=text,
                font=("Arial", 10),
                bg="#4CAF50",
                fg="white",
                activebackground="#45a049",
                activeforeground="white",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=command,
                padx=15,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg="#45a049"))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg="#4CAF50"))
    
    def create_welcome_panel(self, parent):
        """Create welcome panel with user info and date"""
        welcome_frame = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT, bd=0)
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add subtle shadow effect with frame
        shadow_frame = tk.Frame(parent, bg="#e0e0e0", height=2)
        shadow_frame.place(in_=welcome_frame, relx=0, rely=1, relwidth=1)
        
        # Content padding
        content = tk.Frame(welcome_frame, bg="#ffffff")
        content.pack(fill=tk.X, padx=30, pady=20)
        
        # Left side - Welcome message
        left = tk.Frame(content, bg="#ffffff")
        left.pack(side=tk.LEFT)
        
        tk.Label(
            left,
            text=f"Welcome back, {self.user_data['username']}! 👋",
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W)
        
        # Current date and time
        current_datetime = datetime.now().strftime("%A, %B %d, %Y • %I:%M %p")
        tk.Label(
            left,
            text=current_datetime,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#666666"
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # Right side - Quick stats
        right = tk.Frame(content, bg="#ffffff")
        right.pack(side=tk.RIGHT)
        
        # Quick stats container
        stats_frame = tk.Frame(right, bg="#f0f0f0", relief=tk.FLAT)
        stats_frame.pack()
        
        # Foods logged today
        self.foods_logged_label = tk.Label(
            stats_frame,
            text="0",
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            fg="#4CAF50"
        )
        self.foods_logged_label.pack(padx=30, pady=(15, 0))
        
        tk.Label(
            stats_frame,
            text="Foods Logged Today",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666666"
        ).pack(padx=30, pady=(0, 15))
    
    def create_quick_actions(self, parent):
        """Create quick actions buttons"""
        actions_frame = tk.Frame(parent, bg="#f5f5f5")
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Section title
        tk.Label(
            actions_frame,
            text="Quick Actions",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Buttons container
        buttons_frame = tk.Frame(actions_frame, bg="#f5f5f5")
        buttons_frame.pack(fill=tk.X)
        
        # Quick action buttons
        actions = [
            {
                "icon": "🔍",
                "title": "Quick Food Search",
                "desc": "Find nutritional info",
                "command": self.quick_search,
                "color": "#2196F3"
            },
            {
                "icon": "🍽️",
                "title": "Log a Meal",
                "desc": "Add to your diary",
                "command": self.quick_log,
                "color": "#FF9800"
            },
            {
                "icon": "📋",
                "title": "View Today's Log",
                "desc": "See what you ate",
                "command": self.view_today,
                "color": "#9C27B0"
            },
            {
                "icon": "📈",
                "title": "Weekly Summary",
                "desc": "Track your progress",
                "command": self.view_weekly,
                "color": "#4CAF50"
            }
        ]
        
        for i, action in enumerate(actions):
            self.create_action_button(buttons_frame, action, i)
    
    def create_action_button(self, parent, action, index):
        """Create a single action button"""
        # Button frame
        btn_frame = tk.Frame(
            parent,
            bg="#ffffff",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2"
        )
        btn_frame.grid(row=0, column=index, padx=10, sticky="ew")
        parent.grid_columnconfigure(index, weight=1)
        
        # Add shadow effect
        shadow = tk.Frame(parent, bg="#e0e0e0", height=2)
        shadow.grid(row=1, column=index, sticky="ew", padx=10)
        
        # Make entire frame clickable
        btn_frame.bind('<Button-1>', lambda e: action['command']())
        
        # Content
        content = tk.Frame(btn_frame, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        content.bind('<Button-1>', lambda e: action['command']())
        
        # Icon with colored background
        icon_frame = tk.Frame(content, bg=action['color'], width=60, height=60)
        icon_frame.pack(pady=(0, 15))
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(
            icon_frame,
            text=action['icon'],
            font=("Arial", 28),
            bg=action['color'],
            fg="white"
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        icon_label.bind('<Button-1>', lambda e: action['command']())
        
        # Title
        title = tk.Label(
            content,
            text=action['title'],
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        title.pack()
        title.bind('<Button-1>', lambda e: action['command']())
        
        # Description
        desc = tk.Label(
            content,
            text=action['desc'],
            font=("Arial", 10),
            bg="#ffffff",
            fg="#999999"
        )
        desc.pack(pady=(5, 0))
        desc.bind('<Button-1>', lambda e: action['command']())
        
        # Hover effect
        def on_enter(e):
            btn_frame.config(bg="#f9f9f9")
            content.config(bg="#f9f9f9")
            title.config(bg="#f9f9f9")
            desc.config(bg="#f9f9f9")
        
        def on_leave(e):
            btn_frame.config(bg="#ffffff")
            content.config(bg="#ffffff")
            title.config(bg="#ffffff")
            desc.config(bg="#ffffff")
        
        btn_frame.bind('<Enter>', on_enter)
        btn_frame.bind('<Leave>', on_leave)
        content.bind('<Enter>', on_enter)
        content.bind('<Leave>', on_leave)
    
    def create_summary_card(self, parent):
        """Create today's summary card with nutrition stats"""
        summary_frame = tk.Frame(parent, bg="#f5f5f5")
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        # Section title
        title_frame = tk.Frame(summary_frame, bg="#f5f5f5")
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            title_frame,
            text="Today's Summary",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        ).pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = tk.Button(
            title_frame,
            text="🔄 Refresh",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#666666",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.load_today_stats,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Summary card
        card = tk.Frame(summary_frame, bg="#ffffff", relief=tk.FLAT)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Card content
        content = tk.Frame(card, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Nutrition stats grid
        stats_frame = tk.Frame(content, bg="#ffffff")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Define nutrition stats
        stats = [
            {
                "label": "Total Calories",
                "value_var": "calories",
                "unit": "kcal",
                "color": "#FF5722",
                "icon": "🔥"
            },
            {
                "label": "Protein",
                "value_var": "protein",
                "unit": "g",
                "color": "#2196F3",
                "icon": "💪"
            },
            {
                "label": "Carbohydrates",
                "value_var": "carbs",
                "unit": "g",
                "color": "#FF9800",
                "icon": "🌾"
            },
            {
                "label": "Fat",
                "value_var": "fat",
                "unit": "g",
                "color": "#9C27B0",
                "icon": "🥑"
            }
        ]
        
        # Create stat cards in a 2x2 grid
        self.stat_labels = {}
        
        for i, stat in enumerate(stats):
            row = i // 2
            col = i % 2
            
            stat_card = tk.Frame(
                stats_frame,
                bg="#f8f8f8",
                relief=tk.FLAT,
                bd=0
            )
            stat_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Configure grid weights
            stats_frame.grid_rowconfigure(row, weight=1)
            stats_frame.grid_columnconfigure(col, weight=1)
            
            # Stat content
            stat_content = tk.Frame(stat_card, bg="#f8f8f8")
            stat_content.pack(expand=True, padx=30, pady=25)
            
            # Icon and label
            header = tk.Frame(stat_content, bg="#f8f8f8")
            header.pack()
            
            tk.Label(
                header,
                text=f"{stat['icon']} {stat['label']}",
                font=("Arial", 12, "bold"),
                bg="#f8f8f8",
                fg="#666666"
            ).pack()
            
            # Value
            value_label = tk.Label(
                stat_content,
                text="0",
                font=("Arial", 36, "bold"),
                bg="#f8f8f8",
                fg=stat['color']
            )
            value_label.pack(pady=(10, 0))
            
            # Store reference to update later
            self.stat_labels[stat['value_var']] = value_label
            
            # Unit
            tk.Label(
                stat_content,
                text=stat['unit'],
                font=("Arial", 11),
                bg="#f8f8f8",
                fg="#999999"
            ).pack()
    
    def load_today_stats(self):
        """Load today's nutrition statistics from database"""
        try:
            user_id = self.user_data['user_id']
            today = datetime.now().date()
            
            # Query to get today's nutrition totals
            query = '''
                SELECT 
                    COUNT(DISTINCT fi.food_id) as food_count,
                    COALESCE(SUM(n.calories), 0) as total_calories,
                    COALESCE(SUM(n.protein), 0) as total_protein,
                    COALESCE(SUM(n.carbs), 0) as total_carbs,
                    COALESCE(SUM(n.fat), 0) as total_fat
                FROM food_info fi
                JOIN has_nutrition hn ON fi.food_id = hn.food_id
                JOIN nutrition n ON hn.nutrition_id = n.nutrition_id
                WHERE fi.user_id = %s AND fi.log_date = %s;
            '''
            
            result = self.db.execute_query_one(query, (user_id, today))
            
            if result:
                food_count, calories, protein, carbs, fat = result
                
                # Update UI
                self.foods_logged_label.config(text=str(food_count))
                self.stat_labels['calories'].config(text=f"{int(calories)}")
                self.stat_labels['protein'].config(text=f"{round(protein, 1)}")
                self.stat_labels['carbs'].config(text=f"{round(carbs, 1)}")
                self.stat_labels['fat'].config(text=f"{round(fat, 1)}")
            else:
                # No data for today
                self.foods_logged_label.config(text="0")
                self.stat_labels['calories'].config(text="0")
                self.stat_labels['protein'].config(text="0")
                self.stat_labels['carbs'].config(text="0")
                self.stat_labels['fat'].config(text="0")
        
        except Exception as e:
            print(f"Error loading today's stats: {e}")
            messagebox.showerror("Error", "Failed to load today's statistics")
    
    # Menu bar actions
    def go_home(self):
        """Go to home/dashboard"""
        messagebox.showinfo("Home", "You're already on the home page!")
    
    def search_foods(self):
        """Open food search window"""
        messagebox.showinfo(
            "Coming Soon",
            "Food Search feature will be implemented in Phase 6!"
        )
    
    def log_food(self):
        """Open food logging window"""
        messagebox.showinfo(
            "Coming Soon",
            "Food Logging feature will be implemented in Phase 7!"
        )
    
    def view_reports(self):
        """Open reports window"""
        messagebox.showinfo(
            "Coming Soon",
            "Reports feature will be implemented in Phase 8!"
        )
    
    def view_profile(self):
        """View user profile"""
        ProfileWindow(user_data=self.user_data).run()
    
    def logout(self):
        """Logout user"""
    def quick_search(self):
        """Quick food search - opens search window"""
        SearchWindow(database=self.db, user_data=self.user_data)
    
    def quick_log(self):
        """Quick log a meal - opens log window"""
        log_win = tk.Toplevel(self.root)
        log_win.title("Food Log")
        LogWindow(log_win, user_id=self.user_data['user_id'], username=self.user_data['username'])
    
    def view_today(self):
        """View today's food log"""
        self.quick_log()

    
    
    def view_weekly(self):
        """View weekly summary"""
        messagebox.showinfo(
            "Weekly Summary",
            "Weekly Summary will be implemented in Phase 8!"
        )
    
    def run(self):
        """Run the main window"""
        self.root.mainloop()


# Test the window
if __name__ == "__main__":
    # Mock user data for testing
    test_user = {
        'user_id': 1,
        'username': 'Ashna',
        'email': 'ashna@example.com',
        'registration_date': '2024-11-21'
    }
    
    window = MainWindow(test_user)
    window.run()