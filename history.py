import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import pdfkit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


class HistoryTab(ttk.Frame):
    """Frame container for displaying insulin history in a tabular format"""

    def __init__(self, parent):
        """Initialize the history tab frame"""
        super().__init__(parent)
        self.history_data = []  # Store history data for graphing
        self.graph_canvas = None  # Store reference to graph
        self.hide_graph_button = None  # Store reference to Hide Graph button
        self.create_widgets()

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
        self.tree.grid(row=0, column=0, columnspan=3, sticky='nsew')
        scrollbar.grid(row=0, column=3, sticky='ns')

        # Configure grid resizing behavior
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Dropdown to select graph time scale
        self.graph_type_label = ttk.Label(self, text="Graph Time Scale:")
        self.graph_type_label.grid(row=1, column=0, pady=5, sticky='w')

        self.graph_type = ttk.Combobox(self, values=["Days", "Hours", "Minutes"], state="readonly")
        self.graph_type.grid(row=1, column=1, pady=5, sticky='w')
        self.graph_type.current(0)  # Default to "Days"

        # Buttons
        self.export_csv_button = ttk.Button(self, text='Export CSV', command=self.export_to_csv)
        self.export_csv_button.grid(row=2, column=0, pady=5, sticky='w')

        self.export_pdf_button = ttk.Button(self, text='Export PDF', command=self.export_to_pdf)
        self.export_pdf_button.grid(row=2, column=1, pady=5, sticky='e')

        self.show_graph_button = ttk.Button(self, text='Show Graph', command=self.show_graph)
        self.show_graph_button.grid(row=2, column=2, pady=5, sticky='e')

        self.delete_entry_button = ttk.Button(self, text="Delete Entry", command=self.delete_selected_entry)
        self.delete_entry_button.grid(row=2, column=3, pady=5, sticky='e')  # New Delete Button

    def update_history(self, history_data):
        """Update the displayed history with new data"""
        self.history_data = history_data  # Store data for graphing

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

        if not history_data:
            self.tree.insert('', 'end', values=('No Data', '', '', ''))

    def delete_selected_entry(self):
        """Deletes the selected entry from the history log"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Delete Entry", "Are you sure you want to delete this entry?")
        if not confirm:
            return

        # Remove from UI
        for item in selected_item:
            values = self.tree.item(item)['values']
            self.tree.delete(item)

            # Remove from history data
            self.history_data = [entry for entry in self.history_data if
                                 (entry['date'], entry['time'], entry['blood_sugar'], entry['dose']) != tuple(values)]

    def sort_treeview(self, col, reverse=False):
        """Sorts the Treeview column in ascending or descending order"""
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        try:
            data.sort(key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0], reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)

        for index, (_, child) in enumerate(data):
            self.tree.move(child, '', index)

        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def export_to_csv(self):
        """Exports the Treeview data to a CSV file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Time', 'Blood Sugar', 'Dose'])
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)['values'])

    def export_to_pdf(self):
        """Exports the Treeview data to a PDF file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            html_content = "<html><head><title>Insulin History</title></head><body>"
            html_content += "<h2>Insulin History</h2><table border='1'><tr><th>Date</th><th>Time</th><th>Blood Sugar</th><th>Dose</th></tr>"
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                html_content += f"<tr><td>{values[0]}</td><td>{values[1]}</td><td>{values[2]}</td><td>{values[3]}</td></tr>"
            html_content += "</table></body></html>"

            config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
            pdfkit.from_string(html_content, file_path, configuration=config)

    def show_graph(self):
        """Displays a scatter plot of Blood Sugar Levels based on selected time scale"""
        if not self.history_data:
            return

        selected_scale = self.graph_type.get()

        x_values = []
        blood_sugar_levels = []

        for entry in self.history_data:
            try:
                date_obj = datetime.strptime(entry['date'], "%Y-%m-%d")
                time_obj = datetime.strptime(entry['time'], "%H:%M")

                if selected_scale == "Days":
                    x_values.append(date_obj.strftime("%Y-%m-%d"))
                elif selected_scale == "Hours":
                    x_values.append(time_obj.hour + time_obj.minute / 60)
                elif selected_scale == "Minutes":
                    x_values.append(time_obj.hour * 60 + time_obj.minute)

                blood_sugar_levels.append(float(entry['blood_sugar']))
            except ValueError:
                continue

        fig, ax = plt.subplots()
        ax.scatter(x_values, blood_sugar_levels, color='b', label='Blood Sugar', alpha=0.7)
        ax.set_ylabel('Blood Sugar (mg/dL)')
        ax.set_title('Blood Sugar Levels Over Time')
        ax.grid()
        ax.legend()
        plt.show()
