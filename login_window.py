import tkinter as tk
from auth import authenticate, register_user
from main_app import MainApp

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Insulin Tracker - Login")
        
        # Widgets
        tk.Label(master, text="Username:").grid(row=0)
        tk.Label(master, text="Password:").grid(row=1)
        
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")
        
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        
        tk.Button(master, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(master, text="Register", command=self.register).grid(row=2, column=1)

    def get_credentials(self):
        return (
            self.username_entry.get().strip(),
            self.password_entry.get().strip()
        )

    def login(self):
        username, password = self.get_credentials()
        if not username or not password:
            tk.messagebox.showerror("Error", "All fields required!")
            return
            
        if authenticate(username, password):
            self.master.destroy()
            root = tk.Tk()
            MainApp(root, username)
            root.mainloop()
        else:
            tk.messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username, password = self.get_credentials()
        if not username or not password:
            tk.messagebox.showerror("Error", "All fields required!")
            return
            
        if register_user(username, password):
            tk.messagebox.showinfo("Success", "Registration successful")