import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class FitnessTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("ACEestFitness and Gym Tracker")
        master.geometry("500x500")
        master.resizable(False, False)

        # Initialize workout dictionary
        self.workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}

        # Title Section
        tk.Label(master, text="🏋️ ACEest Fitness & Gym Tracker", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Category Selector
        self.category_var = tk.StringVar(value="Workout")
        tk.Label(master, text="Select Category:", font=("Arial", 12)).pack()
        self.category_menu = ttk.Combobox(master, textvariable=self.category_var, values=list(self.workouts.keys()), state="readonly")
        self.category_menu.pack(pady=5)

        # Workout Input Fields
        input_frame = tk.Frame(master)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Exercise:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
        self.workout_entry = tk.Entry(input_frame, width=25)
        self.workout_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Duration (min):", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(input_frame, width=10)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Session", command=self.add_workout, width=20, bg="#28a745", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="View Summary", command=self.view_summary, width=20, bg="#007bff", fg="white").grid(row=0, column=1, padx=5)

        tk.Button(master, text="Exit", command=master.quit, width=15, bg="#dc3545", fg="white").pack(pady=10)

        # Status Bar
        self.status_label = tk.Label(master, text="Welcome! Log your first session.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def add_workout(self):
        """Add a workout entry to the log."""
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

    def view_summary(self):
        """Show a categorized summary of all sessions."""
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

        # Motivational Note
        if total_time < 30:
            msg = "Good start! Keep moving 💪"
        elif total_time < 60:
            msg = "Nice effort! You're building consistency 🔥"
        else:
            msg = "Excellent dedication! Keep up the great work 🏆"
        tk.Label(summary_window, text=msg, font=("Arial", 12, "italic"), fg="#555").pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
