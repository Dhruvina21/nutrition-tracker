"""
Search Window - Food Search Interface (COMPLETE VERSION)
With GREEN vertical divider lines between panels
"""

import tkinter as tk
from tkinter import ttk, messagebox


class SearchWindow:
    """
    Complete Food Search Interface
    """
    
    def __init__(self, database, user_data):
        """
        Initialize search window
        
        Args:
            database: Database instance
            user_data: Current user data dict
        """
        self.db = database
        self.user_data = user_data
        self.current_food = None
        self.search_results = []
        self.categories = []
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Food Search - Nutrition Tracker")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        self.root.configure(bg="#f5f5f5")
        
        # Center window
        self.center_window(1400, 800)
        
        # Load categories
        self.load_categories()
        
        # Create UI
        self.create_ui()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_categories(self):
        """Load food categories from database"""
        try:
            query = "SELECT category_id, category_name FROM CATEGORY ORDER BY category_name;"
            results = self.db.execute_query(query, fetch=True)
            self.categories = [(row[0], row[1]) for row in results] if results else []
        except Exception as e:
            print(f"Error loading categories: {e}")
            self.categories = []
    
    def create_ui(self):
        """Create the user interface"""
        # Top bar
        self.create_top_bar()
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Configure column weights to make panels equal
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)  # Left panel
        main_container.grid_columnconfigure(1, weight=0)  # Divider 1
        main_container.grid_columnconfigure(2, weight=1)  # Middle panel
        main_container.grid_columnconfigure(3, weight=0)  # Divider 2
        main_container.grid_columnconfigure(4, weight=1)  # Right panel
        
        # Left panel - Search and filters (EQUAL WIDTH)
        left_panel = tk.Frame(main_container, bg="#ffffff")
        left_panel.grid(row=0, column=0, sticky="nsew")
        
        self.create_search_panel(left_panel)
        
        # GREEN DIVIDER 1
        divider1 = tk.Frame(main_container, bg="#4CAF50", width=3)
        divider1.grid(row=0, column=1, sticky="ns")
        
        # Middle panel - Search results (EQUAL WIDTH)
        middle_panel = tk.Frame(main_container, bg="#ffffff")
        middle_panel.grid(row=0, column=2, sticky="nsew")
        
        self.create_results_panel(middle_panel)
        
        # GREEN DIVIDER 2
        divider2 = tk.Frame(main_container, bg="#4CAF50", width=3)
        divider2.grid(row=0, column=3, sticky="ns")
        
        # Right panel - Food details (EQUAL WIDTH)
        right_panel = tk.Frame(main_container, bg="#ffffff")
        right_panel.grid(row=0, column=4, sticky="nsew")
        
        self.create_details_panel(right_panel)
    
    def create_top_bar(self):
        """Create top bar with user info"""
        top_bar = tk.Frame(self.root, bg="#4CAF50", height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Left side
        left_frame = tk.Frame(top_bar, bg="#4CAF50")
        left_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            left_frame,
            text="🥗 Food Search",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.LEFT)
        
        # Right side
        right_frame = tk.Frame(top_bar, bg="#4CAF50")
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        tk.Label(
            right_frame,
            text=f"Welcome, {self.user_data.get('username', 'User')}!",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.RIGHT, padx=10)
        
        
    
    def create_search_panel(self, parent):
        """Create search and filter panel"""
        # Header
        header = tk.Frame(parent, bg="#4CAF50")
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="🔍 Search & Filter",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=15
        ).pack()
        
        # Content
        content = tk.Frame(parent, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Search by name
        tk.Label(
            content,
            text="Search by Name",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        search_frame = tk.Frame(content, bg="#e0e0e0")
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 16),
            relief=tk.FLAT,
            bg="#ffffff"
        )
        self.search_entry.pack(fill=tk.X, padx=3, pady=3, ipady=8)
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        search_btn = tk.Button(
            content,
            text="🔍 Search",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.perform_search,
            height=2
        )
        search_btn.pack(fill=tk.X, pady=(0, 20))
        
        # Divider
        tk.Frame(content, bg="#e0e0e0", height=2).pack(fill=tk.X, pady=20)
        
        # Browse by category
        tk.Label(
            content,
            text="Browse by Category",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        category_frame = tk.Frame(content, bg="#ffffff")
        category_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(category_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(category_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for cat_id, cat_name in self.categories:
            btn = tk.Button(
                scrollable_frame,
                text=cat_name,
                font=("Arial", 13),
                bg="#f5f5f5",
                fg="#333333",
                relief=tk.FLAT,
                cursor="hand2",
                anchor=tk.W,
                padx=15,
                pady=12,
                command=lambda c=cat_id, n=cat_name: self.search_by_category(c, n)
            )
            btn.pack(fill=tk.X, pady=2)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg="#e0e0e0"))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg="#f5f5f5"))
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_results_panel(self, parent):
        """Create search results panel"""
        header = tk.Frame(parent, bg="#4CAF50")
        header.pack(fill=tk.X)
        
        self.results_label = tk.Label(
            header,
            text="📋 Search Results (0)",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=15
        )
        self.results_label.pack()
        
        results_container = tk.Frame(parent, bg="#ffffff")
        results_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        canvas = tk.Canvas(results_container, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=canvas.yview)
        
        self.results_frame = tk.Frame(canvas, bg="#ffffff")
        
        self.results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.no_results_label = tk.Label(
            self.results_frame,
            text="🔍 Use search or select a category to find foods",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#999999",
            pady=50
        )
        self.no_results_label.pack()
    
    def create_details_panel(self, parent):
        """Create food details panel"""
        header = tk.Frame(parent, bg="#4CAF50")
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📊 Food Details",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=15
        ).pack()
        
        details_container = tk.Frame(parent, bg="#ffffff")
        details_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(details_container, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_container, orient="vertical", command=canvas.yview)
        
        self.details_frame = tk.Frame(canvas, bg="#ffffff")
        
        self.details_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.details_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            self.details_frame,
            text="👈 Select a food to view details",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#999999",
            pady=50
        ).pack()
    
    def perform_search(self):
        """Perform food search by name"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Search", "Please enter a search term")
            return
        
        try:
            query = """
                SELECT f.food_id, f.food_name, c.category_name
                FROM FOOD f
                LEFT JOIN Belong_to bt ON f.food_id = bt.food_id
                LEFT JOIN CATEGORY c ON bt.category_id = c.category_id
                WHERE LOWER(f.food_name) LIKE LOWER(%s)
                ORDER BY f.food_name
                LIMIT 100;
            """
            
            results = self.db.execute_query(query, (f'%{search_term}%',), fetch=True)
            self.display_results(results, f"Search: '{search_term}'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
    
    def search_by_category(self, category_id, category_name):
        """Search foods by category"""
        try:
            query = """
                SELECT f.food_id, f.food_name, c.category_name
                FROM FOOD f
                JOIN Belong_to bt ON f.food_id = bt.food_id
                JOIN CATEGORY c ON bt.category_id = c.category_id
                WHERE c.category_id = %s
                ORDER BY f.food_name;
            """
            
            results = self.db.execute_query(query, (category_id,), fetch=True)
            self.display_results(results, f"Category: {category_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Category search failed: {e}")
    
    def display_results(self, results, search_info):
        """Display search results"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not results or len(results) == 0:
            self.results_label.config(text=f"📋 Search Results (0) - {search_info}")
            tk.Label(
                self.results_frame,
                text="No results found",
                font=("Arial", 14),
                bg="#ffffff",
                fg="#999999",
                pady=50
            ).pack()
            return
        
        self.search_results = results
        self.results_label.config(text=f"📋 Results ({len(results)}) - {search_info}")
        
        for food in results:
            self.create_result_card(food)
    
    def create_result_card(self, food):
        """Create a result card for a food item"""
        food_id, name, category = food
        
        # Get nutrition preview
        nutrition_query = """
            SELECT n.calories, n.protein, n.fat, n.carbs, n.measure, n.grams
            FROM NUTRITION n
            JOIN has_nutrition hn ON n.nutrition_id = hn.nutrition_id
            WHERE hn.food_id = %s
            LIMIT 1;
        """
        nutrition = self.db.execute_query_one(nutrition_query, (food_id,))
        
        # Card
        card = tk.Frame(self.results_frame, bg="#f9f9f9", relief=tk.SOLID, borderwidth=1)
        card.pack(fill=tk.X, pady=5, padx=5)
        
        card.bind('<Button-1>', lambda e: self.show_food_details(food_id))
        card.bind('<Enter>', lambda e: card.config(bg="#e8f5e9", cursor="hand2"))
        card.bind('<Leave>', lambda e: card.config(bg="#f9f9f9"))
        
        content = tk.Frame(card, bg="#f9f9f9")
        content.pack(fill=tk.BOTH, padx=15, pady=12)
        content.bind('<Button-1>', lambda e: self.show_food_details(food_id))
        
        # Food name
        name_label = tk.Label(
            content,
            text=name,
            font=("Arial", 14, "bold"),
            bg="#f9f9f9",
            fg="#333333",
            anchor=tk.W
        )
        name_label.pack(fill=tk.X)
        name_label.bind('<Button-1>', lambda e: self.show_food_details(food_id))
        
        # Category
        if category:
            cat_label = tk.Label(
                content,
                text=f"📁 {category}",
                font=("Arial", 11),
                bg="#f9f9f9",
                fg="#666666",
                anchor=tk.W
            )
            cat_label.pack(fill=tk.X)
            cat_label.bind('<Button-1>', lambda e: self.show_food_details(food_id))
        
        # Nutrition preview
        if nutrition:
            calories, protein, fat, carbs, measure, grams = nutrition
            
            info_frame = tk.Frame(content, bg="#f9f9f9")
            info_frame.pack(fill=tk.X, pady=(8, 0))
            info_frame.bind('<Button-1>', lambda e: self.show_food_details(food_id))
            
            nutrients = [
                ("🔥", f"{calories:.0f} cal" if calories else "N/A"),
                ("💪", f"{protein:.1f}g protein" if protein else "N/A"),
                ("🥑", f"{fat:.1f}g fat" if fat else "N/A"),
                ("🌾", f"{carbs:.1f}g carbs" if carbs else "N/A")
            ]
            
            for emoji, text in nutrients:
                label = tk.Label(
                    info_frame,
                    text=f"{emoji} {text}",
                    font=("Arial", 11),
                    bg="#f9f9f9",
                    fg="#555555"
                )
                label.pack(side=tk.LEFT, padx=(0, 15))
                label.bind('<Button-1>', lambda e: self.show_food_details(food_id))
    
    def show_food_details(self, food_id):
        """Show detailed information for selected food"""
        try:
            # Get food info
            food_query = """
                SELECT f.food_id, f.food_name, c.category_name
                FROM FOOD f
                LEFT JOIN Belong_to bt ON f.food_id = bt.food_id
                LEFT JOIN CATEGORY c ON bt.category_id = c.category_id
                WHERE f.food_id = %s;
            """
            
            food_result = self.db.execute_query_one(food_query, (food_id,))
            
            if not food_result:
                messagebox.showerror("Error", "Food not found")
                return
            
            # Get nutrition info
            nutrition_query = """
                SELECT n.nutrition_id, n.measure, n.grams, n.calories, n.protein, 
                       n.fat, n.sat_fat, n.fiber, n.carbs
                FROM NUTRITION n
                JOIN has_nutrition hn ON n.nutrition_id = hn.nutrition_id
                WHERE hn.food_id = %s;
            """
            
            nutrition_results = self.db.execute_query(nutrition_query, (food_id,), fetch=True)
            
            self.display_food_details(food_result, nutrition_results)
            
        except Exception as e:
            print(f"Error showing food details: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load food details: {e}")
    
    def display_food_details(self, food_data, nutrition_data):
        """Display detailed food information"""
        # Clear previous
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        food_id, name, category = food_data
        
        # Food name
        tk.Label(
            self.details_frame,
            text=name,
            font=("Arial", 18, "bold"),
            bg="#ffffff",
            fg="#333333",
            wraplength=380,
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Category
        if category:
            tk.Label(
                self.details_frame,
                text=f"📁 {category}",
                font=("Arial", 12),
                bg="#ffffff",
                fg="#666666"
            ).pack(anchor=tk.W, pady=(0, 20))
        
        # Nutrition info
        if nutrition_data:
            tk.Label(
                self.details_frame,
                text="Serving Sizes Available",
                font=("Arial", 14, "bold"),
                bg="#ffffff",
                fg="#333333"
            ).pack(anchor=tk.W, pady=(0, 10))
            
            for nutrition in nutrition_data:
                nutrition_id, measure, grams, calories, protein, fat, sat_fat, fiber, carbs = nutrition
                
                # Serving frame with GREEN BORDER
                serving_frame = tk.Frame(
                    self.details_frame, 
                    bg="#f9f9f9", 
                    relief=tk.SOLID, 
                    borderwidth=3,
                    highlightbackground="#4CAF50",
                    highlightthickness=3
                )
                serving_frame.pack(fill=tk.X, pady=(0, 15))
                
                # Header
                header_frame = tk.Frame(serving_frame, bg="#e8f5e9")
                header_frame.pack(fill=tk.X)
                
                tk.Label(
                    header_frame,
                    text=f"📏 {measure} ({grams}g)",
                    font=("Arial", 13, "bold"),
                    bg="#e8f5e9",
                    fg="#2e7d32"
                ).pack(pady=10)
                
                # Nutrients
                nutrients = [
                    ("🔥 Calories", calories, "kcal"),
                    ("💪 Protein", protein, "g"),
                    ("🥑 Total Fat", fat, "g"),
                    ("🧈 Saturated Fat", sat_fat, "g"),
                    ("🌾 Carbohydrates", carbs, "g"),
                    ("🌿 Fiber", fiber, "g")
                ]
                
                for label, value, unit in nutrients:
                    if value is not None:
                        row = tk.Frame(serving_frame, bg="#f9f9f9")
                        row.pack(fill=tk.X, padx=15, pady=5)
                        
                        tk.Label(
                            row,
                            text=label,
                            font=("Arial", 12),
                            bg="#f9f9f9",
                            fg="#555555"
                        ).pack(side=tk.LEFT)
                        
                        tk.Label(
                            row,
                            text=f"{value:.1f} {unit}",
                            font=("Arial", 12, "bold"),
                            bg="#f9f9f9",
                            fg="#333333"
                        ).pack(side=tk.RIGHT)
                
                # Add button
                add_btn = tk.Button(
                    serving_frame,
                    text=f"➕ Add {measure} to Food Log",
                    font=("Arial", 12, "bold"),
                    bg="#4CAF50",
                    fg="white",
                    relief=tk.FLAT,
                    cursor="hand2",
                    command=lambda fid=food_id: self.add_to_food_log(fid),
                    height=2
                )
                add_btn.pack(fill=tk.X, padx=15, pady=10)
                add_btn.bind('<Enter>', lambda e, b=add_btn: b.config(bg="#45a049"))
                add_btn.bind('<Leave>', lambda e, b=add_btn: b.config(bg="#4CAF50"))
        else:
            tk.Label(
                self.details_frame,
                text="No nutritional information available",
                font=("Arial", 13),
                bg="#ffffff",
                fg="#999999"
            ).pack(pady=20)
    
    
    
    def run(self):
        """Run the search window"""
        self.root.mainloop()


if __name__ == "__main__":
    from app.database import Database
    
    db = Database()
    user_data = {'user_id': 1, 'username': 'TestUser'}
    
    search_window = SearchWindow(db, user_data)
    search_window.run()