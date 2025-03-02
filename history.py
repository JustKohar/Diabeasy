# Import Tkinter modules for GUI creation
import tkinter as tk
from tkinter import ttk  # Themed Tkinter widgets


class HistoryTab(ttk.Frame):
    """Frame container for displaying insulin history in a tabular format"""

    def __init__(self, parent):
        """Initialize the history tab frame
        Args:
            parent: Parent widget container
        """
        super().__init__(parent)
        self.create_widgets()  # Setup UI components

    def create_widgets(self):
        """Create and arrange visual elements in the frame"""

        # Create Treeview widget with 4 columns
        self.tree = ttk.Treeview(self,
                                 columns=('Date', 'Time', 'Blood Sugar', 'Dose'),
                                 show='headings')  # Hide default first column

        # Configure column headers
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Blood Sugar', text='Blood Sugar (mg/dL)')  # Medical unit label
        self.tree.heading('Dose', text='Dose (units)')  # Insulin units label

        # Create vertical scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self,
                                  orient=tk.VERTICAL,
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)  # Link scrollbar to treeview

        # Grid layout configuration
        self.tree.grid(row=0, column=0, sticky='nsew')  # Expand to fill space
        scrollbar.grid(row=0, column=1, sticky='ns')  # Vertical stretch only

        # Configure grid resizing behavior
        self.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        self.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion

    def update_history(self, history_data):
        """Update the displayed history with new data
        Args:
            history_data: List of dictionaries containing history entries
        """

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new entries with fallback values
        for entry in history_data:
            self.tree.insert('',  # Insert at root level
                             'end',  # Add as last item
                             values=(
                                 entry.get('date', 'N/A'),  # Fallback to 'N/A'
                                 entry.get('time', 'N/A'),
                                 entry.get('blood_sugar', 'N/A'),
                                 entry.get('dose', 'N/A')
                             ))