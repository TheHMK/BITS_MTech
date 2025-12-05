import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class FitnessTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("ACEest Fitness & Gym Tracker")
        master.geometry("800x650")
        master.resizable(False, False)
        
        # --- UI Styling ---
        self.style = ttk.Style()
        self.style.theme_use("clam")  # A cleaner theme for modern feel
        self.style.configure("TNotebook.Tab", font=("Helvetica", 11, "bold"))
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        
        # Initialize workout dictionary (to store logged data)
        self.workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Tabs Frames
        self.log_tab = tk.Frame(self.notebook, bg="#f0f0f0")  # Light gray background
        self.chart_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.diet_tab = tk.Frame(self.notebook, bg="#f0f0f0")
        self.progress_tab = tk.Frame(self.notebook, bg="white") # White for charts

        self.notebook.add(self.log_tab, text="🏋️ Log Workouts")
        self.notebook.add(self.chart_tab, text="💡 Workout Plan")
        self.notebook.add(self.diet_tab, text="🥗 Diet Guide")
        self.notebook.add(self.progress_tab, text="📈 Progress Tracker")
        
        # Bind the tab change event to refresh charts
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Initialize sections
        self.create_log_tab()
        self.create_workout_plan_tab()
        self.create_diet_guide_tab()
        self.create_progress_tab()
        
        # Initial chart drawing (needed on startup)
        self.update_progress_charts()

    # --- Utility Methods ---
    def on_tab_change(self, event):
        """Called when a tab is switched to refresh content."""
        selected_tab = self.notebook.tab(self.notebook.select(), "text").strip()
        if "Progress Tracker" in selected_tab:
            self.update_progress_charts()
            
    # ------------------ LOG WORKOUTS TAB ------------------ #
    def create_log_tab(self):
        # Header
        tk.Label(self.log_tab, text="ACEest Fitness & Gym Tracker", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#343a40").pack(pady=15)
        
        # Input container frame for better alignment
        input_container = tk.Frame(self.log_tab, bg="#e9ecef", padx=20, pady=20, relief=tk.RAISED, bd=1)
        input_container.pack(pady=10, padx=50, fill="x")

        # Category Selection
        self.category_var = tk.StringVar(value="Workout")
        tk.Label(input_container, text="Select Category:", font=("Arial", 12, "bold"), bg="#e9ecef").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.category_menu = ttk.Combobox(input_container, textvariable=self.category_var, 
                                          values=list(self.workouts.keys()), state="readonly", width=20, font=("Arial", 11))
        self.category_menu.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Exercise Input
        tk.Label(input_container, text="Exercise:", font=("Arial", 12, "bold"), bg="#e9ecef").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.workout_entry = tk.Entry(input_container, width=30, font=("Arial", 11))
        self.workout_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Duration Input
        tk.Label(input_container, text="Duration (min):", font=("Arial", 12, "bold"), bg="#e9ecef").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.duration_entry = tk.Entry(input_container, width=10, font=("Arial", 11))
        self.duration_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Button Frame
        button_frame = tk.Frame(self.log_tab, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Custom Button Styling
        self.style.configure("Add.TButton", background="#28a745", foreground="white")
        self.style.configure("Summary.TButton", background="#007bff", foreground="white")

        ttk.Button(button_frame, text="✅ Add Session", command=self.add_workout, width=20, style="Add.TButton").grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="📋 View Summary", command=self.view_summary, width=20, style="Summary.TButton").grid(row=0, column=1, padx=15)

        # Status Bar
        self.status_label = tk.Label(self.log_tab, text="Welcome! Log your first session.", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#fff", fg="#6c757d", font=("Arial", 10))
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
        
        # Automatically update the progress charts after a new log
        self.update_progress_charts()

        messagebox.showinfo("Success", f"{workout} added to {category} category successfully!")

    def view_summary(self):
        if not any(self.workouts.values()):
            messagebox.showinfo("Summary", "No sessions logged yet!")
            return

        summary_window = tk.Toplevel(self.master)
        summary_window.title("Workout Summary")
        summary_window.geometry("500x500")
        summary_window.config(bg="#f8f9fa")

        tk.Label(summary_window, text="📊 Weekly Session Summary", font=("Helvetica", 16, "bold"), bg="#f8f9fa", fg="#343a40").pack(pady=10)
        
        # Use a scrolled text area for better presentation of many entries
        summary_text = tk.Text(summary_window, height=20, width=55, wrap=tk.WORD, font=("Arial", 10), bg="white", fg="#343a40")
        summary_text.pack(pady=10, padx=20)
        
        total_time = 0
        
        for category, sessions in self.workouts.items():
            summary_text.insert(tk.END, f"--- {category.upper()} ---\n", category.lower())
            summary_text.tag_config(category.lower(), font=("Arial", 12, "bold"), foreground="#007bff" if category=="Warm-up" else "#28a745" if category=="Workout" else "#ffc107")
            
            if sessions:
                for i, entry in enumerate(sessions, 1):
                    line = f"  {i}. {entry['exercise']} - {entry['duration']} min | Logged: {entry['timestamp'].split(' ')[0]}\n"
                    summary_text.insert(tk.END, line)
                    total_time += entry['duration']
            else:
                summary_text.insert(tk.END, "  No sessions recorded.\n", "italic")
                summary_text.tag_config("italic", font=("Arial", 10, "italic"), foreground="#888")
            summary_text.insert(tk.END, "\n")
            
        summary_text.insert(tk.END, f"--- TOTAL TIME SPENT ---\n", "total_header")
        summary_text.tag_config("total_header", font=("Arial", 13, "bold"), foreground="#dc3545")
        summary_text.insert(tk.END, f"  Total Time: {total_time} minutes\n", "total_value")
        summary_text.tag_config("total_value", font=("Arial", 12, "bold"), foreground="#dc3545")

        summary_text.config(state=tk.DISABLED) # Make it read-only

    # ------------------ WORKOUT PLAN TAB ------------------ #
    def create_workout_plan_tab(self):
        tk.Label(self.chart_tab, text="💡 Personalized Workout Plan", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#343a40").pack(pady=15)
        
        plan_frame = tk.Frame(self.chart_tab, bg="white", padx=20, pady=10, relief=tk.FLAT, bd=1)
        plan_frame.pack(pady=10, padx=50, fill="x")

        chart_data = {
            "Warm-up (5-10 min)": ["5 min light cardio (Jog/Cycle)", "Jumping Jacks (30 reps)", "Arm Circles (15 Fwd/Bwd)"],
            "Strength Workout (45-60 min)": ["Push-ups (3 sets of 10-15)", "Squats (3 sets of 15-20)", "Plank (3 sets of 60 seconds)", "Lunges (3 sets of 10/leg)"],
            "Cool-down (5 min)": ["Slow Walking", "Static Stretching (Hold 30s each)", "Deep Breathing Exercises"]
        }

        for category, exercises in chart_data.items():
            tk.Label(plan_frame, text=f"🔥 {category}", font=("Arial", 14, "bold"), bg="white", fg="#007bff").pack(anchor="w", padx=10, pady=(10, 5))
            for ex in exercises:
                tk.Label(plan_frame, text=f"   • {ex}", font=("Arial", 12), bg="white", fg="#495057").pack(anchor="w", padx=30)
                
    # ------------------ DIET GUIDE TAB ------------------ #
    def create_diet_guide_tab(self):
        tk.Label(self.diet_tab, text="🥗 Best Diet Guide for Fitness Goals", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#343a40").pack(pady=15)
        
        diet_frame = tk.Frame(self.diet_tab, bg="white", padx=20, pady=10, relief=tk.FLAT, bd=1)
        diet_frame.pack(pady=10, padx=50, fill="x")

        diet_plans = {
            "🎯 Weight Loss": ["Breakfast: Oatmeal with Berries", "Lunch: Grilled Chicken/Tofu Salad", "Dinner: Vegetable Soup with Lentils"],
            "💪 Muscle Gain": ["Breakfast: 3 Egg Omelet, Spinach, Whole-wheat Toast", "Lunch: Chicken Breast, Quinoa, and Steamed Veggies", "Post-Workout: Protein Shake, Greek Yogurt"],
            "🏃 Endurance Focus": ["Pre-Workout: Banana & Peanut Butter", "Lunch: Whole Grain Pasta with Light Sauce", "Dinner: Salmon & Avocado Salad"]
        }

        for goal, foods in diet_plans.items():
            tk.Label(diet_frame, text=f"{goal} Plan:", font=("Arial", 14, "bold"), bg="white", fg="#28a745").pack(anchor="w", padx=10, pady=(10, 5))
            for food in foods:
                tk.Label(diet_frame, text=f"   • {food}", font=("Arial", 12), bg="white", fg="#495057").pack(anchor="w", padx=30)

    # ------------------ PROGRESS TRACKER TAB ------------------ #
    def create_progress_tab(self):
        tk.Label(self.progress_tab, text="📈 Personal Progress Tracker (Minutes Logged)", font=("Helvetica", 18, "bold"), bg="white", fg="#343a40").pack(pady=15)
        
        self.chart_container = tk.Frame(self.progress_tab, bg="white")
        self.chart_container.pack(pady=10)
        
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
            tk.Label(self.chart_container, text="No workout data logged yet. Log a session to see your progress!", font=("Arial", 12, "italic"), fg="#888", bg="white").pack(pady=50)
            return

        # 3. Create Matplotlib Figure
        fig = Figure(figsize=(7.5, 4.5), dpi=100, facecolor='white')
        
        # Color palette for consistency
        colors = ["#007bff", "#28a745", "#ffc107"] # Blue, Green, Yellow

        # --- Subplot 1: Bar Chart (Time Spent) ---
        ax1 = fig.add_subplot(121)
        ax1.bar(categories, values, color=colors)
        ax1.set_title("Time Spent per Category (Min)", fontsize=10)
        ax1.set_ylabel("Total Minutes", fontsize=8)
        ax1.tick_params(axis='x', labelsize=8)
        ax1.tick_params(axis='y', labelsize=8)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # --- Subplot 2: Pie Chart (Distribution) ---
        ax2 = fig.add_subplot(122)
        
        # Filter out categories with zero minutes for the pie chart
        pie_labels = [c for c, v in zip(categories, values) if v > 0]
        pie_values = [v for v in values if v > 0]
        pie_colors = [colors[i] for i, v in enumerate(values) if v > 0]
        
        ax2.pie(pie_values, labels=pie_labels, autopct="%1.1f%%", startangle=90, colors=pie_colors, 
                wedgeprops={"edgecolor": "black", 'linewidth': 0.5}, textprops={'fontsize': 8})
        ax2.set_title("Workout Distribution", fontsize=10)
        ax2.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.

        fig.tight_layout(pad=2.0)

        # 4. Embed Matplotlib Figure into Tkinter
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 5. Add a simple text summary below the chart
        total_minutes = sum(values)
        summary_text = f"Total Training Time Logged: {total_minutes} minutes"
        tk.Label(self.progress_tab, text=summary_text, font=("Arial", 12, "bold"), bg="white", fg="#dc3545").pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
