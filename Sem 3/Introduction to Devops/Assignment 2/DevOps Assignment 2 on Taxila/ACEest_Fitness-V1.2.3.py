import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Define a clean, modern color palette
COLOR_PRIMARY = "#4CAF50"   # Vibrant Green (Success/Add)
COLOR_SECONDARY = "#2196F3" # Bright Blue (Info/Summary)
COLOR_BACKGROUND = "#F8F9FA" # Very Light Gray
COLOR_CARD_BG = "#FFFFFF"   # White for data entry cards
COLOR_TEXT = "#343A40"      # Dark Charcoal

class FitnessTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("ACEest Fitness & Gym Tracker")
        master.geometry("850x700") # Slightly larger window
        master.config(bg=COLOR_BACKGROUND)

        # --- UI Styling Setup (Ttk Style) ---
        self.style = ttk.Style()
        self.style.theme_use("clam") 
        
        # Notebook (Tab) Styling
        self.style.configure("TNotebook", background=COLOR_BACKGROUND, borderwidth=0)
        self.style.configure("TNotebook.Tab", 
                             font=("Helvetica", 12, "bold"), 
                             foreground=COLOR_TEXT,
                             padding=[15, 8],
                             background=COLOR_BACKGROUND)
        self.style.map("TNotebook.Tab", 
                       background=[("selected", COLOR_CARD_BG)],
                       foreground=[("selected", COLOR_PRIMARY)])

        # Button Styling
        self.style.configure("Primary.TButton", 
                             font=("Arial", 11, "bold"), 
                             background=COLOR_PRIMARY, 
                             foreground=COLOR_CARD_BG,
                             padding=10)
        self.style.map("Primary.TButton", background=[('active', '#388E3C')])
        
        self.style.configure("Secondary.TButton", 
                             font=("Arial", 11, "bold"), 
                             background=COLOR_SECONDARY, 
                             foreground=COLOR_CARD_BG,
                             padding=10)
        self.style.map("Secondary.TButton", background=[('active', '#1976D2')])
        
        
        # Initialize workout dictionary (to store logged data)
        self.workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        # Tabs Frames - Using COLOR_BACKGROUND for tab content
        self.log_tab = tk.Frame(self.notebook, bg=COLOR_BACKGROUND)
        self.chart_tab = tk.Frame(self.notebook, bg=COLOR_BACKGROUND)
        self.diet_tab = tk.Frame(self.notebook, bg=COLOR_BACKGROUND)
        self.progress_tab = tk.Frame(self.notebook, bg=COLOR_CARD_BG) # White BG for charts

        self.notebook.add(self.log_tab, text="🏋️ Log Workouts")
        self.notebook.add(self.chart_tab, text="💡 Workout Plan")
        self.notebook.add(self.diet_tab, text="🥗 Diet Guide")
        self.notebook.add(self.progress_tab, text="📈 Progress Tracker")
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Initialize sections
        self.create_log_tab()
        self.create_workout_plan_tab()
        self.create_diet_guide_tab()
        self.create_progress_tab()
        
        self.update_progress_charts() # Initial chart draw

    # --- Utility Methods ---
    def on_tab_change(self, event):
        """Called when a tab is switched to refresh content."""
        selected_tab = self.notebook.tab(self.notebook.select(), "text").strip()
        if "Progress Tracker" in selected_tab:
            self.update_progress_charts()
            
    # ------------------ LOG WORKOUTS TAB ------------------ #
    def create_log_tab(self):
        # Header
        tk.Label(self.log_tab, text="ACEest Session Logger", font=("Inter", 20, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_TEXT).pack(pady=(20, 10))
        tk.Label(self.log_tab, text="Track your progress with precision.", font=("Inter", 12), bg=COLOR_BACKGROUND, fg="#6C757D").pack(pady=(0, 20))
        
        # Input Card Container
        log_card = tk.Frame(self.log_tab, bg=COLOR_CARD_BG, padx=40, pady=30, relief=tk.RAISED, bd=0, highlightbackground="#E9ECEF", highlightthickness=1)
        log_card.pack(pady=10, padx=100, fill="x")

        # Category Selection
        self.category_var = tk.StringVar(value="Workout")
        tk.Label(log_card, text="Category:", font=("Inter", 12, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.category_menu = ttk.Combobox(log_card, textvariable=self.category_var, 
                                          values=list(self.workouts.keys()), state="readonly", width=30, font=("Inter", 11))
        self.category_menu.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Exercise Input
        tk.Label(log_card, text="Exercise Name:", font=("Inter", 12, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.workout_entry = tk.Entry(log_card, width=30, font=("Inter", 11), bd=1, relief=tk.FLAT, highlightcolor=COLOR_PRIMARY, highlightthickness=1)
        self.workout_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Duration Input
        tk.Label(log_card, text="Duration (min):", font=("Inter", 12, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.duration_entry = tk.Entry(log_card, width=15, font=("Inter", 11), bd=1, relief=tk.FLAT, highlightcolor=COLOR_PRIMARY, highlightthickness=1)
        self.duration_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        # Button Frame
        button_frame = tk.Frame(self.log_tab, bg=COLOR_BACKGROUND)
        button_frame.pack(pady=30)

        # Buttons with new Ttk styling
        ttk.Button(button_frame, text="✅ ADD SESSION", command=self.add_workout, style="Primary.TButton", width=18).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="📋 VIEW SUMMARY", command=self.view_summary, style="Secondary.TButton", width=18).grid(row=0, column=1, padx=15)

        # Status Bar
        self.status_label = tk.Label(self.log_tab, text="Welcome! Ready for a great session.", bd=1, relief=tk.FLAT, anchor=tk.W, bg=COLOR_CARD_BG, fg="#6C757D", font=("Inter", 10))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def add_workout(self):
        category = self.category_var.get()
        workout = self.workout_entry.get().strip()
        duration_str = self.duration_entry.get().strip()

        if not workout or not duration_str:
            messagebox.showerror("Input Error", "Please enter both exercise and duration.")
            return

        try:
            duration = int(duration_str)
            if duration <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Duration must be a positive whole number.")
            return

        entry = {
            "exercise": workout,
            "duration": duration,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.workouts[category].append(entry)

        self.workout_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.status_label.config(text=f"Added {workout} ({duration} min) to {category}! 💪")
        
        self.update_progress_charts()
        messagebox.showinfo("Success", f"{workout} added successfully!")

    def view_summary(self):
        if not any(self.workouts.values()):
            messagebox.showinfo("Summary", "No sessions logged yet! Start tracking your workouts.")
            return

        summary_window = tk.Toplevel(self.master)
        summary_window.title("Detailed Workout Summary")
        summary_window.geometry("550x550")
        summary_window.config(bg=COLOR_CARD_BG)

        tk.Label(summary_window, text="🏋️ Full Session History", font=("Inter", 16, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).pack(pady=10)
        
        # Frame for Scrollbar and Text
        text_frame = tk.Frame(summary_window, bg=COLOR_CARD_BG)
        text_frame.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        summary_text = tk.Text(text_frame, height=20, width=55, wrap=tk.WORD, font=("Inter", 10), bg=COLOR_BACKGROUND, fg=COLOR_TEXT, yscrollcommand=scrollbar.set, relief=tk.FLAT)
        summary_text.pack(fill="both", expand=True)
        scrollbar.config(command=summary_text.yview)

        total_time = 0
        
        for category, sessions in self.workouts.items():
            summary_text.insert(tk.END, f"--- {category.upper()} ---\n", category.lower())
            summary_text.tag_config(category.lower(), font=("Inter", 12, "bold"), foreground=COLOR_SECONDARY if category=="Warm-up" else COLOR_PRIMARY if category=="Workout" else "#FFC107")
            
            if sessions:
                for i, entry in enumerate(sessions, 1):
                    line = f"  {i}. {entry['exercise']} - {entry['duration']} min | Date: {entry['timestamp'].split(' ')[0]}\n"
                    summary_text.insert(tk.END, line)
                    total_time += entry['duration']
            else:
                summary_text.insert(tk.END, "  No sessions recorded.\n", "italic")
                summary_text.tag_config("italic", font=("Inter", 10, "italic"), foreground="#888")
            summary_text.insert(tk.END, "\n")
            
        summary_text.insert(tk.END, f"--- LIFETIME TOTALS ---\n", "total_header")
        summary_text.tag_config("total_header", font=("Inter", 13, "bold"), foreground="#DC3545")
        summary_text.insert(tk.END, f"  Total Training Time: {total_time} minutes\n", "total_value")
        summary_text.tag_config("total_value", font=("Inter", 12, "bold"), foreground="#DC3545")

        summary_text.config(state=tk.DISABLED) # Make it read-only

    # ------------------ WORKOUT PLAN TAB ------------------ #
    def create_workout_plan_tab(self):
        tk.Label(self.chart_tab, text="💡 Personalized Workout Plan Guide", font=("Inter", 20, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_TEXT).pack(pady=20)
        
        plan_card = tk.Frame(self.chart_tab, bg=COLOR_CARD_BG, padx=30, pady=20, bd=0, relief=tk.FLAT, highlightbackground="#E9ECEF", highlightthickness=1)
        plan_card.pack(pady=10, padx=50, fill="x")

        chart_data = {
            "Warm-up (5-10 min)": ["5 min light cardio (Jog/Cycle) to raise heart rate.", "Jumping Jacks (30 reps) for dynamic mobility.", "Arm Circles (15 Fwd/Bwd) to prepare shoulders."],
            "Strength & Cardio (45-60 min)": ["Push-ups (3 sets of 10-15) - Upper body strength.", "Squats (3 sets of 15-20) - Lower body foundation.", "Plank (3 sets of 60 seconds) - Core stabilization.", "Lunges (3 sets of 10/leg) - Balance and leg development."],
            "Cool-down (5 min)": ["Slow Walking - Bring heart rate down gradually.", "Static Stretching (Hold 30s each) - Focus on major muscle groups.", "Deep Breathing Exercises - Aid recovery and relaxation."]
        }

        for category, exercises in chart_data.items():
            tk.Label(plan_card, text=f"🔥 {category}", font=("Inter", 14, "bold"), bg=COLOR_CARD_BG, fg=COLOR_SECONDARY).pack(anchor="w", padx=10, pady=(15, 5))
            for ex in exercises:
                tk.Label(plan_card, text=f"   • {ex}", font=("Inter", 11), bg=COLOR_CARD_BG, fg="#495057", wraplength=700, justify=tk.LEFT).pack(anchor="w", padx=30)
                
    # ------------------ DIET GUIDE TAB ------------------ #
    def create_diet_guide_tab(self):
        tk.Label(self.diet_tab, text="🥗 Nutritional Goal Setting Guide", font=("Inter", 20, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_TEXT).pack(pady=20)
        
        diet_card = tk.Frame(self.diet_tab, bg=COLOR_CARD_BG, padx=30, pady=20, bd=0, relief=tk.FLAT, highlightbackground="#E9ECEF", highlightthickness=1)
        diet_card.pack(pady=10, padx=50, fill="x")

        diet_plans = {
            "🎯 Weight Loss Focus (Calorie Deficit)": ["Breakfast: Oatmeal with Berries (High Fiber).", "Lunch: Grilled Chicken/Tofu Salad (Lean Protein).", "Dinner: Vegetable Soup with Lentils (Low Calorie, High Volume)."],
            "💪 Muscle Gain Focus (High Protein)": ["Breakfast: 3 Egg Omelet, Spinach, Whole-wheat Toast (Protein/Carb combo).", "Lunch: Chicken Breast, Quinoa, and Steamed Veggies (Balanced Meal).", "Post-Workout: Protein Shake & Greek Yogurt (Immediate Recovery)."],
            "🏃 Endurance Focus (Complex Carbs)": ["Pre-Workout: Banana & Peanut Butter (Quick Energy).", "Lunch: Whole Grain Pasta with Light Sauce (Sustainable Carbs).", "Dinner: Salmon & Avocado Salad (Omega-3s and Healthy Fats)."]
        }

        for goal, foods in diet_plans.items():
            tk.Label(diet_card, text=f"{goal}", font=("Inter", 14, "bold"), bg=COLOR_CARD_BG, fg=COLOR_PRIMARY).pack(anchor="w", padx=10, pady=(15, 5))
            for food in foods:
                tk.Label(diet_card, text=f"   • {food}", font=("Inter", 11), bg=COLOR_CARD_BG, fg="#495057", wraplength=700, justify=tk.LEFT).pack(anchor="w", padx=30)

    # ------------------ PROGRESS TRACKER TAB ------------------ #
    def create_progress_tab(self):
        tk.Label(self.progress_tab, text="📈 Personal Progress Tracker", font=("Inter", 20, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).pack(pady=(20, 10))
        tk.Label(self.progress_tab, text="Visualization of your logged workout time distribution.", font=("Inter", 12), bg=COLOR_CARD_BG, fg="#6C757D").pack(pady=(0, 20))
        
        self.chart_container = tk.Frame(self.progress_tab, bg=COLOR_CARD_BG)
        self.chart_container.pack(pady=10, fill="both", expand=True)
        
        self.chart_canvas = None # Placeholder for the matplotlib canvas

    def update_progress_charts(self):
        """Dynamically update progress visualizations (Bar and Pie Charts)."""
        
        # 1. Clean existing charts
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        # 2. Process data
        totals = {cat: sum(entry['duration'] for entry in sessions) for cat, sessions in self.workouts.items()}
        categories = list(totals.keys())
        values = list(totals.values())
        
        if sum(values) == 0:
            tk.Label(self.chart_container, text="No workout data logged yet. Log a session to see your progress!", 
                     font=("Inter", 14, "italic"), fg="#888", bg=COLOR_CARD_BG).pack(pady=100)
            return

        # 3. Create Matplotlib Figure
        fig = Figure(figsize=(8, 5), dpi=100, facecolor=COLOR_CARD_BG)
        
        # Color palette for consistency
        chart_colors = [COLOR_SECONDARY, COLOR_PRIMARY, "#FFC107"] # Blue, Green, Yellow

        # --- Subplot 1: Bar Chart (Time Spent) ---
        ax1 = fig.add_subplot(121)
        bars = ax1.bar(categories, values, color=chart_colors)
        ax1.set_title("Total Minutes per Category", fontsize=10, color=COLOR_TEXT)
        ax1.set_ylabel("Total Minutes", fontsize=8, color=COLOR_TEXT)
        ax1.tick_params(axis='x', labelsize=8, colors=COLOR_TEXT)
        ax1.tick_params(axis='y', labelsize=8, colors=COLOR_TEXT)
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.grid(axis='y', linestyle='-', alpha=0.3)
        ax1.set_facecolor(COLOR_CARD_BG)

        # --- Subplot 2: Pie Chart (Distribution) ---
        ax2 = fig.add_subplot(122)
        
        # Filter out categories with zero minutes for the pie chart
        pie_labels = [c for c, v in zip(categories, values) if v > 0]
        pie_values = [v for v in values if v > 0]
        pie_colors = [chart_colors[i] for i, v in enumerate(values) if v > 0]
        
        ax2.pie(pie_values, labels=pie_labels, autopct="%1.1f%%", startangle=90, colors=pie_colors, 
                wedgeprops={"edgecolor": "white", 'linewidth': 1}, textprops={'fontsize': 8, 'color': COLOR_TEXT})
        ax2.set_title("Workout Distribution (%)", fontsize=10, color=COLOR_TEXT)
        ax2.axis('equal') 
        ax2.set_facecolor(COLOR_CARD_BG)

        fig.tight_layout(pad=2.0)

        # 4. Embed Matplotlib Figure into Tkinter
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 5. Add a simple text summary below the chart
        total_minutes = sum(values)
        summary_text = f"LIFETIME TOTAL: {total_minutes} minutes logged across all categories."
        tk.Label(self.progress_tab, text=summary_text, font=("Inter", 13, "bold"), bg=COLOR_CARD_BG, fg="#DC3545").pack(pady=(10, 5))


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
