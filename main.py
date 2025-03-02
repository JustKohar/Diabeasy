# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from auth import validate_user, register_user
from gui import InsulinApp
from data_manager import get_data_dir

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insulin Calculator - Login")
        self.geometry("400x450")
        self.configure(bg="#f0f0f0")
        self.style = ttk.Style()
        
        # Configure custom styles
        self.style.theme_use('clam')
        self.style.configure("TButton", 
            font=("Arial", 10, "bold"),
            padding=8,
            borderwidth=0,
            foreground="white",
            background="#2c3e50"
        )
        self.style.map("TButton",
            background=[("active", "#34495e"), ("disabled", "#bdc3c7")],
            relief=[("active", "groove"), ("!active", "flat")]
        )
        
        # Load and display logo
        self.load_logo()
        
        # Create widgets
        self.create_widgets()

    def load_logo(self):
        try:
            self.logo = tk.PhotoImage(file="download.png")
            logo_label = tk.Label(self, image=self.logo, bg="#f0f0f0")
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {str(e)}")

    def create_widgets(self):
        # Main container
        container = ttk.Frame(self)
        container.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Username field
        ttk.Label(container, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_entry = ttk.Entry(container)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Password field
        ttk.Label(container, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_entry = ttk.Entry(container, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Button container
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=2, columnspan=2, pady=20, sticky=tk.EW)
        
        # Login button
        login_btn = ttk.Button(btn_frame, text="Login", command=self.login, style="TButton")
        login_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Register button
        register_btn = ttk.Button(btn_frame, text="Register", command=self.register, style="TButton")
        register_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Configure grid weights
        container.columnconfigure(1, weight=1)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
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
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
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