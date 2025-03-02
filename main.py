# main.py
import tkinter as tk  # Import tkinter for GUI components
from tkinter import ttk, messagebox  # Import additional tkinter components
from auth import validate_user, register_user  # Import authentication functions
import gui  # Import the gui module (InsulinApp)
from data_manager import get_data_dir  # Import function to get data directory

class LoginWindow(tk.Tk):  # Define the LoginWindow class, inheriting from Tk
    def __init__(self):
        super().__init__()  # Initialize the parent Tk class
        self.title("Insulin Calculator - Login")  # Set the window title
        self.geometry("400x450")  # Set window size
        self.configure(bg="#f0f0f0")  # Set background color of the window
        self.style = ttk.Style()  # Create an instance of ttk.Style for custom styling

        # Configure custom styles for the buttons
        self.style.theme_use('clam')  # Use the clam theme for the window
        self.style.configure("TButton",
            font=("Arial", 10, "bold"),  # Set the font of the buttons
            padding=8,  # Set padding for buttons
            borderwidth=0,  # Remove border width
            foreground="white",  # Set button text color to white
            background="#2c3e50"  # Set button background color
        )
        self.style.map("TButton",  # Configure button interaction effects (hover and disabled states)
            background=[("active", "#34495e"), ("disabled", "#bdc3c7")],  # Change background color when active/disabled
            relief=[("active", "groove"), ("!active", "flat")]  # Set relief style based on active state
        )

        # Load and display logo
        self.load_logo()  # Call the method to load the logo image

        # Create widgets for the login interface
        self.create_widgets()

    def load_logo(self):
        """Load the logo image and display it on the window"""
        try:
            self.logo = tk.PhotoImage(file="download.png")  # Try to load the logo image from file
            logo_label = tk.Label(self, image=self.logo, bg="#f0f0f0")  # Create a label to display the logo
            logo_label.pack(pady=10)  # Pack the logo label with padding
        except Exception as e:
            print(f"Error loading logo: {str(e)}")  # Print an error if the logo cannot be loaded

    def create_widgets(self):
        """Create all the widgets for the login window"""
        # Main container for the input fields and buttons
        container = ttk.Frame(self)
        container.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Username field
        ttk.Label(container, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)  # Label for the username field
        self.username_entry = ttk.Entry(container)  # Entry widget for username input
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)  # Grid the username entry widget

        # Password field
        ttk.Label(container, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)  # Label for the password field
        self.password_entry = ttk.Entry(container, show="*")  # Entry widget for password input (hidden)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)  # Grid the password entry widget

        # Button container for the login and register buttons
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=2, columnspan=2, pady=20, sticky=tk.EW)  # Grid the button container

        # Login button that triggers the login method
        login_btn = ttk.Button(btn_frame, text="Login", command=self.login, style="TButton")
        login_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)  # Pack the login button to the left

        # Register button that triggers the register method
        register_btn = ttk.Button(btn_frame, text="Register", command=self.register, style="TButton")
        register_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)  # Pack the register button to the left

        # Configure the grid to allow the username and password fields to expand
        container.columnconfigure(1, weight=1)

    def login(self):
        """Handle the login logic when the user clicks the login button"""
        username = self.username_entry.get().strip()  # Get the username input and remove surrounding whitespace
        password = self.password_entry.get().strip()  # Get the password input and remove surrounding whitespace

        # Check if username and password are not empty
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")  # Show error message
            return

        # Validate the user's credentials
        if validate_user(username, password):
            self.destroy()  # Close the login window
            app = gui.InsulinApp(username)  # Initialize the main app with the username
            app.mainloop()  # Start the main app loop
        else:
            messagebox.showerror("Error", "Invalid credentials")  # Show error message if credentials are incorrect

    def register(self):
        """Handle the registration logic when the user clicks the register button"""
        username = self.username_entry.get().strip()  # Get the username input and remove surrounding whitespace
        password = self.password_entry.get().strip()  # Get the password input and remove surrounding whitespace

        # Check if username and password are not empty
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")  # Show error message
            return

        # Register the new user
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful")  # Show success message if registration is successful
        else:
            messagebox.showerror("Error", "Username already exists")  # Show error message if username already exists

if __name__ == "__main__":  # Main entry point of the script
    get_data_dir().mkdir(parents=True, exist_ok=True)  # Ensure the data directory exists
    LoginWindow().mainloop()  # Create and run the login window
