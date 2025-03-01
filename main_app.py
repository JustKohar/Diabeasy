# main_app.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from data_manager import load_user_data, save_user_data

class MainApp:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.master.title(f"Insulin Tracker - {username}")
        
        # Initialize data with duplicate protection
        self.data = self.clean_duplicates(load_user_data(username))
        
        # Create UI components
        self.create_widgets()
        self.update_history()

    def create_widgets(self):
        # Calculator Frame
        calc_frame = tk.LabelFrame(self.master, text="Insulin Calculator")
        calc_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(calc_frame, text="Carbs (g):").grid(row=0, column=0)
        tk.Label(calc_frame, text="Insulin Ratio:").grid(row=1, column=0)
        
        self.carbs_entry = tk.Entry(calc_frame)
        self.ratio_entry = tk.Entry(calc_frame)
        self.carbs_entry.grid(row=0, column=1)
        self.ratio_entry.grid(row=1, column=1)
        
        tk.Button(calc_frame, text="Calculate", command=self.calculate).grid(row=2, columnspan=2)

        # History Frame with Scrollbar
        history_frame = tk.LabelFrame(self.master, text="Usage History")
        self.history_text = tk.Text(history_frame, height=10)
        scrollbar = tk.Scrollbar(history_frame)
        
        self.history_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
        history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def calculate(self):
        try:
            # Get and validate inputs
            carbs = float(self.carbs_entry.get())
            ratio = float(self.ratio_entry.get())
            
            if ratio <= 0:
                messagebox.showerror("Error", "Ratio must be greater than 0")
                return

            # Create new entry
            new_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "carbs": carbs,
                "ratio": ratio,
                "dose": round(carbs / ratio, 2)
            }

            # Check for duplicates
            if not self.is_duplicate(new_entry):
                self.data.append(new_entry)
                save_user_data(self.username, self.data)
                self.update_history()
                self.clear_inputs()
                messagebox.showinfo("Result", f"Insulin Dose: {new_entry['dose']} units")
            else:
                messagebox.showwarning("Duplicate", "This entry already exists")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def is_duplicate(self, new_entry):
        """Check if entry already exists in current session"""
        return any(
            entry["carbs"] == new_entry["carbs"] and
            entry["ratio"] == new_entry["ratio"] and
            entry["dose"] == new_entry["dose"]
            for entry in self.data
        )

    def clean_duplicates(self, data):
        """Remove duplicates from loaded data"""
        seen = set()
        cleaned = []
        for entry in data:
            identifier = (entry["carbs"], entry["ratio"], entry["dose"])
            if identifier not in seen:
                seen.add(identifier)
                cleaned.append(entry)
        return cleaned

    def clear_inputs(self):
        self.carbs_entry.delete(0, tk.END)
        self.ratio_entry.delete(0, tk.END)

    def update_history(self):
        self.history_text.delete(1.0, tk.END)
        for entry in reversed(self.data):
            self.history_text.insert(tk.END,
                f"{entry['timestamp']}\n"
                f"Carbs: {entry['carbs']}g | Ratio: 1:{entry['ratio']} | Dose: {entry['dose']}u\n"
                f"{'-' * 50}\n"
            )
        self.history_text.see(tk.END)