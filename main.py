import tkinter as tk
from tkinter import ttk, messagebox
from auth import validate_user, register_user
from gui import InsulinApp
from data_manager import get_data_dir

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insulin Calculator - Login")
        self.geometry("300x200")
        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Login", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Register", command=self.register).pack(side=tk.LEFT, padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if validate_user(username, password):
            self.destroy()
            app = InsulinApp(username)
            app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful")
        else:
            messagebox.showerror("Error", "Username already exists")

if __name__ == "__main__":
    get_data_dir().mkdir(parents=True, exist_ok=True)
    LoginWindow().mainloop()