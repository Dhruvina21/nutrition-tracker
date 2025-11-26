"""
Phase 7: Food Logging System - MANYA

Tkinter window for:
- Logging foods for a user on a given date
- Viewing all logs for a selected date
- Showing nutrition totals
- Deleting selected log entries

File: app/gui/log_window.py

This file is designed so it can be tested standalone with:
    python -m app.gui.log_window

Assumptions:
- PostgreSQL is set up with the nutrition_tracker schema
- config/db_config.py defines DB_CONFIG dict with connection params
- Tables: USER, FOOD, CATEGORY, NUTRITION, Belong_to, has_nutrition, FOOD_INFO
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

import psycopg2
from tkcalendar import DateEntry

from config.db_config import DB_CONFIG


# ---------------------------------------------------------------------
# Database helper
# ---------------------------------------------------------------------
def get_connection():
    """Create a new database connection using DB_CONFIG."""
    return psycopg2.connect(**DB_CONFIG)


# ---------------------------------------------------------------------
# Log Window (as a Frame, NOT a popup)
# ---------------------------------------------------------------------
class LogWindow(tk.Frame):
    """
    Phase 7: Food Logging System GUI.

    Features:
    1. Log Food Form
       - Select food (dropdown)
       - Select date (date picker)
       - Select serving size (number of servings, 1–5)
       - Add notes (optional, UI only)
    2. View Logs
       - Display all logged foods for a date
       - Show nutritional totals (calories, protein, fat, carbs)
       - Delete selected log entries
    3. Quick Log
       - quick_log_food() helper for logging directly from search results
    """

    def __init__(self, master, user_id: int, username: str, *args, **kwargs):
        super().__init__(master, bg="#f5f5f5", *args, **kwargs)

        # make this frame fill the window
        self.pack(fill=tk.BOTH, expand=True)

        # main window properties (since this is a page, not popup)
        master.title("Food Log - Nutrition Tracker")
        master.minsize(900, 550)

        self.user_id = user_id
        self.username = username

        # map "Apple" -> 1 etc.
        self.food_id_by_name: dict[str, int] = {}

        # selected date as string yyyy-mm-dd
        self.selected_date = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))

        # servings (number of servings, default 1)
        self.servings_var = tk.IntVar(value=1)

        # --- build UI ---
        self._build_top_bar()
        self._build_main_layout()

        # Load initial data
        self._load_food_options()
        self._load_logs_for_date(self.selected_date.get())

    # ------------------------------------------------------------------
    # UI LAYOUT
    # ------------------------------------------------------------------
    def _build_top_bar(self):
        """Green bar at the top: title + logged-in user."""
        top_bar = tk.Frame(self, bg="#4CAF50", height=50)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        top_bar.pack_propagate(False)

        left = tk.Frame(top_bar, bg="#4CAF50")
        left.pack(side=tk.LEFT, padx=20)

        tk.Label(
            left,
            text="🥗 Food Log",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.LEFT)

        right = tk.Frame(top_bar, bg="#4CAF50")
        right.pack(side=tk.RIGHT, padx=20)

        tk.Label(
            right,
            text=f"Logged in as: {self.username}",
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.RIGHT)

    def _build_main_layout(self):
        """Main white frame with log form, table and totals."""
        outer = tk.Frame(self, bg="#f5f5f5")
        outer.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

        # top: log form
        self._build_form(outer)

        # middle: table
        self._build_table(outer)

        # bottom: totals + high/low summary
        self._build_totals(outer)

    # ------------------ form ------------------
    def _build_form(self, parent):
        form_frame = tk.LabelFrame(
            parent,
            text=" Log Food ",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#333333",
            bd=1,
            relief=tk.GROOVE,
        )
        form_frame.pack(fill=tk.X, pady=(0, 10))

        for i in range(8):
            form_frame.grid_columnconfigure(i, weight=1)

        # Date picker
        tk.Label(
            form_frame,
            text="Date",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).grid(row=0, column=0, padx=(15, 5), pady=10, sticky="w")

        self.date_entry = DateEntry(
            form_frame,
            textvariable=self.selected_date,
            date_pattern="yyyy-mm-dd",
            width=12,
        )
        self.date_entry.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="w")
        self.date_entry.bind("<<DateEntrySelected>>", lambda e: self._on_date_changed())

        # Food dropdown
        tk.Label(
            form_frame,
            text="Food",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).grid(row=0, column=2, padx=(5, 5), pady=10, sticky="w")

        self.food_var = tk.StringVar()
        self.food_combo = ttk.Combobox(
            form_frame,
            textvariable=self.food_var,
            state="readonly",
            width=40,
        )
        self.food_combo.grid(row=0, column=3, padx=(0, 20), pady=10, sticky="we")

        # Serving size (simple: number of servings)
        tk.Label(
            form_frame,
            text="Servings",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).grid(row=0, column=4, padx=(5, 5), pady=10, sticky="w")

        self.servings_spin = tk.Spinbox(
            form_frame,
            from_=1,
            to=5,
            textvariable=self.servings_var,
            width=5,
        )
        self.servings_spin.grid(row=0, column=5, padx=(0, 20), pady=10, sticky="w")

        # Log button (GREEN with BLACK text so it's visible)
        log_btn = tk.Button(
            form_frame,
            text="Log Food",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="black",              # <- black text for visibility
            activebackground="#45a049",
            activeforeground="black",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._log_food,
            height=1,
        )
        log_btn.grid(row=0, column=6, padx=(0, 10), pady=10, sticky="we")

        # Refresh button
        refresh_btn = tk.Button(
            form_frame,
            text="Refresh Logs",
            font=("Arial", 11),
            bg="#e0e0e0",
            fg="#333333",
            activebackground="#d5d5d5",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._refresh_logs,
            height=1,
        )
        refresh_btn.grid(row=0, column=7, padx=(0, 15), pady=10, sticky="we")

        # Optional notes (UI only)
        tk.Label(
            form_frame,
            text="Notes (optional)",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).grid(row=1, column=0, padx=(15, 5), pady=(0, 10), sticky="nw")

        self.notes_text = tk.Text(
            form_frame,
            height=2,
            width=80,
            font=("Arial", 9),
            bg="#fafafa",
        )
        self.notes_text.grid(
            row=1, column=1, columnspan=7, padx=(0, 15), pady=(0, 10), sticky="we"
        )

    # ------------------ table ------------------
    def _build_table(self, parent):
        table_frame = tk.LabelFrame(
            parent,
            text=" Logged Foods ",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#333333",
            bd=1,
            relief=tk.GROOVE,
        )
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.table_title_var = tk.StringVar(
            value=f"Logged Foods for {self.selected_date.get()}"
        )
        top_label = tk.Label(
            table_frame,
            textvariable=self.table_title_var,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#555555",
        )
        self.table_title_label = top_label
        top_label.pack(anchor="w", padx=15, pady=(5, 0))

        columns = (
            "food_name",
            "category",
            "calories",
            "protein",
            "fat",
            "carbs",
            "log_date",
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12,
        )

        self.tree.heading("food_name", text="Food")
        self.tree.heading("category", text="Category")
        self.tree.heading("calories", text="Calories")
        self.tree.heading("protein", text="Protein (g)")
        self.tree.heading("fat", text="Fat (g)")
        self.tree.heading("carbs", text="Carbs (g)")
        self.tree.heading("log_date", text="Date")

        self.tree.column("food_name", width=220)
        self.tree.column("category", width=130)
        self.tree.column("calories", width=90, anchor="e")
        self.tree.column("protein", width=90, anchor="e")
        self.tree.column("fat", width=90, anchor="e")
        self.tree.column("carbs", width=90, anchor="e")
        self.tree.column("log_date", width=100, anchor="center")

        self.tree.pack(side="left", fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

        # Delete button under the table
        btn_frame = tk.Frame(parent, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=(0, 5))

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Selected Log",
            font=("Arial", 11),
            bg="#e53935",
            fg="white",
            activebackground="#c62828",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self._delete_selected_log,
            height=1,
        )
        delete_btn.pack(side="right", padx=10)

    # ------------------ totals ------------------
    def _build_totals(self, parent):
        totals_frame = tk.LabelFrame(
            parent,
            text=" Daily Totals ",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#333333",
            bd=1,
            relief=tk.GROOVE,
        )
        totals_frame.pack(fill=tk.X)

        self.total_calories_var = tk.StringVar(value="0")
        self.total_protein_var = tk.StringVar(value="0")
        self.total_fat_var = tk.StringVar(value="0")
        self.total_carbs_var = tk.StringVar(value="0")
        self.summary_var = tk.StringVar(value="")

        labels = [
            ("Calories:", self.total_calories_var),
            ("Protein (g):", self.total_protein_var),
            ("Fat (g):", self.total_fat_var),
            ("Carbs (g):", self.total_carbs_var),
        ]

        col = 0
        for text, var in labels:
            tk.Label(
                totals_frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#ffffff",
                fg="#333333",
            ).grid(row=0, column=col, padx=(15, 5), pady=8, sticky="e")
            tk.Label(
                totals_frame,
                textvariable=var,
                font=("Arial", 10),
                bg="#ffffff",
                fg="#333333",
            ).grid(row=0, column=col + 1, padx=(0, 20), pady=8, sticky="w")
            col += 2

        # high / low calorie summary
        tk.Label(
            totals_frame,
            text="Day Summary:",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).grid(row=1, column=0, padx=(15, 5), pady=(0, 8), sticky="e")

        tk.Label(
            totals_frame,
            textvariable=self.summary_var,
            font=("Arial", 10),
            bg="#ffffff",
            fg="#555555",
        ).grid(row=1, column=1, columnspan=7, padx=(0, 15), pady=(0, 8), sticky="w")

    # ------------------------------------------------------------------
    # DATA LOADING
    # ------------------------------------------------------------------
    def _load_food_options(self):
        """Load all foods into dropdown."""
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT food_id, food_name FROM FOOD ORDER BY food_name;")
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load foods:\n{e}")
            rows = []
        finally:
            if conn is not None:
                conn.close()

        names = []
        self.food_id_by_name.clear()
        for food_id, food_name in rows:
            names.append(food_name)
            self.food_id_by_name[food_name] = food_id

        self.food_combo["values"] = names
        if names:
            self.food_combo.current(0)

    def _load_logs_for_date(self, log_date_str: str):
        """Load all logs for the given date and update table + totals."""
        # clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        totals = {"calories": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}

        conn = None
        rows = []
        try:
            conn = get_connection()
            cur = conn.cursor()

            # View user's logs for a date
            query = """
                SELECT
                    fi.food_id,
                    f.food_name,
                    c.category_name,
                    n.calories,
                    n.protein,
                    n.fat,
                    n.carbs,
                    fi.log_date
                FROM FOOD_INFO fi
                JOIN FOOD f ON fi.food_id = f.food_id
                JOIN Belong_to bt ON f.food_id = bt.food_id
                JOIN CATEGORY c ON bt.category_id = c.category_id
                JOIN has_nutrition hn ON f.food_id = hn.food_id
                JOIN NUTRITION n ON hn.nutrition_id = n.nutrition_id
                WHERE fi.user_id = %s AND fi.log_date = %s
                ORDER BY f.food_name;
            """
            cur.execute(query, (self.user_id, log_date_str))
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load logs:\n{e}")
        finally:
            if conn is not None:
                conn.close()

        # insert rows; iid IS UNIQUE (uses index) to avoid duplicate error
        for index, (
            food_id,
            food_name,
            category,
            calories,
            protein,
            fat,
            carbs,
            log_date,
        ) in enumerate(rows):
            iid = f"{food_id}_{log_date}_{index}"
            self.tree.insert(
                "",
                "end",
                iid=iid,
                values=(food_name, category, calories, protein, fat, carbs, log_date),
            )

            totals["calories"] += float(calories or 0)
            totals["protein"] += float(protein or 0)
            totals["fat"] += float(fat or 0)
            totals["carbs"] += float(carbs or 0)

        # update totals
        self.total_calories_var.set(f"{totals['calories']:.0f}")
        self.total_protein_var.set(f"{totals['protein']:.1f}")
        self.total_fat_var.set(f"{totals['fat']:.1f}")
        self.total_carbs_var.set(f"{totals['carbs']:.1f}")

        # simple high / low calorie summary
        if totals["calories"] >= 2000:
            self.summary_var.set("High calorie day 🔥")
        elif totals["calories"] <= 1200 and totals["calories"] > 0:
            self.summary_var.set("Low calorie day 🥗")
        elif totals["calories"] == 0:
            self.summary_var.set("No foods logged yet.")
        else:
            self.summary_var.set("Moderate calorie day 👍")

        # update title above table
        self.table_title_var.set(f"Logged Foods for {self.selected_date.get()}")

    # ------------------------------------------------------------------
    # EVENT HANDLERS
    # ------------------------------------------------------------------
    def _on_date_changed(self):
        self.selected_date.set(self.date_entry.get_date().strftime("%Y-%m-%d"))
        self._refresh_logs()

    def _refresh_logs(self):
        self._load_logs_for_date(self.selected_date.get())

    def _log_food(self):
        """Insert one or more rows into FOOD_INFO based on servings."""
        food_name = self.food_var.get().strip()
        if not food_name:
            messagebox.showwarning("Missing Data", "Please select a food to log.")
            return

        food_id = self.food_id_by_name.get(food_name)
        if not food_id:
            messagebox.showerror("Error", "Could not find selected food.")
            return

        log_date_str = self.selected_date.get()

        # servings: number of rows we will insert
        try:
            servings = int(self.servings_var.get())
        except ValueError:
            servings = 1
        servings = max(1, min(servings, 5))

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            for _ in range(servings):
                cur.execute(
                    "INSERT INTO FOOD_INFO (user_id, food_id, log_date) "
                    "VALUES (%s, %s, %s);",
                    (self.user_id, food_id, log_date_str),
                )

            conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to log food:\n{e}")
            return
        finally:
            if conn is not None:
                conn.close()

        messagebox.showinfo(
            "Success",
            f"Logged {servings} serving(s) of {food_name} on {log_date_str}.",
        )

        # clear notes text (they are not stored in DB for this phase)
        self.notes_text.delete("1.0", tk.END)

        self._refresh_logs()

    def _delete_selected_log(self):
        """Delete the selected log entry from FOOD_INFO."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select a log entry to delete."
            )
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        food_name = values[0]
        log_date_str = values[-1]

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Delete log for '{food_name}' on {log_date_str}?",
        ):
            return

        try:
            # iid format: "<food_id>_<date>_<index>"
            food_id = int(item_id.split("_")[0])
        except ValueError:
            messagebox.showerror("Error", "Could not parse selected item id.")
            return

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM FOOD_INFO "
                "WHERE user_id = %s AND food_id = %s AND log_date = %s "
                "LIMIT 1;",
                (self.user_id, food_id, log_date_str),
            )
            conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete log:\n{e}")
            return
        finally:
            if conn is not None:
                conn.close()

        self._refresh_logs()

    # ------------------------------------------------------------------
    # QUICK LOG API (for Phase 7 "Quick Log" from search window)
    # ------------------------------------------------------------------
    def quick_log_food(self, food_id: int, log_date_str: str | None = None):
        """
        Helper for 'Quick Log' from other windows (e.g., SearchWindow).

        Logs a single serving of the given food_id for this user.
        If log_date_str is None, today's date is used.
        """
        if log_date_str is None:
            log_date_str = date.today().strftime("%Y-%m-%d")

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO FOOD_INFO (user_id, food_id, log_date) "
                "VALUES (%s, %s, %s);",
                (self.user_id, food_id, log_date_str),
            )
            conn.commit()
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Failed to quick-log food:\n{e}"
            )
            return
        finally:
            if conn is not None:
                conn.close()

        # refresh if we’re looking at that date
        if log_date_str == self.selected_date.get():
            self._refresh_logs()


# ---------------------------------------------------------------------
# Standalone testing 
# ---------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x650")
    app = LogWindow(root, user_id=1, username="demo_user")
    root.mainloop()