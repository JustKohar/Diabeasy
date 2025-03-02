# main_app.py

import tkinter as tk  # Import tkinter for GUI components
from tkinter import messagebox  # Import messagebox for pop-up messages
from datetime import datetime  # Import datetime for timestamping insulin usage
from data_manager import load_user_data, save_user_data  # Import functions for loading and saving user data


class MainApp:
    def __init__(self, master, username):
        self.master = master  # Store reference to the root window
        self.username = username  # Store the username for the session
        self.master.title(f"Insulin Tracker - {username}")  # Set window title to include username

        # Initialize data with duplicate protection
        self.data = self.clean_duplicates(load_user_data(username))  # Load and clean any duplicate data

        # Create UI components
        self.create_widgets()  # Set up the UI components
        self.update_history()  # Display the user's usage history

    def create_widgets(self):
        """Create the widgets for the main application window"""

        # Create a frame for the insulin calculator section
        calc_frame = tk.LabelFrame(self.master, text="Insulin Calculator")
        calc_frame.pack(padx=10, pady=10, fill="x")

        # Labels for Carbs and Insulin Ratio
        tk.Label(calc_frame, text="Carbs (g):").grid(row=0, column=0)  # Label for carbs input
        tk.Label(calc_frame, text="Insulin Ratio:").grid(row=1, column=0)  # Label for insulin ratio input

        # Entry fields for Carbs and Insulin Ratio
        self.carbs_entry = tk.Entry(calc_frame)  # Entry for carbs input
        self.ratio_entry = tk.Entry(calc_frame)  # Entry for insulin ratio input
        self.carbs_entry.grid(row=0, column=1)  # Position carbs entry field
        self.ratio_entry.grid(row=1, column=1)  # Position ratio entry field

        # Calculate button, which triggers the calculation of insulin dose
        tk.Button(calc_frame, text="Calculate", command=self.calculate).grid(row=2, columnspan=2)

        # Create a frame for displaying usage history
        history_frame = tk.LabelFrame(self.master, text="Usage History")

        # Create a Text widget for displaying the history
        self.history_text = tk.Text(history_frame, height=10)  # Text box to display the history of insulin usage
        scrollbar = tk.Scrollbar(history_frame)  # Scrollbar for the history text box

        # Link scrollbar with the history text widget
        self.history_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)

        # Pack the history frame and its components
        history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Text box will expand to the left
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Scrollbar will be on the right

    def calculate(self):
        """Handle the calculation of the insulin dose"""
        try:
            # Get and validate inputs for carbs and ratio
            carbs = float(self.carbs_entry.get())  # Convert carbs input to a float
            ratio = float(self.ratio_entry.get())  # Convert ratio input to a float

            # Validate that ratio is greater than 0
            if ratio <= 0:
                messagebox.showerror("Error", "Ratio must be greater than 0")  # Error message if ratio is invalid
                return

            # Create a new entry for the calculation result
            new_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp of calculation
                "carbs": carbs,  # Carbs input
                "ratio": ratio,  # Insulin ratio input
                "dose": round(carbs / ratio, 2)  # Calculate insulin dose and round to 2 decimal places
            }

            # Check for duplicates in the session
            if not self.is_duplicate(new_entry):
                self.data.append(new_entry)  # Add the new entry to the data list
                save_user_data(self.username, self.data)  # Save the updated data
                self.update_history()  # Update the history display
                self.clear_inputs()  # Clear the input fields
                messagebox.showinfo("Result",
                                    f"Insulin Dose: {new_entry['dose']} units")  # Display result in a message box
            else:
                messagebox.showwarning("Duplicate", "This entry already exists")  # Warning if the entry is a duplicate

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")  # Error message if inputs are invalid

    def is_duplicate(self, new_entry):
        """Check if the new entry already exists in the current data"""
        return any(
            entry["carbs"] == new_entry["carbs"] and  # Compare carbs
            entry["ratio"] == new_entry["ratio"] and  # Compare ratio
            entry["dose"] == new_entry["dose"]  # Compare insulin dose
            for entry in self.data  # Iterate through the existing entries
        )

    def clean_duplicates(self, data):
        """Remove duplicates from the loaded data"""
        seen = set()  # Create a set to track seen entries
        cleaned = []  # List to store cleaned data
        for entry in data:
            identifier = (entry["carbs"], entry["ratio"], entry["dose"])  # Create a unique identifier for each entry
            if identifier not in seen:  # Check if the identifier has been seen before
                seen.add(identifier)  # Mark this identifier as seen
                cleaned.append(entry)  # Add the entry to the cleaned list
        return cleaned  # Return the cleaned list of data

    def clear_inputs(self):
        """Clear the input fields for carbs and ratio"""
        self.carbs_entry.delete(0, tk.END)  # Clear the carbs entry field
        self.ratio_entry.delete(0, tk.END)  # Clear the ratio entry field

    def update_history(self):
        """Update the history display with the most recent entries"""
        self.history_text.delete(1.0, tk.END)  # Clear the existing history text
        for entry in reversed(self.data):  # Loop through the data in reverse order (most recent first)
            # Insert the formatted entry into the history text box
            self.history_text.insert(tk.END,
                                     f"{entry['timestamp']}\n"
                                     f"Carbs: {entry['carbs']}g | Ratio: 1:{entry['ratio']} | Dose: {entry['dose']}u\n"
                                     f"{'-' * 50}\n"
                                     )
        self.history_text.see(tk.END)  # Scroll to the bottom to show the latest entry
