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
        self.geometry("1000x800")
        self.profile = self.load_profile()
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        
        self.setup_tab = SetupTab(self.notebook, self.profile, self.save_profile)
        self.calc_tab = CalculationTab(self.notebook, self.calculate_dose)
        self.history_tab = HistoryTab(self.notebook)
        
        self.notebook.add(self.setup_tab, text="Profile Setup")
        self.notebook.add(self.calc_tab, text="Calculator")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.pack(expand=True, fill=tk.BOTH)

    def load_profile(self):
        profile_data = load_user_data(self.username, "profile")
        return InsulinProfile(**profile_data) if profile_data else create_new_profile()

    def save_profile(self, profile):
        save_user_data(self.username, "profile", profile.__dict__)
        messagebox.showinfo("Success", "Profile saved successfully")
        self.profile = profile

    def calculate_dose(self, blood_sugar, time_str):
        try:
            calc_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            base_dose = self.get_base_dose(calc_time)
            additional_dose = self.get_additional_dose(blood_sugar)
            total_dose = base_dose + additional_dose
            self.save_history(blood_sugar, time_str, total_dose)
            return total_dose
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
            return 0

    def get_base_dose(self, time):
        if 5 <= time.hour < 11: return self.profile.breakfast
        elif 11 <= time.hour < 16: return self.profile.lunch
        else: return self.profile.dinner

    def get_additional_dose(self, blood_sugar):
        for scale in self.profile.scale_ranges:
            if scale['low'] <= blood_sugar < scale['high']:
                return scale['dose']
        return 0

    def save_history(self, blood_sugar, time_str, dose):
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
        history = load_user_data(self.username, "history") or []
        self.history_tab.update_history(history)

class SetupTab(ttk.Frame):
    def __init__(self, parent, profile, save_callback):
        super().__init__(parent)
        self.profile = profile
        self.save_callback = save_callback
        self.create_widgets()

    def create_widgets(self):
        fields = [
            ("Breakfast Insulin:", 'breakfast'),
            ("Lunch Insulin:", 'lunch'),
            ("Dinner Insulin:", 'dinner'),
            ("Base Rate:", 'base_rate'),
            ("Increase Per:", 'increase_per')
        ]
        
        self.entries = {}
        for row, (label, field) in enumerate(fields):
            ttk.Label(self, text=label).grid(row=row, column=0, padx=5, pady=5)
            entry = ttk.Entry(self)
            entry.insert(0, str(getattr(self.profile, field)))
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries[field] = entry
            
        ttk.Button(self, text="Save Profile", command=self.save_profile).grid(row=5, columnspan=2, pady=10)

    def save_profile(self):
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
        now = datetime.datetime.now()
        default_time = f"{now.hour}:{30 if now.minute >= 30 else 00}"
        
        ttk.Label(self, text="Blood Sugar (mg/dL):").grid(row=0, column=0, padx=5, pady=5)
        self.blood_sugar_entry = ttk.Entry(self)
        self.blood_sugar_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Time (HH:MM):").grid(row=1, column=0, padx=5, pady=5)
        self.time_entry = ttk.Entry(self)
        self.time_entry.insert(0, default_time)
        self.time_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.result_label = ttk.Label(self, text="Recommended Dose: ")
        self.result_label.grid(row=2, columnspan=2, pady=10)
        
        ttk.Button(self, text="Calculate", command=self.calculate).grid(row=3, columnspan=2, pady=5)

    def calculate(self):
        try:
            dose = self.calculate_callback(
                int(self.blood_sugar_entry.get()),
                self.time_entry.get()
            )
            self.result_label.config(text=f"Recommended Dose: {dose} units")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")