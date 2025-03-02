import tkinter as tk
from tkinter import ttk, filedialog
import csv
import pdfkit
from datetime import datetime


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
                                 show='headings')

        # Configure column headers and width
        columns = [('Date', 100), ('Time', 80), ('Blood Sugar', 120), ('Dose', 80)]
        for col, width in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c, False))
            self.tree.column(col, width=width, anchor='center')

        # Create vertical scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid layout configuration
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure grid resizing behavior
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add Export Buttons
        self.export_csv_button = ttk.Button(self, text='Export CSV', command=self.export_to_csv)
        self.export_csv_button.grid(row=1, column=0, pady=5, sticky='w')

        self.export_pdf_button = ttk.Button(self, text='Export PDF', command=self.export_to_pdf)
        self.export_pdf_button.grid(row=1, column=0, pady=5, sticky='e')

        # Apply styling
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    def update_history(self, history_data):
        """Update the displayed history with new data
        Args:
            history_data: List of dictionaries containing history entries
        """
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new entries with formatted data
        for entry in history_data:
            date = entry.get('date', 'N/A')
            time = entry.get('time', 'N/A')
            blood_sugar = entry.get('blood_sugar', 'N/A')
            dose = entry.get('dose', 'N/A')
            self.tree.insert('', 'end', values=(date, time, blood_sugar, dose))

        # Handle empty data case
        if not history_data:
            self.tree.insert('', 'end', values=('No Data', '', '', ''))

    def sort_treeview(self, col, reverse=False):
        """Sorts the Treeview column in ascending or descending order"""
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        # Attempt to sort numerically, else sort as string
        try:
            data.sort(key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0], reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)

        for index, (_, child) in enumerate(data):
            self.tree.move(child, '', index)

        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def export_to_csv(self):
        """Exports the Treeview data to a CSV file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Time', 'Blood Sugar', 'Dose'])
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)['values'])

    def export_to_pdf(self):
        """Exports the Treeview data to a PDF file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if file_path:
            html_content = "<html><head><title>Insulin History</title></head><body>"
            html_content += "<h2>Insulin History</h2><table border='1'><tr><th>Date</th><th>Time</th><th>Blood Sugar</th><th>Dose</th></tr>"
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                html_content += f"<tr><td>{values[0]}</td><td>{values[1]}</td><td>{values[2]}</td><td>{values[3]}</td></tr>"
            html_content += "</table></body></html>"

            # Specify the wkhtmltopdf path
            config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

            # Convert HTML to PDF
            pdfkit.from_string(html_content, file_path, configuration=config)

