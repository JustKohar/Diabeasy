# Import GUI framework and application components
import tkinter as tk
from auth import authenticate, register_user  # Security and user management
from main_app import MainApp  # Main application interface


class LoginWindow:
    """Tkinter window for user authentication and registration"""

    def __init__(self, master):
        """Initialize login interface
        Args:
            master: Parent Tkinter container
        """
        self.master = master
        self.master.title("Insulin Tracker - Login")  # Window title

        # Create username/password input fields
        tk.Label(master, text="Username:").grid(row=0)  # Username label
        tk.Label(master, text="Password:").grid(row=1)  # Password label

        # Entry widgets for credential input
        self.username_entry = tk.Entry(master)  # Plain text username field
        self.password_entry = tk.Entry(master, show="*")  # Masked password field

        # Grid layout positioning
        self.username_entry.grid(row=0, column=1)  # Username input position
        self.password_entry.grid(row=1, column=1)  # Password input position

        # Action buttons
        tk.Button(master, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(master, text="Register", command=self.register).grid(row=2, column=1)

    def get_credentials(self) -> tuple:
        """Retrieve and sanitize user inputs
        Returns:
            Tuple of (username, password) with whitespace removed
        """
        return (
            self.username_entry.get().strip(),  # Clean username input
            self.password_entry.get().strip()  # Clean password input
        )

    def login(self):
        """Handle login attempt with validation"""
        username, password = self.get_credentials()

        # Empty field validation
        if not username or not password:
            tk.messagebox.showerror("Error", "All fields required!")
            return

        # Authentication check
        if authenticate(username, password):
            # Close login window
            self.master.destroy()
            # Launch main application
            root = tk.Tk()
            MainApp(root, username)
            root.mainloop()
        else:
            # Failed credentials feedback
            tk.messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        """Handle new user registration"""
        username, password = self.get_credentials()

        # Input validation
        if not username or not password:
            tk.messagebox.showerror("Error", "All fields required!")
            return

        # Registration attempt
        if register_user(username, password):
            tk.messagebox.showinfo("Success", "Registration successful")