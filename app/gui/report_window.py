"""
Report Window - Nutrition Reports and Analytics
With Daily, Weekly, and Monthly summaries and visualizations
Can be run standalone for testing: python app/gui/report_window.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')


class ReportWindow:
    """
    Report Window with nutrition analytics and visualizations
    """
    
    def __init__(self, database, user_data):
        """
        Initialize report window
        
        Args:
            database: Database instance
            user_data: Current user data dict
        """
        self.db = database
        self.user_data = user_data
        self.current_view = "daily"
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Nutrition Reports - Nutrition Tracker")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        self.root.configure(bg="#f5f5f5")
        
        # Center window
        self.center_window(1400, 900)
        
        # Create UI
        self.create_ui()
        
        # Load today's report by default
        self.show_daily_report()
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_ui(self):
        """Create the user interface"""
        # Top bar
        self.create_top_bar()
        
        # Navigation tabs
        self.create_navigation()
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#ffffff")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
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
            text="📊 Nutrition Reports",
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
        
        
    
    def create_navigation(self):
        """Create navigation tabs"""
        nav_frame = tk.Frame(self.root, bg="#f5f5f5")
        nav_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        buttons = [
            ("📅 Daily Summary", "daily", self.show_daily_report),
            ("📆 Weekly Summary", "weekly", self.show_weekly_report),
            ("📈 Monthly Overview", "monthly", self.show_monthly_report)
        ]
        
        for text, view_type, command in buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg="#4CAF50" if view_type == self.current_view else "#e0e0e0",
                fg="white" if view_type == self.current_view else "#333333",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda v=view_type, c=command: self.switch_view(v, c),
                padx=30,
                pady=15
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            if view_type != self.current_view:
                btn.bind('<Enter>', lambda e, b=btn: b.config(bg="#d0d0d0"))
                btn.bind('<Leave>', lambda e, b=btn: b.config(bg="#e0e0e0"))
    
    def switch_view(self, view_type, command):
        """Switch between different report views"""
        self.current_view = view_type
        
        # Unpack content_frame temporarily
        self.content_frame.pack_forget()
        
        # Destroy and recreate top bar and navigation
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.content_frame:
                widget.destroy()
        
        # Recreate in correct order
        self.create_top_bar()
        self.create_navigation()
        
        # Repack content_frame LAST
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # THEN load the content
        command()
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_daily_report(self):
        """Show daily nutrition summary"""
        self.clear_content()
        
        # Date selector
        date_frame = tk.Frame(self.content_frame, bg="#ffffff")
        date_frame.pack(fill=tk.X, pady=(10, 20))
        
        tk.Label(
            date_frame,
            text="Select Date:",
            font=("Arial", 14, "bold"),
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=10)
        
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = tk.Entry(
            date_frame,
            textvariable=self.date_var,
            font=("Arial", 12),
            width=15
        )
        date_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            date_frame,
            text="📅 Load Report",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.load_daily_data,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)
        
        # Content area
        self.daily_content = tk.Frame(self.content_frame, bg="#ffffff")
        self.daily_content.pack(fill=tk.BOTH, expand=True)
        
        # Load today's data by default
        self.load_daily_data()
    
    def load_daily_data(self):
        """Load and display daily nutrition data"""
        for widget in self.daily_content.winfo_children():
            widget.destroy()
        
        date_str = self.date_var.get()
        
        try:
            # Get daily totals
            query = """
                SELECT 
                    SUM(n.calories) AS total_calories,
                    SUM(n.protein) AS total_protein,
                    SUM(n.fat) AS total_fat,
                    SUM(n.carbs) AS total_carbs,
                    SUM(n.fiber) AS total_fiber
                FROM food_info fi
                JOIN has_nutrition hn ON fi.food_id = hn.food_id
                JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
                WHERE fi.user_id = %s AND fi.log_date = %s;
            """
            
            totals = self.db.execute_query_one(query, (self.user_data['user_id'], date_str))
            
            if not totals or totals[0] is None:
                tk.Label(
                    self.daily_content,
                    text=f"No food logged for {date_str}",
                    font=("Arial", 14),
                    bg="#ffffff",
                    fg="#999999"
                ).pack(pady=50)
                return
            
            total_calories, total_protein, total_fat, total_carbs, total_fiber = totals
            
            # Get foods list
            foods_query = """
                SELECT f.food_name, n.measure, n.calories, n.protein, n.fat, n.carbs
                FROM food_info fi
                JOIN FOOD f ON fi.food_id = f.food_id
                JOIN has_nutrition hn ON fi.food_id = hn.food_id
                JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
                WHERE fi.user_id = %s AND fi.log_date = %s
                ORDER BY fi.log_id;
            """
            
            foods = self.db.execute_query(foods_query, (self.user_data['user_id'], date_str), fetch=True)
            
            # Create layout
            left_panel = tk.Frame(self.daily_content, bg="#ffffff")
            left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            
            right_panel = tk.Frame(self.daily_content, bg="#ffffff")
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
            
            # Left panel - Summary stats
            self.create_summary_cards(left_panel, total_calories, total_protein, total_fat, total_carbs, total_fiber)
            
            # Foods list
            self.create_foods_list(left_panel, foods)
            
            # Right panel - Pie chart
            self.create_macro_pie_chart(right_panel, total_protein, total_fat, total_carbs)
            
        except Exception as e:
            print(f"Error loading daily data: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load daily report: {e}")
    
    def create_summary_cards(self, parent, calories, protein, fat, carbs, fiber):
        """Create summary cards for daily totals"""
        tk.Label(
            parent,
            text="Daily Totals",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        cards_frame = tk.Frame(parent, bg="#ffffff")
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats = [
            ("🔥 Calories", f"{calories:.0f}", "kcal", "#FF6B6B"),
            ("💪 Protein", f"{protein:.1f}", "g", "#4ECDC4"),
            ("🥑 Fat", f"{fat:.1f}", "g", "#FFE66D"),
            ("🌾 Carbs", f"{carbs:.1f}", "g", "#95E1D3"),
            ("🌿 Fiber", f"{fiber:.1f}", "g", "#A8E6CF")
        ]
        
        for i, (label, value, unit, color) in enumerate(stats):
            card = tk.Frame(cards_frame, bg=color, relief=tk.RAISED, borderwidth=2)
            card.pack(fill=tk.X, pady=5)
            
            tk.Label(
                card,
                text=label,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="#333333"
            ).pack(pady=(10, 5))
            
            tk.Label(
                card,
                text=f"{value} {unit}",
                font=("Arial", 16, "bold"),
                bg=color,
                fg="#333333"
            ).pack(pady=(0, 10))
    
    def create_foods_list(self, parent, foods):
        """Create list of foods consumed"""
        tk.Label(
            parent,
            text="Foods Consumed",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(20, 10))
        
        # Create scrollable frame
        list_frame = tk.Frame(parent, bg="#ffffff")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(list_frame, bg="#ffffff", highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if foods:
            for food_name, measure, calories, protein, fat, carbs in foods:
                food_card = tk.Frame(scrollable_frame, bg="#f9f9f9", relief=tk.SOLID, borderwidth=1)
                food_card.pack(fill=tk.X, pady=5, padx=5)
                
                tk.Label(
                    food_card,
                    text=food_name,
                    font=("Arial", 12, "bold"),
                    bg="#f9f9f9",
                    fg="#333333",
                    anchor=tk.W
                ).pack(fill=tk.X, padx=10, pady=(8, 2))
                
                tk.Label(
                    food_card,
                    text=f"{measure} - {calories:.0f} cal | P: {protein:.1f}g | F: {fat:.1f}g | C: {carbs:.1f}g",
                    font=("Arial", 10),
                    bg="#f9f9f9",
                    fg="#666666",
                    anchor=tk.W
                ).pack(fill=tk.X, padx=10, pady=(0, 8))
        else:
            tk.Label(
                scrollable_frame,
                text="No foods logged",
                font=("Arial", 11),
                bg="#ffffff",
                fg="#999999"
            ).pack(pady=20)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_macro_pie_chart(self, parent, protein, fat, carbs):
        """Create pie chart of macronutrients"""
        tk.Label(
            parent,
            text="Macronutrient Breakdown",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Create figure - SMALLER to fit in frame
        fig = Figure(figsize=(4.5, 3.5), facecolor='white', dpi=90)
        ax = fig.add_subplot(111)
        
        # Data
        protein_cal = protein * 4
        fat_cal = fat * 9
        carbs_cal = carbs * 4
        
        sizes = [protein_cal, fat_cal, carbs_cal]
        labels = [f'Protein\n{protein:.1f}g\n({protein_cal:.0f} cal)',
                  f'Fat\n{fat:.1f}g\n({fat_cal:.0f} cal)',
                  f'Carbs\n{carbs:.1f}g\n({carbs_cal:.0f} cal)']
        colors = ['#4ECDC4', '#FFE66D', '#95E1D3']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 9})
        ax.axis('equal')
        
        # Use tight_layout with padding to prevent cutoff
        fig.tight_layout(pad=1.5)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
    
    def show_weekly_report(self):
        """Show weekly nutrition summary"""
        self.clear_content()
        
        # Week selector
        week_frame = tk.Frame(self.content_frame, bg="#ffffff")
        week_frame.pack(fill=tk.X, pady=(10, 20))
        
        tk.Label(
            week_frame,
            text="Select Week Ending:",
            font=("Arial", 14, "bold"),
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=10)
        
        self.week_end_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        week_entry = tk.Entry(
            week_frame,
            textvariable=self.week_end_var,
            font=("Arial", 12),
            width=15
        )
        week_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            week_frame,
            text="📅 Load Report",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.load_weekly_data,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)
        
        # Content area
        self.weekly_content = tk.Frame(self.content_frame, bg="#ffffff")
        self.weekly_content.pack(fill=tk.BOTH, expand=True)
        
        # Load this week's data by default
        self.load_weekly_data()
    
    def load_weekly_data(self):
        """Load and display weekly nutrition data"""
        for widget in self.weekly_content.winfo_children():
            widget.destroy()
        
        end_date = datetime.strptime(self.week_end_var.get(), "%Y-%m-%d")
        start_date = end_date - timedelta(days=6)
        
        try:
            # Get daily calories for the week
            query = """
                SELECT 
                    fi.log_date,
                    SUM(n.calories) AS daily_calories,
                    SUM(n.protein) AS daily_protein,
                    SUM(n.fat) AS daily_fat,
                    SUM(n.carbs) AS daily_carbs
                FROM food_info fi
                JOIN has_nutrition hn ON fi.food_id = hn.food_id
                JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
                WHERE fi.user_id = %s 
                    AND fi.log_date >= %s 
                    AND fi.log_date <= %s
                GROUP BY fi.log_date
                ORDER BY fi.log_date;
            """
            
            daily_data = self.db.execute_query(query, 
                (self.user_data['user_id'], start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")), 
                fetch=True)
            
            if not daily_data:
                tk.Label(
                    self.weekly_content,
                    text=f"No food logged for week ending {end_date.strftime('%Y-%m-%d')}",
                    font=("Arial", 14),
                    bg="#ffffff",
                    fg="#999999"
                ).pack(pady=50)
                return
            
            # Get most logged foods
            most_logged_query = """
                SELECT f.food_name, COUNT(*) as log_count
                FROM food_info fi
                JOIN FOOD f ON fi.food_id = f.food_id
                WHERE fi.user_id = %s 
                    AND fi.log_date >= %s 
                    AND fi.log_date <= %s
                GROUP BY f.food_name
                ORDER BY log_count DESC
                LIMIT 5;
            """
            
            most_logged = self.db.execute_query(most_logged_query,
                (self.user_data['user_id'], start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                fetch=True)
            
            # Get category distribution
            category_query = """
                SELECT c.category_name, COUNT(*) as count
                FROM food_info fi
                JOIN FOOD f ON fi.food_id = f.food_id
                JOIN Belong_to bt ON f.food_id = bt.food_id
                JOIN CATEGORY c ON bt.category_id = c.category_id
                WHERE fi.user_id = %s 
                    AND fi.log_date >= %s 
                    AND fi.log_date <= %s
                GROUP BY c.category_name
                ORDER BY count DESC;
            """
            
            categories = self.db.execute_query(category_query,
                (self.user_data['user_id'], start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                fetch=True)
            
            # Create layout
            top_panel = tk.Frame(self.weekly_content, bg="#ffffff")
            top_panel.pack(fill=tk.X, padx=10, pady=10)
            
            bottom_panel = tk.Frame(self.weekly_content, bg="#ffffff")
            bottom_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Calculate averages
            avg_calories = sum(day[1] for day in daily_data) / len(daily_data)
            avg_protein = sum(day[2] for day in daily_data) / len(daily_data)
            avg_fat = sum(day[3] for day in daily_data) / len(daily_data)
            avg_carbs = sum(day[4] for day in daily_data) / len(daily_data)
            
            # Top panel - Average stats
            self.create_weekly_averages(top_panel, avg_calories, avg_protein, avg_fat, avg_carbs, len(daily_data))
            
            # Bottom left - Calorie bar chart
            bottom_left = tk.Frame(bottom_panel, bg="#ffffff")
            bottom_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            self.create_calorie_bar_chart(bottom_left, daily_data, start_date, end_date)
            
            # Bottom right - Most logged foods and categories
            bottom_right = tk.Frame(bottom_panel, bg="#ffffff")
            bottom_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
            
            self.create_most_logged_section(bottom_right, most_logged, categories)
            
        except Exception as e:
            print(f"Error loading weekly data: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load weekly report: {e}")
    
    def create_weekly_averages(self, parent, avg_cal, avg_protein, avg_fat, avg_carbs, days):
        """Create average stats cards for the week"""
        tk.Label(
            parent,
            text=f"Weekly Averages ({days} days logged)",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        stats_frame = tk.Frame(parent, bg="#ffffff")
        stats_frame.pack(fill=tk.X)
        
        stats = [
            ("🔥 Avg Calories", f"{avg_cal:.0f}", "kcal/day"),
            ("💪 Avg Protein", f"{avg_protein:.1f}", "g/day"),
            ("🥑 Avg Fat", f"{avg_fat:.1f}", "g/day"),
            ("🌾 Avg Carbs", f"{avg_carbs:.1f}", "g/day")
        ]
        
        for label, value, unit in stats:
            card = tk.Frame(stats_frame, bg="#e8f5e9", relief=tk.RAISED, borderwidth=2)
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            tk.Label(
                card,
                text=label,
                font=("Arial", 11, "bold"),
                bg="#e8f5e9",
                fg="#333333"
            ).pack(pady=(8, 2))
            
            tk.Label(
                card,
                text=f"{value} {unit}",
                font=("Arial", 14, "bold"),
                bg="#e8f5e9",
                fg="#2e7d32"
            ).pack(pady=(0, 8))
    
    def create_calorie_bar_chart(self, parent, daily_data, start_date, end_date):
        """Create bar chart of daily calories"""
        tk.Label(
            parent,
            text="Daily Calorie Intake",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Create figure - SMALLER to fit in frame
        fig = Figure(figsize=(5.5, 3.5), facecolor='white', dpi=90)
        ax = fig.add_subplot(111)
        
        # Create full week data (fill in missing days with 0)
        date_dict = {}
        for day in daily_data:
            date_val = day[0]
            # Convert to string if it's a date object
            if isinstance(date_val, str):
                date_dict[date_val] = day[1]
            else:
                date_dict[date_val.strftime("%Y-%m-%d")] = day[1]
        
        dates = []
        calories = []
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            dates.append(current_date.strftime("%a\n%m/%d"))
            calories.append(date_dict.get(date_str, 0))
            current_date += timedelta(days=1)
        
        # Plot
        bars = ax.bar(range(len(dates)), calories, color='#4CAF50', alpha=0.8)
        ax.set_xlabel('Day', fontsize=10)
        ax.set_ylabel('Calories', fontsize=10)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, fontsize=8)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=8)
        
        # Use tight_layout with padding to prevent cutoff
        fig.tight_layout(pad=1.0)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_most_logged_section(self, parent, most_logged, categories):
        """Create section showing most logged foods and category distribution"""
        # Most logged foods
        tk.Label(
            parent,
            text="Most Logged Foods",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        if most_logged:
            for food_name, count in most_logged[:5]:
                food_frame = tk.Frame(parent, bg="#f9f9f9", relief=tk.SOLID, borderwidth=1)
                food_frame.pack(fill=tk.X, pady=3)
                
                tk.Label(
                    food_frame,
                    text=food_name,
                    font=("Arial", 11),
                    bg="#f9f9f9",
                    anchor=tk.W
                ).pack(side=tk.LEFT, padx=10, pady=5)
                
                tk.Label(
                    food_frame,
                    text=f"{count}x",
                    font=("Arial", 11, "bold"),
                    bg="#f9f9f9",
                    fg="#4CAF50"
                ).pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Category distribution
        tk.Label(
            parent,
            text="Category Distribution",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(20, 10))
        
        if categories:
            for category_name, count in categories:
                cat_frame = tk.Frame(parent, bg="#e8f5e9", relief=tk.SOLID, borderwidth=1)
                cat_frame.pack(fill=tk.X, pady=3)
                
                tk.Label(
                    cat_frame,
                    text=f"📁 {category_name}",
                    font=("Arial", 11),
                    bg="#e8f5e9",
                    anchor=tk.W
                ).pack(side=tk.LEFT, padx=10, pady=5)
                
                tk.Label(
                    cat_frame,
                    text=f"{count}",
                    font=("Arial", 11, "bold"),
                    bg="#e8f5e9",
                    fg="#2e7d32"
                ).pack(side=tk.RIGHT, padx=10, pady=5)
    
    def show_monthly_report(self):
        """Show monthly nutrition overview"""
        self.clear_content()
        
        # Month selector
        month_frame = tk.Frame(self.content_frame, bg="#ffffff")
        month_frame.pack(fill=tk.X, pady=(10, 20))
        
        tk.Label(
            month_frame,
            text="Select Month (YYYY-MM):",
            font=("Arial", 14, "bold"),
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=10)
        
        self.month_var = tk.StringVar(value=datetime.now().strftime("%Y-%m"))
        month_entry = tk.Entry(
            month_frame,
            textvariable=self.month_var,
            font=("Arial", 12),
            width=15
        )
        month_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            month_frame,
            text="📅 Load Report",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.load_monthly_data,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)
        
        # Content area
        self.monthly_content = tk.Frame(self.content_frame, bg="#ffffff")
        self.monthly_content.pack(fill=tk.BOTH, expand=True)
        
        # Load this month's data by default
        self.load_monthly_data()
    
    def load_monthly_data(self):
        """Load and display monthly nutrition data"""
        for widget in self.monthly_content.winfo_children():
            widget.destroy()
        
        year_month = self.month_var.get()
        
        try:
            year, month = map(int, year_month.split('-'))
            start_date = datetime(year, month, 1)
            
            # Calculate last day of month
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
            # Get daily data for the month
            query = """
                SELECT 
                    fi.log_date,
                    SUM(n.calories) AS daily_calories,
                    SUM(n.protein) AS daily_protein,
                    SUM(n.fat) AS daily_fat,
                    SUM(n.carbs) AS daily_carbs
                FROM food_info fi
                JOIN has_nutrition hn ON fi.food_id = hn.food_id
                JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
                WHERE fi.user_id = %s 
                    AND fi.log_date >= %s 
                    AND fi.log_date <= %s
                GROUP BY fi.log_date
                ORDER BY fi.log_date;
            """
            
            monthly_data = self.db.execute_query(query,
                (self.user_data['user_id'], start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                fetch=True)
            
            if not monthly_data:
                tk.Label(
                    self.monthly_content,
                    text=f"No food logged for {year_month}",
                    font=("Arial", 14),
                    bg="#ffffff",
                    fg="#999999"
                ).pack(pady=50)
                return
            
            # Create layout
            top_panel = tk.Frame(self.monthly_content, bg="#ffffff")
            top_panel.pack(fill=tk.X, padx=10, pady=10)
            
            bottom_panel = tk.Frame(self.monthly_content, bg="#ffffff")
            bottom_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Calculate monthly averages
            avg_calories = sum(day[1] for day in monthly_data) / len(monthly_data)
            avg_protein = sum(day[2] for day in monthly_data) / len(monthly_data)
            avg_fat = sum(day[3] for day in monthly_data) / len(monthly_data)
            avg_carbs = sum(day[4] for day in monthly_data) / len(monthly_data)
            
            # Top panel - Monthly stats
            self.create_monthly_stats(top_panel, avg_calories, avg_protein, avg_fat, avg_carbs, 
                                     len(monthly_data), (end_date - start_date).days + 1)
            
            # Bottom - Trend charts
            self.create_trend_charts(bottom_panel, monthly_data, start_date, end_date)
            
        except Exception as e:
            print(f"Error loading monthly data: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load monthly report: {e}")
    
    def create_monthly_stats(self, parent, avg_cal, avg_protein, avg_fat, avg_carbs, days_logged, total_days):
        """Create monthly statistics summary"""
        tk.Label(
            parent,
            text=f"Monthly Overview ({days_logged}/{total_days} days logged)",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        stats_frame = tk.Frame(parent, bg="#ffffff")
        stats_frame.pack(fill=tk.X)
        
        stats = [
            ("🔥 Avg Calories", f"{avg_cal:.0f}", "kcal/day", "#FF6B6B"),
            ("💪 Avg Protein", f"{avg_protein:.1f}", "g/day", "#4ECDC4"),
            ("🥑 Avg Fat", f"{avg_fat:.1f}", "g/day", "#FFE66D"),
            ("🌾 Avg Carbs", f"{avg_carbs:.1f}", "g/day", "#95E1D3"),
        ]
        
        for label, value, unit, color in stats:
            card = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, borderwidth=2)
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            tk.Label(
                card,
                text=label,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="#333333"
            ).pack(pady=(8, 2))
            
            tk.Label(
                card,
                text=f"{value} {unit}",
                font=("Arial", 13, "bold"),
                bg=color,
                fg="#333333"
            ).pack(pady=(0, 8))
    
    def create_trend_charts(self, parent, monthly_data, start_date, end_date):
        """Create trend line charts for the month"""
        tk.Label(
            parent,
            text="Nutrition Trends Over Time",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Create figure with 2 subplots - SMALLER to fit in frame
        fig = Figure(figsize=(9, 3.5), facecolor='white', dpi=90)
        
        # Calories trend
        ax1 = fig.add_subplot(121)
        
        # Handle both datetime.date and string formats
        dates = []
        for day in monthly_data:
            date_val = day[0]
            if isinstance(date_val, str):
                dates.append(datetime.strptime(date_val, "%Y-%m-%d"))
            else:
                # Already a datetime.date object
                dates.append(datetime.combine(date_val, datetime.min.time()))
        
        calories = [day[1] for day in monthly_data]
        
        ax1.plot(dates, calories, marker='o', color='#4CAF50', linewidth=2, markersize=4)
        ax1.set_xlabel('Date', fontsize=9)
        ax1.set_ylabel('Calories', fontsize=9)
        ax1.set_title('Daily Calorie Trend', fontsize=11, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', labelsize=7, rotation=45)
        ax1.tick_params(axis='y', labelsize=8)
        
        # Macros trend
        ax2 = fig.add_subplot(122)
        protein = [day[2] for day in monthly_data]
        fat = [day[3] for day in monthly_data]
        carbs = [day[4] for day in monthly_data]
        
        ax2.plot(dates, protein, marker='o', label='Protein', color='#4ECDC4', linewidth=2, markersize=3)
        ax2.plot(dates, fat, marker='s', label='Fat', color='#FFE66D', linewidth=2, markersize=3)
        ax2.plot(dates, carbs, marker='^', label='Carbs', color='#95E1D3', linewidth=2, markersize=3)
        ax2.set_xlabel('Date', fontsize=9)
        ax2.set_ylabel('Grams', fontsize=9)
        ax2.set_title('Macronutrient Trends', fontsize=11, fontweight='bold')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', labelsize=7, rotation=45)
        ax2.tick_params(axis='y', labelsize=8)
        
        # Use tight_layout with padding to prevent cutoff
        fig.tight_layout(pad=1.0)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        """Run the report window"""
        self.root.mainloop()


# Example usage (for testing)
if __name__ == "__main__":
    # Try to import real database, fall back to mock
    try:
        from app.database import Database
        db = Database()
        print("✅ Connected to real database")
    except Exception as e:
        print(f"⚠️  Could not connect to database: {e}")
        print("📝 Using mock database for testing")
        
        # Mock database for testing
        class MockDB:
            def execute_query(self, query, params=None, fetch=True):
                return []
            def execute_query_one(self, query, params=None):
                return None
        
        db = MockDB()
    
    user_data = {'user_id': 1, 'username': 'TestUser'}
    
    report_window = ReportWindow(db, user_data)
    report_window.run()