import tkinter as tk
from tkinter import ttk

class HistoryTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Date', 'Time', 'Blood Sugar', 'Dose'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Blood Sugar', text='Blood Sugar (mg/dL)')
        self.tree.heading('Dose', text='Dose (units)')
        
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_history(self, history_data):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for entry in history_data:
            self.tree.insert('', 'end', values=(
                entry.get('date', 'N/A'),
                entry.get('time', 'N/A'),
                entry.get('blood_sugar', 'N/A'),
                entry.get('dose', 'N/A')
            ))