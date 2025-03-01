import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from auth import authenticate, register_user
from main_app import MainApp


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Insulin Tracker - Login")
        self.master.geometry("400x400")  # Set window size

        # Load and display image
        try:
            self.bg_image = ImageTk.PhotoImage(Image.open("download.png").resize((200, 200)))
            self.image_label = tk.Label(master, image=self.bg_image)
            self.image_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Login logo image not found")

        # Create form frame
        self.form_frame = tk.Frame(master)
        self.form_frame.pack(pady=20)

        # Widgets
        tk.Label(self.form_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        tk.Label(self.form_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)

        self.username_entry = tk.Entry(self.form_frame, font=("Arial", 12))
        self.password_entry = tk.Entry(self.form_frame, show="*", font=("Arial", 12))

        self.username_entry.grid(row=0, column=1, pady=5)
        self.password_entry.grid(row=1, column=1, pady=5)

        # Buttons with styling
        button_style = {"font": ("Arial", 12), "width": 10}
        tk.Button(self.form_frame, text="Login", command=self.login, **button_style, bg="#4CAF50", fg="white"
                  ).grid(row=2, column=0, pady=10, padx=5)
        tk.Button(self.form_frame, text="Register", command=self.register, **button_style, bg="#2196F3", fg="white"
                  ).grid(row=2, column=1, pady=10, padx=5)

    def get_credentials(self):
        return (
            self.username_entry.get().strip(),
            self.password_entry.get().strip()
        )

    def login(self):
        username, password = self.get_credentials()
        if not username or not password:
            messagebox.showerror("Error", "All fields required!")
            return

        if authenticate(username, password):
            self.master.destroy()
            root = tk.Tk()
            MainApp(root, username)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username, password = self.get_credentials()
        if not username or not password:
            messagebox.showerror("Error", "All fields required!")
            return

        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful")


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()