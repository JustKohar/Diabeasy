import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from profile_manager import InsulinProfile, create_new_profile, generate_scale_ranges
from data_manager import save_user_data, load_user_data
from history import HistoryTab
from main import LoginWindow  # Import the LoginWindow class

class InsulinApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username  # Store the username for personalized app data
        self.title(f"Insulin Calculator - {username}")  # Set window title with username
        self.geometry("1200x800")  # Set the window size
        self.configure(bg="#f5f6fa")  # Set the background color of the window

        # Color scheme for the UI elements
        self.colors = {
            'primary': "#2c3e50",
            'secondary': "#3498db",
            'background': "#f5f6fa",
            'text': "#2c3e50",
            'success': "#27ae60",
            'warning': "#e67e22"
        }

        self.style = ttk.Style()  # Create a style object for widget styling
        self.style.theme_use('clam')  # Use the clam theme for ttk widgets
        self.configure_styles()  # Apply the custom styles

        # Initialize application profile and load data
        self.profile = self.load_profile()  # Load user profile data
        self.create_widgets()  # Create the UI elements
        self.load_history()  # Load the historical data of insulin doses

    def configure_styles(self):
        """Configure custom styles for widgets"""
        # Set default background for all widgets
        self.style.configure(".", background=self.colors['background'])

        # Set style for frames
        self.style.configure("TFrame", background=self.colors['background'])

        # Set style for labels
        self.style.configure("TLabel",
                             background=self.colors['background'],
                             foreground=self.colors['text'],
                             font=("Arial", 10))

        # Style for buttons (including padding and background color)
        self.style.configure("TButton",
                             font=("Arial", 10, "bold"),
                             padding=8,
                             background=self.colors['secondary'],
                             foreground="white",
                             borderwidth=0)
        # Define the appearance of the button when it is active or disabled
        self.style.map("TButton",
                       background=[("active", self.colors['primary']), ("disabled", "#bdc3c7")])

        # Style for entry widgets (input fields)
        self.style.configure("TEntry",
                             fieldbackground="white",
                             foreground=self.colors['text'],
                             padding=5)

        # Header label style
        self.style.configure("Header.TLabel",
                             font=("Arial", 14, "bold"),
                             foreground=self.colors['primary'])

        # Style for result labels (insulin dose result display)
        self.style.configure("Result.TLabel",
                             font=("Arial", 16, "bold"),
                             foreground=self.colors['success'])

        # Style for notebook (tabbed interface)
        self.style.configure("TNotebook", background=self.colors['background'])
        self.style.configure("TNotebook.Tab",
                             font=("Arial", 10, "bold"),
                             padding=(15, 8),
                             background="#dfe6e9",
                             foreground=self.colors['text'])
        # Tab selection colors
        self.style.map("TNotebook.Tab",
                       background=[("selected", self.colors['primary'])],
                       foreground=[("selected", "white")])

    def create_widgets(self):
        """Create the main application widgets (tabs)"""
        # Create a frame for the logout button and pack it to the top right
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Create a logout button
        logout_btn = ttk.Button(top_frame, text="Logout", command=self.logout, style="TButton")
        logout_btn.pack(side=tk.RIGHT)

        # Create a clear history button
        clear_history_btn = ttk.Button(top_frame, text="Clear History", command=self.clear_history, style="TButton")
        clear_history_btn.pack(side=tk.RIGHT, padx=10)

        self.notebook = ttk.Notebook(self)  # Create a notebook widget for tabs

        # Create each of the application tabs
        self.setup_tab = SetupTab(self.notebook, self.profile, self.save_profile)
        self.calc_tab = CalculationTab(self.notebook, self.calculate_dose)
        self.history_tab = HistoryTab(self.notebook)

        # Add tabs to the notebook widget
        self.notebook.add(self.setup_tab, text=" Profile Setup ")
        self.notebook.add(self.calc_tab, text=" Calculator ")
        self.notebook.add(self.history_tab, text=" History ")

        # Display the notebook in the main window
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    def load_profile(self):
        """Load user profile data from storage (or create a new one)"""
        profile_data = load_user_data(self.username, "profile")  # Load profile data
        return InsulinProfile(
            **profile_data) if profile_data else create_new_profile()  # Return profile or create new one

    def save_profile(self, profile):
        """Save the user profile data to storage"""
        save_user_data(self.username, "profile", profile.__dict__)  # Save profile data
        messagebox.showinfo("Success", "Profile saved successfully")  # Notify user of successful save
        self.profile = profile  # Update the current profile in memory

    def calculate_dose(self, blood_sugar, time_str):
        """Calculate insulin dose based on blood sugar and time"""
        try:
            # Determine base dose based on time of day
            calc_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            if 5 <= calc_time.hour < 11:
                base_dose = self.profile.breakfast
            elif 11 <= calc_time.hour < 16:
                base_dose = self.profile.lunch
            else:
                base_dose = self.profile.dinner

            # Calculate additional dose based on sliding scale
            if blood_sugar < self.profile.base_rate:
                additional_dose = 0
            else:
                additional_dose = (blood_sugar - self.profile.base_rate) // self.profile.increase_per

            total_dose = base_dose + additional_dose  # Calculate the total insulin dose

            # Save this calculation to history
            self.save_history_entry(blood_sugar, time_str, total_dose)

            return total_dose  # Return the calculated dose
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")  # Handle any input errors
            return 0

    def save_history_entry(self, blood_sugar, time_str, dose):
        """Save a calculation entry to the history"""
        entry = {
            'date': datetime.date.today().isoformat(),  # Store the current date
            'time': time_str,  # Store the time of calculation
            'blood_sugar': blood_sugar,  # Store the blood sugar value
            'dose': dose  # Store the calculated dose
        }
        history = load_user_data(self.username, "history") or []  # Load existing history or initialize an empty list
        history.insert(0, entry)  # Insert the new entry at the beginning of the list
        save_user_data(self.username, "history", history)  # Save the updated history to storage
        self.history_tab.update_history(history)  # Update the history tab in the UI

    def load_history(self):
        """Load the calculation history and display it"""
        history = load_user_data(self.username, "history") or []  # Load history data
        self.history_tab.update_history(history)  # Update the history tab with the loaded data

    def clear_history(self):
        """Clear the user's history after confirmation"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear your history?"):
            save_user_data(self.username, "history", [])  # Clear the history data
            self.history_tab.update_history([])  # Update the history tab in the UI
            messagebox.showinfo("Success", "History cleared successfully")  # Notify user of successful clear

    def logout(self):
        """Handle the logout logic when the user clicks the logout button"""
        self.destroy()  # Close the current window
        LoginWindow().mainloop()  # Reopen the login window


class SetupTab(ttk.Frame):
    def __init__(self, parent, profile, save_callback):
        super().__init__(parent)
        self.profile = profile  # Store the user profile
        self.save_callback = save_callback  # Store the callback function to save profile data
        self.create_widgets()  # Create the widgets for this tab

    def create_widgets(self):
        """Create the profile setup form widgets"""
        header = ttk.Frame(self)  # Create a header frame
        header.pack(pady=20, fill=tk.X)
        ttk.Label(header, text="Profile Configuration", style="Header.TLabel").pack()  # Display the header text

        # Form container for profile input fields
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=50, pady=20)

        # Define the fields for the profile setup
        fields = [
            ("Breakfast Insulin (units):", 'breakfast'),
            ("Lunch Insulin (units):", 'lunch'),
            ("Dinner Insulin (units):", 'dinner'),
            ("Base Rate (mg/dL):", 'base_rate'),
            ("Scale Increment (mg/dL):", 'increase_per')
        ]

        self.entries = {}  # Dictionary to store references to the input fields
        for row, (label, field) in enumerate(fields):
            frame = ttk.Frame(form_frame)  # Create a frame for each field
            frame.grid(row=row, column=0, pady=8, sticky=tk.W)

            # Label for the field
            ttk.Label(frame, text=label, width=25, anchor=tk.W).pack(side=tk.LEFT)
            # Input field for the value
            entry = ttk.Entry(frame, width=15)
            entry.insert(0, str(getattr(self.profile, field)))  # Set the initial value from the profile
            entry.pack(side=tk.LEFT)
            self.entries[field] = entry  # Store reference to the entry field

        # Save button to save profile data
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="Save Profile",
                   command=self.save_profile, width=20).pack()

    def save_profile(self):
        """Save profile data after user input"""
        try:
            # Create a new InsulinProfile object from the user input
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
            self.save_callback(new_profile)  # Call the callback to save the profile
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")  # Handle invalid inputs


class CalculationTab(ttk.Frame):
    def __init__(self, parent, calculate_callback):
        super().__init__(parent)
        self.calculate_callback = calculate_callback  # Store the callback function for dose calculation
        self.create_widgets()  # Create the widgets for the calculation tab

    def create_widgets(self):
        """Create the dose calculator interface widgets"""
        # Header for the dose calculator
        header = ttk.Frame(self)
        header.pack(pady=20, fill=tk.X)
        ttk.Label(header, text="Dose Calculator", style="Header.TLabel").pack()

        # Input container for blood sugar and time
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=30)

        # Blood sugar input field
        ttk.Label(input_frame, text="Current Blood Sugar (mg/dL):").grid(row=0, column=0, padx=15, pady=10, sticky=tk.E)
        self.blood_sugar_entry = ttk.Entry(input_frame, width=10)
        self.blood_sugar_entry.grid(row=0, column=1, padx=15, pady=10)

        # Time input field
        ttk.Label(input_frame, text="Time (HH:MM):").grid(row=1, column=0, padx=15, pady=10, sticky=tk.E)
        self.time_entry = ttk.Entry(input_frame, width=10)
        self.time_entry.insert(0, self.get_default_time())  # Set default time to current rounded to nearest 30 minutes
        self.time_entry.grid(row=1, column=1, padx=15, pady=10)

        # Result display area for calculated dose
        result_frame = ttk.Frame(self)
        result_frame.pack(pady=30)
        self.result_label = ttk.Label(result_frame, text="", style="Result.TLabel")
        self.result_label.pack()

        # Calculate button to trigger dose calculation
        ttk.Button(self, text="Calculate Dose",
                   command=self.calculate, width=20).pack(pady=20)

    def get_default_time(self):
        """Get default time rounded to nearest 30 minutes"""
        now = datetime.datetime.now()
        if now.minute >= 30:
            return f"{now.hour}:30"
        return f"{now.hour}:00"

    def calculate(self):
        """Handle the calculation process when the button is clicked"""
        try:
            # Call the callback to calculate the dose using the input blood sugar and time
            dose = self.calculate_callback(
                int(self.blood_sugar_entry.get()),
                self.time_entry.get()
            )
            self.result_label.config(text=f"Recommended Dose: {dose} units")  # Display the result
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")  # Handle invalid input cases