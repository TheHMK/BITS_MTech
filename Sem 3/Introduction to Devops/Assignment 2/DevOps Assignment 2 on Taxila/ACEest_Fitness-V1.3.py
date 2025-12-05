import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import io
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors as rl_colors
from reportlab.lib.utils import ImageReader

# ---------- Color Palette ----------
COLOR_PRIMARY = "#4CAF50"   # Green
COLOR_SECONDARY = "#2196F3" # Blue
COLOR_BACKGROUND = "#F8F9FA"
COLOR_CARD_BG = "#FFFFFF"
COLOR_TEXT = "#343A40"

# ---------- MET Values for Exercises ----------
MET_VALUES = {
    "Warm-up": 3,
    "Workout": 6,
    "Cool-down": 2.5
}
        
class FitnessTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("ACEest Fitness & Gym Tracker")
        master.geometry("850x700")
        master.config(bg=COLOR_BACKGROUND)

        # --- User Info ---
        self.user_info = {}  # Will hold name, regn-id, height, weight, age, gender, BMI, BMR

        # --- Workouts ---
        self.workouts = {"Warm-up": [], "Workout": [], "Cool-down": []}
        self.daily_workouts = {}  # key=date_iso, value={category:[entries]}
        
        # --- UI Setup ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background=COLOR_BACKGROUND, borderwidth=0)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"), foreground=COLOR_TEXT, padding=[15, 8], background=COLOR_BACKGROUND)
        self.style.map("TNotebook.Tab", background=[("selected", COLOR_CARD_BG)], foreground=[("selected", COLOR_PRIMARY)])
        self.style.configure("Primary.TButton", font=("Arial", 11, "bold"), background=COLOR_PRIMARY, foreground=COLOR_CARD_BG, padding=10)
        self.style.map("Primary.TButton", background=[('active', '#388E3C')])
        self.style.configure("Secondary.TButton", font=("Arial", 11, "bold"), background=COLOR_SECONDARY, foreground=COLOR_CARD_BG, padding=10)
        self.style.map("Secondary.TButton", background=[('active', '#1976D2')])

        # --- Notebook Tabs ---
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        self.log_tab = tk.Frame(self.notebook, bg=COLOR_BACKGROUND)
        self.chart_tab = tk.Frame(self.notebook, bg=COLOR_BACKGROUND)
        self.diet_tab = tk.Frame(self.notebook, bg=COLOR_BACKGROUND)
        self.progress_tab = tk.Frame(self.notebook, bg=COLOR_CARD_BG)

        self.notebook.add(self.log_tab, text="🏋️ Log Workouts")
        self.notebook.add(self.chart_tab, text="💡 Workout Plan")
        self.notebook.add(self.diet_tab, text="🥗 Diet Guide")
        self.notebook.add(self.progress_tab, text="📈 Progress Tracker")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # --- Initialize Tabs ---
        self.create_user_info_section()
        self.create_log_tab()
        self.create_workout_plan_tab()
        self.create_diet_guide_tab()
        self.create_progress_tab()
    # ADD THESE if not already present
    def create_workout_plan_tab(self):
        tk.Label(self.chart_tab, text="Workout Plan coming soon.", bg=COLOR_BACKGROUND).pack(pady=100)

    def create_diet_guide_tab(self):
        tk.Label(self.diet_tab, text="Diet Guide coming soon.", bg=COLOR_BACKGROUND).pack(pady=100)

    # ---------------- Utility ----------------
    def on_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text").strip()
        if "Progress Tracker" in selected_tab:
            self.update_progress_charts()

    # ---------- User Info ----------
    def create_user_info_section(self):
        info_frame = tk.Frame(self.master, bg=COLOR_CARD_BG, padx=20, pady=15, relief=tk.RIDGE, bd=2)
        info_frame.place(x=20, y=20, width=300, height=300)
        tk.Label(info_frame, text="📝 User Info", font=("Inter", 14, "bold"), bg=COLOR_CARD_BG).pack(pady=5)
        # Name
        tk.Label(info_frame, text="Name:", bg=COLOR_CARD_BG).pack(anchor='w'); self.name_entry = tk.Entry(info_frame)
        self.name_entry.pack(fill="x")
        # Regn-ID
        tk.Label(info_frame, text="Regn-ID:", bg=COLOR_CARD_BG).pack(anchor='w'); self.regn_entry = tk.Entry(info_frame)
        self.regn_entry.pack(fill="x")
        # Age
        tk.Label(info_frame, text="Age:", bg=COLOR_CARD_BG).pack(anchor='w'); self.age_entry = tk.Entry(info_frame)
        self.age_entry.pack(fill="x")
        # Gender
        tk.Label(info_frame, text="Gender (M/F):", bg=COLOR_CARD_BG).pack(anchor='w'); self.gender_entry = tk.Entry(info_frame)
        self.gender_entry.pack(fill="x")
        # Height
        tk.Label(info_frame, text="Height (cm):", bg=COLOR_CARD_BG).pack(anchor='w'); self.height_entry = tk.Entry(info_frame)
        self.height_entry.pack(fill="x")
        # Weight
        tk.Label(info_frame, text="Weight (kg):", bg=COLOR_CARD_BG).pack(anchor='w'); self.weight_entry = tk.Entry(info_frame)
        self.weight_entry.pack(fill="x")

        ttk.Button(info_frame, text="Save Info", command=self.save_user_info, style="Primary.TButton").pack(pady=10)

    def save_user_info(self):
        try:
            name = self.name_entry.get().strip()
            regn_id = self.regn_entry.get().strip()
            age = int(self.age_entry.get().strip())
            gender = self.gender_entry.get().strip().upper()
            height_cm = float(self.height_entry.get().strip())
            weight_kg = float(self.weight_entry.get().strip())
            bmi = weight_kg / ((height_cm/100)**2)
            if gender == "M":
                bmr = 10*weight_kg + 6.25*height_cm - 5*age + 5
            else:
                bmr = 10*weight_kg + 6.25*height_cm - 5*age - 161
            self.user_info = {
                "name": name, "regn_id": regn_id, "age": age, "gender": gender,
                "height": height_cm, "weight": weight_kg, "bmi": bmi, "bmr": bmr,
                "weekly_cal_goal": 2000
            }
            messagebox.showinfo("Success", f"User info saved! BMI={bmi:.1f}, BMR={bmr:.0f} kcal/day")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    # ---------- Log Workouts ----------
    def create_log_tab(self):
        tk.Label(self.log_tab, text="ACEest Session Logger", font=("Inter", 20, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_TEXT).pack(pady=(20, 10))
        tk.Label(self.log_tab, text="Track your progress with precision.", font=("Inter", 12), bg=COLOR_BACKGROUND, fg="#6C757D").pack(pady=(0, 20))
        log_card = tk.Frame(self.log_tab, bg=COLOR_CARD_BG, padx=40, pady=30, relief=tk.RAISED, bd=0, highlightbackground="#E9ECEF", highlightthickness=1)
        log_card.pack(pady=10, padx=100, fill="x")
        # Category
        self.category_var = tk.StringVar(value="Workout")
        tk.Label(log_card, text="Category:", font=("Inter", 12, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.category_menu = ttk.Combobox(log_card, textvariable=self.category_var, values=list(self.workouts.keys()), state="readonly", width=30, font=("Inter", 11))
        self.category_menu.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        # Exercise
        tk.Label(log_card, text="Exercise Name:", font=("Inter", 12, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.workout_entry = tk.Entry(log_card, width=30, font=("Inter", 11), bd=1, relief=tk.FLAT, highlightcolor=COLOR_PRIMARY, highlightthickness=1)
        self.workout_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        # Duration
        tk.Label(log_card, text="Duration (min):", font=("Inter", 12, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.duration_entry = tk.Entry(log_card, width=15, font=("Inter", 11), bd=1, relief=tk.FLAT, highlightcolor=COLOR_PRIMARY, highlightthickness=1)
        self.duration_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        # Buttons
        button_frame = tk.Frame(self.log_tab, bg=COLOR_BACKGROUND)
        button_frame.pack(pady=30)
        ttk.Button(button_frame, text="✅ ADD SESSION", command=self.add_workout, style="Primary.TButton", width=18).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="📋 VIEW SUMMARY", command=self.view_summary, style="Secondary.TButton", width=18).grid(row=0, column=1, padx=15)
        self.status_label = tk.Label(self.log_tab, text="Welcome! Ready for a great session.", bd=1, relief=tk.FLAT, anchor=tk.W, bg=COLOR_CARD_BG, fg="#6C757D", font=("Inter", 10))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def add_workout(self):
        category = self.category_var.get()
        workout = self.workout_entry.get().strip()
        duration_str = self.duration_entry.get().strip()
        if not workout or not duration_str:
            messagebox.showerror("Input Error", "Please enter both exercise and duration."); return
        try:
            duration = int(duration_str)
            if duration <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Duration must be a positive whole number."); return
        # Calories calculation
        weight = self.user_info.get("weight", 70)
        met = MET_VALUES.get(category, 5)
        calories = (met * 3.5 * weight / 200) * duration
        entry = {"exercise": workout, "duration": duration, "calories": calories, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.workouts[category].append(entry)
        today_iso = date.today().isoformat()
        if today_iso not in self.daily_workouts:
            self.daily_workouts[today_iso] = {"Warm-up": [], "Workout": [], "Cool-down": []}
        self.daily_workouts[today_iso][category].append(entry)
        self.workout_entry.delete(0, tk.END); self.duration_entry.delete(0, tk.END)
        self.status_label.config(text=f"Added {workout} ({duration} min) to {category}! 💪")
        self.update_progress_charts()
        messagebox.showinfo("Success", f"{workout} added successfully!")

    def view_summary(self):
        if not any(self.workouts.values()):
            messagebox.showinfo("Summary", "No sessions logged yet!"); return
        summary_window = tk.Toplevel(self.master); summary_window.title("Detailed Workout Summary"); summary_window.geometry("550x550"); summary_window.config(bg=COLOR_CARD_BG)
        tk.Label(summary_window, text="🏋️ Full Session History", font=("Inter", 16, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).pack(pady=10)
        text_frame = tk.Frame(summary_window, bg=COLOR_CARD_BG); text_frame.pack(pady=10, padx=20, fill="both", expand=True)
        scrollbar = ttk.Scrollbar(text_frame); scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        summary_text = tk.Text(text_frame, height=20, width=55, wrap=tk.WORD, font=("Inter", 10), bg=COLOR_BACKGROUND, fg=COLOR_TEXT, yscrollcommand=scrollbar.set, relief=tk.FLAT); summary_text.pack(fill="both", expand=True)
        scrollbar.config(command=summary_text.yview)
        total_time = 0
        for category, sessions in self.workouts.items():
            summary_text.insert(tk.END, f"--- {category.upper()} ---\n", category.lower())
            summary_text.tag_config(category.lower(), font=("Inter", 12, "bold"), foreground=COLOR_SECONDARY if category=="Warm-up" else COLOR_PRIMARY if category=="Workout" else "#FFC107")
            if sessions:
                for i, entry in enumerate(sessions, 1):
                    line = f"  {i}. {entry['exercise']} - {entry['duration']} min | {entry['calories']:.1f} kcal | Date: {entry['timestamp'].split(' ')[0]}\n"
                    summary_text.insert(tk.END, line)
                    total_time += entry['duration']
            else:
                summary_text.insert(tk.END, "  No sessions recorded.\n", "italic"); summary_text.tag_config("italic", font=("Inter", 10, "italic"), foreground="#888")
            summary_text.insert(tk.END, "\n")
        summary_text.insert(tk.END, f"--- LIFETIME TOTALS ---\n", "total_header"); summary_text.tag_config("total_header", font=("Inter", 13, "bold"), foreground="#DC3545")
        summary_text.insert(tk.END, f"  Total Training Time: {total_time} minutes\n", "total_value"); summary_text.tag_config("total_value", font=("Inter", 12, "bold"), foreground="#DC3545")
        summary_text.config(state=tk.DISABLED)

    # ---------- Progress Charts ----------
    def create_progress_tab(self):
        tk.Label(self.progress_tab, text="📈 Personal Progress Tracker", font=("Inter", 20, "bold"), bg=COLOR_CARD_BG, fg=COLOR_TEXT).pack(pady=(20, 10))
        tk.Label(self.progress_tab, text="Visualization of your logged workout time distribution.", font=("Inter", 12), bg=COLOR_CARD_BG, fg="#6C757D").pack(pady=(0, 20))
        self.chart_container = tk.Frame(self.progress_tab, bg=COLOR_CARD_BG); self.chart_container.pack(pady=10, fill="both", expand=True)
        self.chart_canvas = None

    def update_progress_charts(self):
        for widget in self.chart_container.winfo_children(): widget.destroy()
        totals = {cat: sum(entry['duration'] for entry in sessions) for cat, sessions in self.workouts.items()}
        categories = list(totals.keys()); values = list(totals.values())
        if sum(values) == 0:
            tk.Label(self.chart_container, text="No workout data logged yet.", font=("Inter", 14, "italic"), fg="#888", bg=COLOR_CARD_BG).pack(pady=100); return
        fig = Figure(figsize=(8,5), dpi=100, facecolor=COLOR_CARD_BG)
        chart_colors = [COLOR_SECONDARY, COLOR_PRIMARY, "#FFC107"]
        ax1 = fig.add_subplot(121)
        ax1.bar(categories, values, color=chart_colors)
        ax1.set_title("Total Minutes per Category", fontsize=10, color=COLOR_TEXT)
        ax1.set_ylabel("Total Minutes", fontsize=8, color=COLOR_TEXT)
        ax1.tick_params(axis='x', labelsize=8, colors=COLOR_TEXT)
        ax1.tick_params(axis='y', labelsize=8, colors=COLOR_TEXT)
        ax1.spines['right'].set_visible(False); ax1.spines['top'].set_visible(False)
        ax1.grid(axis='y', linestyle='-', alpha=0.3); ax1.set_facecolor(COLOR_CARD_BG)
        ax2 = fig.add_subplot(122)
        pie_labels = [c for c, v in zip(categories, values) if v>0]; pie_values = [v for v in values if v>0]
        pie_colors = [chart_colors[i] for i, v in enumerate(values) if v>0]
        ax2.pie(pie_values, labels=pie_labels, autopct="%1.1f%%", startangle=90, colors=pie_colors, wedgeprops={"edgecolor":"white",'linewidth':1}, textprops={'fontsize':8,'color':COLOR_TEXT})
        ax2.set_title("Workout Distribution (%)", fontsize=10, color=COLOR_TEXT); ax2.axis('equal'); ax2.set_facecolor(COLOR_CARD_BG)
        fig.tight_layout(pad=2.0)
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.chart_canvas.draw(); self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)
        total_minutes = sum(values)
        tk.Label(self.progress_tab, text=f"LIFETIME TOTAL: {total_minutes} minutes logged", font=("Inter", 13, "bold"), bg=COLOR_CARD_BG, fg="#DC3545").pack(pady=(10,5))
    
    # ---------- PDF Report ----------
    def export_weekly_report(self):
        if not self.user_info:
            messagebox.showerror("Error", "Please save user info first!"); return
        filename = f"{self.user_info['name'].replace(' ','_')}_weekly_report.pdf"
        c = pdf_canvas.Canvas(filename, pagesize=A4); width, height = A4
        c.setFont("Helvetica-Bold", 16); c.drawString(50, height-50, f"Weekly Fitness Report - {self.user_info['name']}")
        # User Info
        c.setFont("Helvetica", 11)
        c.drawString(50, height-80, f"Regn-ID: {self.user_info['regn_id']} | Age: {self.user_info['age']} | Gender: {self.user_info['gender']}")
        c.drawString(50, height-100, f"Height: {self.user_info['height']} cm | Weight: {self.user_info['weight']} kg | BMI: {self.user_info['bmi']:.1f} | BMR: {self.user_info['bmr']:.0f} kcal/day")
        # Table of workouts
        y = height-140
        table_data = [["Category","Exercise","Duration(min)","Calories(kcal)","Date"]]
        for cat, sessions in self.workouts.items():
            for e in sessions:
                table_data.append([cat,e['exercise'],str(e['duration']),f"{e['calories']:.1f}", e['timestamp'].split()[0]])
        table = Table(table_data, colWidths=[80,150,80,80,80])
        table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),rl_colors.lightblue),("GRID",(0,0),(-1,-1),0.5,rl_colors.black)]))
        table.wrapOn(c, width-100, y); table.drawOn(c,50,y-20)
        c.save()
        messagebox.showinfo("PDF Export", f"Weekly report exported successfully as {filename}")

# ---------- Main ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    # Button placed inside main window for exporting weekly report
    export_btn = ttk.Button(root, text="📄 Export Weekly PDF Report", command=app.export_weekly_report, style="Secondary.TButton")
    export_btn.place(x=20, y=350)
    root.mainloop()
