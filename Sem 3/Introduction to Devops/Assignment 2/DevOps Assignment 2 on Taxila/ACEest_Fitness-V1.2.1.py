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

        # Initialize workout dictionary
        self.workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.log_tab = tk.Frame(self.notebook, bg="white")
        self.chart_tab = tk.Frame(self.notebook, bg="white")
        self.diet_tab = tk.Frame(self.notebook, bg="white")
        self.progress_tab = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.log_tab, text="🏋️ Log Workouts")
        self.notebook.add(self.chart_tab, text="📊 Workout Chart")
        self.notebook.add(self.diet_tab, text="🥗 Diet Chart")
        self.notebook.add(self.progress_tab, text="📈 Progress Tracker")

        # Initialize sections
        self.create_log_tab()
        self.create_workout_chart_tab()
        self.create_diet_chart_tab()
        self.create_progress_tab()

    # ------------------ LOG TAB ------------------ #
    def create_log_tab(self):
        tk.Label(self.log_tab, text="🏋️ ACEest Fitness & Gym Tracker", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        self.category_var = tk.StringVar(value="Workout")
        tk.Label(self.log_tab, text="Select Category:", font=("Arial", 12), bg="white").pack()
        self.category_menu = ttk.Combobox(self.log_tab, textvariable=self.category_var, values=list(self.workouts.keys()), state="readonly")
        self.category_menu.pack(pady=5)

        # Workout Input Fields
        input_frame = tk.Frame(self.log_tab, bg="white")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Exercise:", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.workout_entry = tk.Entry(input_frame, width=25)
        self.workout_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Duration (min):", font=("Arial", 11), bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(input_frame, width=10)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.log_tab, bg="white")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Session", command=self.add_workout, width=20, bg="#28a745", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="View Summary", command=self.view_summary, width=20, bg="#007bff", fg="white").grid(row=0, column=1, padx=5)

        # Status Bar
        self.status_label = tk.Label(self.log_tab, text="Welcome! Log your first session.", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#f8f9fa")
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
        except ValueError:
            messagebox.showerror("Input Error", "Duration must be a number.")
            return

        entry = {
            "exercise": workout,
            "duration": duration,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.workouts[category].append(entry)

        self.workout_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.status_label.config(text=f"Added {workout} ({duration} min) to {category}!")

        messagebox.showinfo("Success", f"{workout} added to {category} category successfully!")

        # Refresh progress chart
        self.update_progress_charts()

    def view_summary(self):
        if not any(self.workouts.values()):
            messagebox.showinfo("Summary", "No sessions logged yet!")
            return

        summary_window = tk.Toplevel(self.master)
        summary_window.title("Workout Summary")
        summary_window.geometry("450x400")

        tk.Label(summary_window, text="Session Summary", font=("Helvetica", 14, "bold")).pack(pady=10)

        total_time = 0
        for category, sessions in self.workouts.items():
            tk.Label(summary_window, text=f"{category}:", font=("Arial", 12, "bold"), fg="#007bff").pack(anchor="w", padx=10)
            if sessions:
                for i, entry in enumerate(sessions, 1):
                    tk.Label(summary_window, text=f" {i}. {entry['exercise']} - {entry['duration']} min", font=("Arial", 11)).pack(anchor="w", padx=25)
                    total_time += entry['duration']
            else:
                tk.Label(summary_window, text="  No sessions recorded.", font=("Arial", 11, "italic"), fg="#888").pack(anchor="w", padx=25)

        tk.Label(summary_window, text=f"\nTotal Time Spent: {total_time} minutes", font=("Arial", 12, "bold"), fg="#28a745").pack(pady=10)

    # ------------------ WORKOUT CHART TAB ------------------ #
    def create_workout_chart_tab(self):
        tk.Label(self.chart_tab, text="🏋️ Personalized Workout Chart", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        chart_data = {
            "Warm-up": ["5 min Jog", "Jumping Jacks", "Arm Circles", "Leg Swings", "Dynamic Stretching"],
            "Workout": ["Push-ups", "Squats", "Plank", "Lunges", "Burpees", "Crunches"],
            "Cool-down": ["Slow Walking", "Static Stretching", "Deep Breathing", "Yoga Poses"]
        }

        for category, exercises in chart_data.items():
            tk.Label(self.chart_tab, text=f"{category} Exercises:", font=("Arial", 13, "bold"), bg="white", fg="#007bff").pack(anchor="w", padx=20, pady=5)
            for ex in exercises:
                tk.Label(self.chart_tab, text=f"• {ex}", font=("Arial", 11), bg="white").pack(anchor="w", padx=40)

    # ------------------ DIET CHART TAB ------------------ #
    def create_diet_chart_tab(self):
        tk.Label(self.diet_tab, text="🥗 Best Diet Chart for Fitness Goals", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        diet_plans = {
            "Weight Loss": ["Oatmeal with Fruits", "Grilled Chicken Salad", "Vegetable Soup", "Brown Rice & Veggies"],
            "Muscle Gain": ["Egg Omelet", "Chicken Breast", "Quinoa & Beans", "Protein Shake", "Greek Yogurt with Nuts"],
            "Endurance": ["Banana & Peanut Butter", "Whole Grain Pasta", "Sweet Potatoes", "Salmon & Avocado", "Trail Mix"]
        }

        for goal, foods in diet_plans.items():
            tk.Label(self.diet_tab, text=f"{goal} Plan:", font=("Arial", 13, "bold"), bg="white", fg="#28a745").pack(anchor="w", padx=20, pady=5)
            for food in foods:
                tk.Label(self.diet_tab, text=f"• {food}", font=("Arial", 11), bg="white").pack(anchor="w", padx=40)

    # ------------------ PROGRESS TAB ------------------ #
    def create_progress_tab(self):
        tk.Label(self.progress_tab, text="📈 Personal Progress Tracker", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
        self.progress_canvas = None
        self.update_progress_charts()

    def update_progress_charts(self):
        """Dynamically update progress visualizations."""
        for widget in self.progress_tab.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        totals = {cat: sum(entry['duration'] for entry in sessions) for cat, sessions in self.workouts.items()}

        fig = Figure(figsize=(7, 4), dpi=100)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        categories = list(totals.keys())
        values = list(totals.values())

        # Bar Chart
        ax1.bar(categories, values, color=["#007bff", "#28a745", "#ffc107"])
        ax1.set_title("Time Spent per Category")
        ax1.set_ylabel("Minutes")

        # Pie Chart
        if sum(values) > 0:
            ax2.pie(values, labels=categories, autopct="%1.1f%%", startangle=90, colors=["#007bff", "#28a745", "#ffc107"])
            ax2.set_title("Workout Distribution")

        self.progress_canvas = FigureCanvasTkAgg(fig, master=self.progress_tab)
        self.progress_canvas.draw()
        self.progress_canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
