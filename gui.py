import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from profile_manager import InsulinProfile, create_new_profile, generate_scale_ranges
from data_manager import save_user_data, load_user_data
from history import HistoryTab

class InsulinApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"Insulin Calculator - {username}")
        self.geometry("1200x800")
        self.configure(bg="#f5f6fa")
        
        # Color scheme and styling
        self.colors = {
            'primary': "#2c3e50",
            'secondary': "#3498db",
            'background': "#f5f6fa",
            'text': "#2c3e50",
            'success': "#27ae60",
            'warning': "#e67e22"
        }
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Initialize application
        self.profile = self.load_profile()
        self.create_widgets()
        self.load_history()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        self.style.configure(".", background=self.colors['background'])
        self.style.configure("TFrame", background=self.colors['background'])
        self.style.configure("TLabel", 
                           background=self.colors['background'],
                           foreground=self.colors['text'],
                           font=("Arial", 10))
        
        self.style.configure("TButton",
                           font=("Arial", 10, "bold"),
                           padding=8,
                           background=self.colors['secondary'],
                           foreground="white",
                           borderwidth=0)
        self.style.map("TButton",
                     background=[("active", self.colors['primary']), ("disabled", "#bdc3c7")])
        
        self.style.configure("TEntry",
                           fieldbackground="white",
                           foreground=self.colors['text'],
                           padding=5)
        
        self.style.configure("Header.TLabel",
                           font=("Arial", 14, "bold"),
                           foreground=self.colors['primary'])
        
        self.style.configure("Result.TLabel",
                           font=("Arial", 16, "bold"),
                           foreground=self.colors['success'])
        
        self.style.configure("TNotebook", background=self.colors['background'])
        self.style.configure("TNotebook.Tab",
                           font=("Arial", 10, "bold"),
                           padding=(15, 8),
                           background="#dfe6e9",
                           foreground=self.colors['text'])
        self.style.map("TNotebook.Tab",
                     background=[("selected", self.colors['primary'])],
                     foreground=[("selected", "white")])

    def create_widgets(self):
        """Create main application widgets"""
        self.notebook = ttk.Notebook(self)
        
        # Create tabs
        self.setup_tab = SetupTab(self.notebook, self.profile, self.save_profile)
        self.calc_tab = CalculationTab(self.notebook, self.calculate_dose)
        self.history_tab = HistoryTab(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.setup_tab, text=" Profile Setup ")
        self.notebook.add(self.calc_tab, text=" Calculator ")
        self.notebook.add(self.history_tab, text=" History ")
        
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def load_profile(self):
        """Load user profile from storage"""
        profile_data = load_user_data(self.username, "profile")
        return InsulinProfile(**profile_data) if profile_data else create_new_profile()

    def save_profile(self, profile):
        """Save user profile to storage"""
        save_user_data(self.username, "profile", profile.__dict__)
        messagebox.showinfo("Success", "Profile saved successfully")
        self.profile = profile

    def calculate_dose(self, blood_sugar, time_str):
        """Calculate insulin dose based on inputs"""
        try:
            # Calculate base dose
            calc_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            if 5 <= calc_time.hour < 11:
                base_dose = self.profile.breakfast
            elif 11 <= calc_time.hour < 16:
                base_dose = self.profile.lunch
            else:
                base_dose = self.profile.dinner

            # Calculate additional dose from sliding scale
            additional_dose = 0
            for scale in self.profile.scale_ranges:
                if scale['low'] <= blood_sugar < scale['high']:
                    additional_dose = scale['dose']
                    break

            total_dose = base_dose + additional_dose

            # Save to history
            self.save_history_entry(blood_sugar, time_str, total_dose)
            
            return total_dose
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
            return 0

    def save_history_entry(self, blood_sugar, time_str, dose):
        """Save calculation to history"""
        entry = {
            'date': datetime.date.today().isoformat(),
            'time': time_str,
            'blood_sugar': blood_sugar,
            'dose': dose
        }
        history = load_user_data(self.username, "history") or []
        history.insert(0, entry)
        save_user_data(self.username, "history", history)
        self.history_tab.update_history(history)

    def load_history(self):
        """Load calculation history"""
        history = load_user_data(self.username, "history") or []
        self.history_tab.update_history(history)

class SetupTab(ttk.Frame):
    def __init__(self, parent, profile, save_callback):
        super().__init__(parent)
        self.profile = profile
        self.save_callback = save_callback
        self.create_widgets()

    def create_widgets(self):
        """Create profile setup form"""
        # Header
        header = ttk.Frame(self)
        header.pack(pady=20, fill=tk.X)
        ttk.Label(header, text="Profile Configuration", style="Header.TLabel").pack()
        
        # Form container
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=50, pady=20)
        
        # Form fields
        fields = [
            ("Breakfast Insulin (units):", 'breakfast'),
            ("Lunch Insulin (units):", 'lunch'),
            ("Dinner Insulin (units):", 'dinner'),
            ("Base Rate (mg/dL):", 'base_rate'),
            ("Scale Increment (mg/dL):", 'increase_per')
        ]
        
        self.entries = {}
        for row, (label, field) in enumerate(fields):
            frame = ttk.Frame(form_frame)
            frame.grid(row=row, column=0, pady=8, sticky=tk.W)
            
            ttk.Label(frame, text=label, width=25, anchor=tk.W).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=15)
            entry.insert(0, str(getattr(self.profile, field)))
            entry.pack(side=tk.LEFT)
            self.entries[field] = entry
        
        # Save button
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="Save Profile", 
                 command=self.save_profile, width=20).pack()

    def save_profile(self):
        """Save profile data"""
        try:
            new_profile = InsulinProfile(
                breakfast=int(self.entries['breakfast'].get()),
                lunch=int(self.entries['lunch'].get()),
                dinner=int(self.entries['dinner'].get()),
                base_rate=int(self.entries['base_rate'].get()),
                increase_per=int(self.entries['increase_per'].get()),
                scale_ranges=generate_scale_ranges(
                    int(self.entries['base_rate'].get()),
                    int(self.entries['increase_per'].get())
                )
            )
            self.save_callback(new_profile)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

class CalculationTab(ttk.Frame):
    def __init__(self, parent, calculate_callback):
        super().__init__(parent)
        self.calculate_callback = calculate_callback
        self.create_widgets()

    def create_widgets(self):
        """Create calculator interface"""
        # Header
        header = ttk.Frame(self)
        header.pack(pady=20, fill=tk.X)
        ttk.Label(header, text="Dose Calculator", style="Header.TLabel").pack()
        
        # Input container
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=30)
        
        # Blood sugar input
        ttk.Label(input_frame, text="Current Blood Sugar (mg/dL):").grid(row=0, column=0, padx=15, pady=10, sticky=tk.E)
        self.blood_sugar_entry = ttk.Entry(input_frame, width=10)
        self.blood_sugar_entry.grid(row=0, column=1, padx=15, pady=10)
        
        # Time input
        ttk.Label(input_frame, text="Time (HH:MM):").grid(row=1, column=0, padx=15, pady=10, sticky=tk.E)
        self.time_entry = ttk.Entry(input_frame, width=10)
        self.time_entry.insert(0, self.get_default_time())
        self.time_entry.grid(row=1, column=1, padx=15, pady=10)
        
        # Result display
        result_frame = ttk.Frame(self)
        result_frame.pack(pady=30)
        self.result_label = ttk.Label(result_frame, text="", style="Result.TLabel")
        self.result_label.pack()
        
        # Calculate button
        ttk.Button(self, text="Calculate Dose", 
                 command=self.calculate, width=20).pack(pady=20)

    def get_default_time(self):
        """Get default time rounded to nearest 30 minutes"""
        now = datetime.datetime.now()
        if now.minute >= 30:
            return f"{now.hour}:30"
        return f"{now.hour}:00"

    def calculate(self):
        """Handle calculation request"""
        try:
            dose = self.calculate_callback(
                int(self.blood_sugar_entry.get()),
                self.time_entry.get()
            )
            self.result_label.config(text=f"Recommended Dose: {dose} units")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")